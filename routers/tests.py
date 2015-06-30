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
        'routers/table/TestPortfolio.yaml',
        #'routers/table/TestNotify.yaml'
    ]

    def setUp(self):
        self._loader = Loader()
        self._loader.start()

    def test_on_work(self):
        for path in self._paths:
            # add as event listener/sumbit
            graph = self._loader.create_graph(path)
            if graph:
                task = self._loader._create_task(graph, priority=1)
                self._loader._add_waits(task)

    def tearDown(self):
        # unnormal stop
        while True:
            if self._loader.is_ready_to_stop():
                break
        self._loader.join()
        del self._loader
 