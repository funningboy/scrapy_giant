# -*- coding: utf-8 -*-

import unittest
import time
import networkx as nx
from main.tests import NoSQLTestCase
from workers.worker import DAGWorker
from workers.nodes import Node
from bin.tasks import nsum, navg

skip_tests = {
    'TestTaskPtr': False,
    'TestChain': False,
    'TestDAGGraphNoCycle': False
}

@unittest.skipIf(skip_tests['TestTaskPtr'], "skip")
class TestTaskPtr(NoSQLTestCase):

    def setUp(self):
        self.G = DAGWorker(deubg=True)
        n = Node(func=nsum, args=(1,2))
        self.G.add_node(0, {'ptr': n})

    def test_on_run(self):
        self.G.node[0]['ptr'].run()
        while not self.G.node[0]['ptr'].is_ready():
            time.sleep(1)
        self.G.node[0]['ptr'].finish()
        retval = self.G.node[0]['ptr'].retval
        self.assertTrue(retval == 3)

@unittest.skipIf(skip_tests['TestChain'], "skip")
class TestChain(NoSQLTestCase):
    """ n: n(0), n(1), n(2)
        e: e(n(0)->n(1),weight=2), e(n(1)->n(2),weight=2), e(n(2)->n(3),weight=2)
    """

    def setUp(self):
        self.G = DAGWorker(debug=True)
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
        self.G.run()

    def test_on_run(self):
        nodes = sorted(self.G.record, key=lambda x: x['node'])
        self.assertTrue(len(nodes) == 3)
        expect = [3,6,9]
        for i in range(3):
            self.assertTrue(nodes[i]['visited'] == 1)
            self.assertTrue(nodes[i]['retval'] == expect[i])

@unittest.skipIf(skip_tests['TestDAGGraphNoCycle'], "skip")
class TestDAGGraphNoCycle(NoSQLTestCase):
    """ n: n(0), n(1), n(2), n(3)
        e: e(n(0)->n(1),weight=2), e(n(1)->n(2),weight=2),
           e(n(0)->n(3),weight=2), e(n(3)->n(2),weight=2),
           e(n(0)->n(2),weight=2)
    """
    
    def setUp(self):
        self.G = DAGWorker(debug=True)
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
        self.G.run()

    def test_on_run(self):
        nodes = sorted(self.G.record, key=lambda x: x['node'])  
        self.assertTrue(len(nodes) == 4)
        expect = [3, 6, 18, 6]
        for i in range(4):
            self.assertTrue(nodes[i]['visited'] == 1)
            self.assertTrue(nodes[i]['retval'] == expect[i])

    def tearDown(self):
        fh=open("test.adjlist",'wb')
        nx.write_adjlist(self.G, fh)

        
