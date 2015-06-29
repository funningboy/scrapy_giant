# -*- coding: utf-8 -*-

import unittest
import time
import networkx as nx
from main.tests import NoSQLTestCase
from workers.worker import DAGWorker
from workers.nodes import Node
from bin.tasks import nsum, navg

skip_tests = {
    # static graph
    'TestTaskPtr': False,
    'TestDAGChain': False,
    'TestDAGParallel': False,
    'TestDAGNoCycle': False,
    # dynamic graph
    'TestDAGDymUpdate': False
}

class TestDAGWorker(DAGWorker):

    def __init__(self, **kwargs):
        super(TestDAGWorker, self).__init__(**kwargs)

    def _collect_incoming_kwargs(self, node):
        args = list(self.node[node]['ptr']._args)
        for pre, cur in self.in_edges(node):
            if self.node[pre]['ptr'].status == 'finish':
                retval = self.node[pre]['ptr'].retval
                try:
                    if isinstance(retval, object):
                        retval = [retval]
                    args.extend(retval)
                except:
                    print 'incoming args is only for list,object'
                    raise
        args = [i for i in args if i]
        self.node[node]['ptr']._args = args
   
@unittest.skipIf(skip_tests['TestTaskPtr'], "skip")
class TestTaskPtr(NoSQLTestCase):

    def setUp(self):
        self.G = TestDAGWorker(deubg=True)
        n = Node(func=nsum, args=(1,2))
        self.G.add_node(0, {'ptr': n})

    def test_on_run(self):
        self.G.node[0]['ptr'].run()
        while not self.G.node[0]['ptr'].is_ready():
            time.sleep(1)
        self.G.node[0]['ptr'].finish()
        retval = self.G.node[0]['ptr'].retval
        self.assertTrue(retval == 3)

    def tearDown(self):
        self.G.clear()
        del self.G

@unittest.skipIf(skip_tests['TestDAGChain'], "skip")
class TestDAGChain(NoSQLTestCase):
    """ n: n(0), n(1), n(2)
        e: e(n(0)->n(1),weight=1), e(n(1)->n(2),weight=1)
    """

    def setUp(self):
        self.G = TestDAGWorker(debug=True)
        for i in range(1,3):
            self.G.add_edge(i-1, i, weight=1)
        for i in range(0,3):
            n = Node(func=nsum, args=(1,2))
            self.G.add_node(i, {'ptr': n})
        # no cycle, loop 
        self.assertTrue(nx.is_directed_acyclic_graph(self.G))
        self.assertTrue(nx.topological_sort(self.G) == [0,1,2])
        self.assertTrue(nx.ancestors(self.G,0) == set([]))
        self.assertTrue(nx.descendants(self.G,0) == set([1,2]))
        self.G.set_start_to_run(0)
        self.G.run(self.G.debug)

    def test_on_run(self):
        nodes = sorted(self.G.record, key=lambda x: x['node'])
        self.assertTrue(len(nodes) == 3)
        expect = [3,6,9]
        for i in range(3):
            self.assertTrue(nodes[i]['visited'] == 1)
            self.assertTrue(nodes[i]['retval'] == expect[i])

    def tearDown(self):
        self.G.clear()
        del self.G

@unittest.skipIf(skip_tests['TestDAGParallel'], "skip")
class TestDAGParallel(NoSQLTestCase):
    """ n: n(0), n(1), n(2), n(3)
        e: e(n(0)->n(1), weight=2),
           e(n(0)->n(2), weight=2),
           e(n(2)->n(3), weight=2)
    """

    def setUp(self):
        self.G = TestDAGWorker(debug=True)
        self.G.add_edge(0, 1, weight=2)
        self.G.add_edge(0, 2, weight=2)
        self.G.add_edge(2, 3, weight=2)
        for i in range(0,4):
            n = Node(func=nsum, args=(1,2))
            self.G.add_node(i, {'ptr': n})
        self.assertTrue(nx.is_directed_acyclic_graph(self.G))
        self.assertTrue(nx.ancestors(self.G,0) == set([]))
        self.assertTrue(nx.descendants(self.G,0) == set([1,2,3]))
        self.G.set_start_to_run(0)
        self.G.run(self.G.debug)

    def test_on_run(self):
        nodes = sorted(self.G.record, key=lambda x: x['node'])
        self.assertTrue(len(nodes) == 4)
        expect = [3,6,6,9]
        for i in range(4):
            self.assertTrue(nodes[i]['visited'] == 1)
            self.assertTrue(nodes[i]['retval'] == expect[i])

    def tearDown(self):
        self.G.clear()
        del self.G

@unittest.skipIf(skip_tests['TestDAGNoCycle'], "skip")
class TestDAGNoCycle(NoSQLTestCase):
    """ n: n(0), n(1), n(2), n(3)
        e: e(n(0)->n(1),weight=2), e(n(1)->n(2),weight=2),
           e(n(0)->n(3),weight=2), e(n(3)->n(2),weight=2),
           e(n(0)->n(2),weight=2)
    """
    
    def setUp(self):
        self.G = TestDAGWorker(debug=True)
        self.G.add_edge(0,1, weight=2)
        self.G.add_edge(1,2, weight=2)
        self.G.add_edge(0,2, weight=2)
        self.G.add_edge(0,3, weight=2)
        self.G.add_edge(3,2, weight=2)
        for i in range(0,4):
            n = Node(func=nsum, args=(1,2))
            self.G.add_node(i, {'ptr': n})
        # no cycle, loop
        self.assertTrue(nx.is_directed_acyclic_graph(self.G))
        self.G.set_start_to_run(0)
        self.G.run(self.G.debug)

    def test_on_run(self):
        nodes = sorted(self.G.record, key=lambda x: x['node'])  
        self.assertTrue(len(nodes) == 4)
        expect = [3, 6, 18, 6]
        for i in range(4):
            self.assertTrue(nodes[i]['visited'] == 1)
            self.assertTrue(nodes[i]['retval'] == expect[i])

    def tearDown(self):
        #with open("test.adjlist",'wb') as fh:
        #    nx.write_adjlist(self.G, fh)
        self.G.clear()
        del self.G