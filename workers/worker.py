# -*- coding: utf-8 -*-

# ref: http://ipython.org/ipython-doc/2/parallel/dag_dependencies.html
# http://networkx.github.io/documentation/networkx-1.9.1/reference/classes.html
# http://www.csie.ntnu.edu.tw/~u91029/DirectedAcyclicGraph.html

import networkx as nx
import timeit 
import threading

class DAGWorker(nx.DiGraph, threading.Thread):
    
    def __init__(self, **kwargs):
        self._debug = kwargs.pop('debug', False)
        self._maxloop = kwargs.pop('maxloop', -1)
        super(DAGWorker, self).__init__(**kwargs)
        self._runs = []
        self._waits = []
        self._finishs = []
        self._records = []
        self._maxloop_count = 0
        threading.Thread.__init__(self)
        self.daemon = True
        self._stop = threading.Event()

    @property
    def record(self):
        return self._records

    def stop(self):
        self._stop.set()

    def stopped(cls):
        return self._stop.isSet()

    def set_start_to_run(self, node):
        if self.node[node]['ptr'].status != 'start':
            self.node[node]['ptr'].status = 'start'
            self._start_to_run(node)
            self._add_runs(node)

    def _is_ready_to_run(self, node):
        if self.node[node]['ptr'].status == 'idle':
            for pre, cur in self.in_edges(node):
                if self.edge[pre][cur]['weight'] <= 0 or self.node[pre]['ptr'].status != 'finish':
                    return (node, False)
            return (node, True)
        return (node, False)

    def _dec_weight(self, node):
        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish' and self.node[cur]['ptr'].status == 'finish':
                self.edge[pre][cur]['weight'] -= 1

    def _find_ready_to_run(self):
        results = map(lambda x: self._is_ready_to_run(x), self._waits)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_wait(self, node):
        pool = []
        if self.node[node]['ptr'].status == 'finish':
            for cur, nxt in self.out_edges(node):
                if self.edge[cur][nxt]['weight'] <= 0 or self.node[nxt]['ptr'].status in ['finish', 'run']:
                    pool.append((nxt, False))
                else:
                    pool.append((nxt, True))
        return pool

    def _find_ready_to_wait(self):
        results = []
        [results.extend(self._is_ready_to_wait(it)) for it in self._finishs]
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_join(self, node):
        return (node, self.node[node]['ptr'].is_ready() and self.node[node]['ptr'].status == 'run')

    def _find_ready_to_join(self):
        results = map(lambda x: self._is_ready_to_join(x), self._runs)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _collect_incoming_kwargs(self, node):
        raise NotImplementedError("subclass should implement this")
   
    def _start_to_run(self, node):
        if self.node[node]['ptr'].status != 'run':
            self._collect_incoming_kwargs(node)
            self.node[node]['ptr'].run()
            self.node[node]['ptr'].status = 'run'
            self.node[node]['ptr'].visited += 1
            self.node[node]['ptr'].runtime = timeit.Timer()

    def _join_to_run(self, node):
        if self.node[node]['ptr'].status != 'finish':
            self.node[node]['ptr'].status = 'finish'
            self.node[node]['ptr'].finish()

    def _create_record(self, node):
        rec = {
            'node': node,
            'retval': self.node[node]['ptr'].retval,
            'visited': self.node[node]['ptr'].visited,
            'runtime': round(self.node[node]['ptr'].runtime.timeit(), 2)
        }
        return rec

    def _switch_to_idle(self, node):
        if self.node[node]['ptr'].status != 'idle':
            self.node[node]['ptr'].status = 'idle'

    def _add_records(self, rec):
        if rec not in self._records:
            self._records.append(rec)

    def _add_runs(self, node):
        if node not in self._runs:
            self._runs.append(node)

    def _del_runs(self, node):
        if node in self._runs:
            self._runs.remove(node)

    def _add_waits(self, node):
        if node not in self._waits:
            self._waits.append(node)

    def _del_waits(self, node):
        if node in self._waits:
            self._waits.remove(node)

    def _add_finishs(self, node):
        if node not in self._finishs:
            self._finishs.append(node)

    def _del_finishs(self, node):
        if node in self._finishs:
            self._finishs.remove(node)

    def _find_ready_to_finish(self):
        return len(self._runs) == 0

    def _dump_runs(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._runs)

    def _dump_waits(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._waits)

    def _dump_finishs(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._finishs)

    @property
    def cover_rate(self):
        try:
            cover = len(self._finishs) / self.number_of_nodes()
            return round(cover, 2)
        except:
            return 0

    @property
    def uncover_rate(self):
        try:
            uncover = (self.number_of_nodes() - len(self._finishs)) / self.number_of_nodes()
            return round(uncover, 2)
        except:
            return 0

    def _is_maxloop_out(self):
        return self._maxloop_count >= self._maxloop and self._maxloop != -1
        
    def close(self):
        self._runs[:] = []    
        self._waits[:] = []
        self._finishs[:] = []
        self._records[:] = []

    #def __del__(self):
    #    self.close()

    def debug(self):
        if self._debug:
            msg = {
                'runs': self._runs,
                'waits': self._waits,
                'finishs': self._finishs
            }
            print msg
        
    def run(self, callback=None):
        # need gevent let ?
        while not self._find_ready_to_finish():

            for node in self._find_ready_to_join():
                self._join_to_run(node)
                rec = self._create_record(node)
                self._add_records(rec)
                self._add_finishs(node)
                self._del_runs(node)

            for node in self._find_ready_to_wait():
                self._add_waits(node)

            for node in self._find_ready_to_run():
                self._start_to_run(node)
                self._add_runs(node)
                self._del_waits(node)

            if self._is_maxloop_out():
                print 'find maxloop out, please check DAG has cycles/unreachable nodes'

                if self._debug:
                    self.debug()

                self.close()
                break
