# -*- coding: utf-8 -*-

import unittest
import time
from main.tests import NoSQLTestCase
from workers.worker import Worker
from workers.node import Node
from bin.tasks import add, mux


class TestTaskPtr(NoSQLTestCase):

    def setUp(self):
        self.G = WapWorker()
        n = Node(func=add, args=(1,2))
        self.G.add_node(0, {'ptr': n})

	def test_on_run(self):
		self.G.node[0]['ptr'].run()
		while not self.G.node[0]['ptr'].is_ready():
			time.sleep(1)
		self.G.node[0]['ptr'].finish()
		retval = self.G.node[0]['ptr'].retval
		self.assertTrue(retval == 3)


class TestSelfLoop(NoSQLTestCase):

	def setUp(self):
		self.G = Worker()
		n = Node(func=add, args=(1,2))
		self.G.add_node(0, {'ptr': n})
		self.G.add_edge(0, 0, weight=2)
		self.G.set_start_node(0)
	
	def test_on_run(self):
		self.G.run()
		record = self.G.record
		self.assertTrue(len(record) == 2)
		nodes = filter(lambda x: x['node'] == 0, record)
		self.assertTrue(len(nodes) == 2)
		for i in range(2):
			self.assertTrue(nodes[i]['visited'] == i+1)
			self.assertTrue(nodes[i]['retval'] == 3)
		print record


class TestChain(NoSQLTestCase):

	def setUp(self):
		self.G = Worker()

		for i in range(1,3):
			self.G.add_edge(i-1, i, weight=1)
		for i in range(0,3):
			n = Node(func=add, args=(1,2))
    		self.G.add_node(i, {'ptr': n})
		print self.G.node[0]
		self.G.set_start_node(0)
		self.G.degree(weight='weight')
	
	def test_on_run(self):
		self.G.run()
		record = self.G.record
		self.assertTrue(self.G.number_of_edges() == 2)
		self.assertTrue(self.G.number_of_nodes() == 3)
	

class TestNestNoLoop:
	pass

class TestNestLoop:
	pass