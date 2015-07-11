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
        'routers/table/TestStockProfile0.yaml',
        'routers/table/TestStockProfile1.yaml',
        'routers/table/TestTraderProfile0.yaml',
        'routers/table/TestTraderProfile1.yaml',
        'routers/table/TestExcAlgDualema.yaml',
        'routers/table/TestExcRptDualema.yaml',
        'routers/table/ExcAlgDualema.yaml',
        'routers/table/ExcRptDualema.yaml',
        #'routers/table/TestNtyAll.yaml'
    ]

    def setUp(self):
        self._loader = Loader()
        self._graphs = []

    def test_on_work(self):
        for path in self._paths:
            # add as event listener/sumbit
            G = self._loader.create_graph(path, priority=1)
            self.assertTrue(G)
            G.start()
            self._graphs.append(G)

        for G in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()
            nodes = sorted(G.record, key=lambda x: x['node'])
            for node in nodes:
                self.assertTrue(node['visited'] == 1)
                # how to handle None
                print node['node']
                print node['kwargs']
                print node['retval']
                #self.assertTrue(node['retval'])
                #self.assertTrue(node['runtime'] <= 10)
            del G

    def tearDown(self):
        del self._loader
 