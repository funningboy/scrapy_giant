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
        super(DAGWorker, self).__init__()
        threading.Thread.__init__(self)
        self._run_queue = []
        self._wait_queue = []
        self._finish_queue = []
        self._record_queue = []
        self._debug_queue = []
        self._maxloop_count = 0
        self._stop = threading.Event()

    @property
    def record(self):
        return self._record_queue

    def stop(self):
        self._stop.set()

    def stopped(cls):
        return self._stop.isSet()

    def set_start_to_run(self, node):
        if self.node[node]['ptr'].status != 'start':
            self.node[node]['ptr'].status = 'start'
            self._start_to_run(node)
            self._add_run_queue(node)

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
        results = map(lambda x: self._is_ready_to_run(x), self._wait_queue)
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
        [results.extend(self._is_ready_to_wait(it)) for it in self._finish_queue]
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_join(self, node):
        return (node, self.node[node]['ptr'].is_ready() and self.node[node]['ptr'].status == 'run')

    def _find_ready_to_join(self):
        results = map(lambda x: self._is_ready_to_join(x), self._run_queue)
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
            rec = {
                'node': node,
                'retval': self.node[node]['ptr'].retval,
                'visited': self.node[node]['ptr'].visited,
                'runtime': round(self.node[node]['ptr'].runtime.timeit(), 2)
            }
            self._record_queue.append(rec)

    def _switch_to_idle(self, node):
        if self.node[node]['ptr'].status != 'idle':
            self.node[node]['ptr'].status = 'idle'

    def _add_run_queue(self, node):
        if node not in self._run_queue:
            self._run_queue.append(node)

    def _del_run_queue(self, node):
        if node in self._run_queue:
            self._run_queue.remove(node)

    def _add_wait_queue(self, node):
        if node not in self._wait_queue:
            self._wait_queue.append(node)

    def _del_wait_queue(self, node):
        if node in self._wait_queue:
            self._wait_queue.remove(node)

    def _add_finish_queue(self, node):
        if node not in self._finish_queue:
            self._finish_queue.append(node)

    def _del_finish_queue(self, node):
        if node in self._finish_queue:
            self._finish_queue.remove(node)

    def _find_ready_to_finish(self):
        return len(self._run_queue) == 0

    def _dump_run_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._run_queue)

    def _dump_wait_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._wait_queue)

    def _dump_finish_queue(self):
        return map(lambda x: (x, self.node[x]['ptr'].status), self._finish_queue)

    @property
    def cover(self):
        try:
            cover = len(self._finish_queue) / self.number_of_nodes()
            return round(cover, 2)
        except:
            return 0

    @property
    def uncover(self):
        try:
            uncover = (self.number_of_nodes() - len(self._finish_queue)) / self.number_of_nodes()
            return round(uncover, 2)
        except:
            return 0

    def _collect_debug_msg(self):
        item = {
            'run': self._dump_run_queue(),
            'wait': self._dump_wait_queue(),
            'finish': self._dump_finish_queue()
        }
        if self._debug_queue:
            if self._debug_queue[-1] == item:
                self._maxloop_count += 1
            else:
                self._debug_queue.append(item)
                self._maxloop_count = 0
        else:
            self._debug_queue.append(item)

    def _dump_debug_queue(self):
        for it in self._debug_queue:
            yield it
  
    def _is_maxloop_out(self):
        return self._maxloop_count >= self._maxloop and self._maxloop != -1
        
    def clear(self):
        self._run_queue[:] = []    
        self._wait_queue[:] = []
        self._finish_queue[:] = []
        self._record_queue[:] = []
        self._debug_queue[:] = []

    def debug(self):
        if self._debug:
            for node in self._dump_debug_queue():
                print node

    def run(self, callback=None):
        # need gevent let ?
        while not self._find_ready_to_finish():

            for node in self._find_ready_to_join():
                self._join_to_run(node)
                self._add_finish_queue(node)
                self._del_run_queue(node)

            for node in self._find_ready_to_wait():
                self._add_wait_queue(node)

            for node in self._find_ready_to_run():
                self._start_to_run(node)
                self._add_run_queue(node)
                self._del_wait_queue(node)

            if self._debug:
                self._collect_debug_msg()
                if self._is_maxloop_out():
                    print 'find maxloop out, please check DAG has cycles/unreachable nodes'
                    if callback:
                        callback()
                    self.clear()
                    break
