# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta 
from main.tests import NoSQLTestCase
from routers.loader import Loader

skip_tests = {
    # static 
    'TestLoaderStrategy': False
    # 
} 

@unittest.skipIf(skip_tests['TestLoaderStrategy'], "skip")
class TestLoaderStrategy(NoSQLTestCase):

    _paths = [
        'routers/table/TestStockProfile.yaml',
        'routers/table/TestTraderProfile.yaml',
        'routers/table/TestPortfolio.yaml'
    ]

    def setUp(self):
        self._loader = Loader()
        self._loader.start()

    def test_on_work(self):
        # add as graph event listener
        for path in self._paths:
            graph = self._loader.create_graph(path)
            if graph:
                task = self._loader._create_task(graph, priority=1)
                self._loader._add_wait_queue(task)

    def tearDown(self):
        # unnormal stop
        while True:
            if self._loader.is_ready_to_stop():
                self._loader.stop()
                break

 