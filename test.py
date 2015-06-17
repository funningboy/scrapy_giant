import networkx as nx
import time
from bin.tasks import add


class Node(object):

    def __init__(self, *args, **kwargs):
        self.status = 'idle'
        self.retval = None
        self.asyncresult = None

    def run(self):
        if not self.asyncresult:
            self.asyncresult = add.delay(2, 3)

    def is_ready(self):
        if self.asyncresult:
            return self.asyncresult.ready()
 
    def finish(self):
        self.retval = self.asyncresult.get()
        self.asyncresult = None

class Worker(nx.DiGraph):
    
    def __init__(self):
        super(Worker, self).__init__()
        self._run_queue = []
        self._wait_queue = []
        self._record = []

    def _is_ready_to_run(self, node):
        # passive mode, wait all incoming nodes are finished and edge weights >0
        if self.node[node]['ptr'].status == 'idle':
            for pre, cur in self.in_edges(node):
                if self.node[pre]['ptr'].status != 'finish' or self.edge[pre][cur]['weight'] <= 0:
                    return (node, False)
        # master mode, start when node is set to run
        elif self.node[node]['ptr'].status == 'run':
            return (node, True)
        else:
            return (node, False)

    def _dec_weight(self, node):
        # dec weight when pre and cur node  are all at finish status
        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish' and self.node[cur]['ptr'].status == 'finish':
                self.edge[pre][cur]['weight'] = self.edge[pre][cur]['weight'] -1

    def _find_ready_to_run(self):
        # iter run node to run_queue
        results = map(lambda x: self._is_ready_to_run(x), self._wait_queue)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_wait(self, node):
        pool = []
        if self.node[node]['ptr'].status != 'idle':
            for cur, nxt in self.out_edges(node):
                if self.edge[cur][nxt]['weight'] < 0:
                    pool.append((nxt, False))
                else:
                    pool.append((nxt, True))
        return pool

    def _find_ready_to_wait(self):
        # 
        results = []
        [results.extend(self._is_ready_to_wait(it)) for it in self._run_queue]
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _is_ready_to_join(self, node):
        return (node, self.node[node]['ptr'].is_ready())

    def _find_ready_to_join(self):
        results = map(lambda x: self._is_ready_to_join(x), self._run_queue)
        for it in set(filter(lambda x: x[1] == True, results)):
            yield it[0]

    def _start_to_run(self, node):
        self.node[node]['ptr'].run()
        self.node[node]['ptr'].status = 'run'

    def _join_to_run(self, node):
        self.node[node]['ptr'].status = 'idle'
        self.node[node]['ptr'].finish()
        retval = self.node[node]['ptr'].retval
        self._record.append(retval)

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

    def _is_ready_to_finish(self, node):
        if self.node[node]['ptr'].status == 'idle':
            for pre, cur in self.in_edges(node):
                if self.edge[pre][cur]['weight'] > 0:
                    return (node, False)
        return (node, True)

    def _find_ready_to_finish(self):
        results = zip(*map(lambda x: self._is_ready_to_finish(x), self._wait_queue))
        return set(list(results[1])) == set([True])

# test self loop
import time
G=Worker()
n = Node()
G.add_node(0, {'ptr': n})
G.add_edge(0, 0, weight=2)
G._add_wait_queue(0)
n.status = 'run'
G.node[0]['ptr'].run()
while not G.node[0]['ptr'].is_ready():
    time.sleep(1)
G.node[0]['ptr'].finish()
print G.node[0]['ptr'].retval

# test

# test 
while G._find_ready_to_finish():
    for node in G._find_ready_to_join():
        G._dec_weight(node)
        G._join_to_run(node)
        G._del_run_queue(node)
    for node in G._find_ready_to_run():
        G._start_to_run(node)
        G._add_run_queue(node)
        G._del_wait_queue(node)
    for node in G._find_ready_to_wait():
        G._add_wait_queue(node)

print G._record