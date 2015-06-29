# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta 
from main.tests import NoSQLTestCase
from routers.manager import GiantManager
skip_tests = {
	# static 
	'TestManagerStatic': False
	# 
} 

@unittest.skipIf(skip_tests['TestManagerStatic'], "skip")
class TestManagerStatic(NoSQLTestCase):

	_paths = [
		'routers/table/TestStockProfile.yaml',
		'routers/table/TestTraderProfiel.yaml',
		'routers/table/TestPortfolio.yaml'
	]

	def setUp(self):
		self._mgr = GiantManager()
		self._mgr.start()

	def test_on_work(self):
		for path in self._paths:
			G = self._mgr.create_graph(path)
			self.assertTrue(G)
			if G:
				task = self._mgr._create_task(G, priority=1)
				self._mgr._add_task_queue(task)

	def tearDown(self):
		while True:
			if self._mgr.is_ready_to_stop():
				self._mgr.stop()
				break

 