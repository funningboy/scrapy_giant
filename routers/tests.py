# -*- coding: utf-8 -*-

import unittest
from main.tests import NoSQLTestCase
from routers.loader import Loader
from routers.generator import Generator

skip_tests = {
    # static 
    'TestLoaderStrategy': False,
    'TestGeneratorRandom': True
    #
} 

@unittest.skipIf(skip_tests['TestLoaderStrategy'], "skip")
class TestLoaderStrategy(NoSQLTestCase):

    _paths = [
        'routers/table/TestStockProfile0.yaml',
        #'routers/table/TestStockProfile1.yaml',
        #'routers/table/TestTraderProfile0.yaml',
        #'routers/table/TestTraderProfile1.yaml',
        #'routers/table/TestExcAlgDualema.yaml',
        #'routers/table/TestExcRptDualema.yaml',
        #'routers/table/ExcAlgDualema.yaml',
        #'routers/table/ExcRptDualema.yaml',
        #'routers/table/TestNtyAll.yaml'
    ]

    def setUp(self):
        self._loader = Loader()
        self._graphs = []

    def test_on_run(self):
        for path in self._paths:
            # add as event listener/sumbit
            G = self._loader.create_graph(path, priority=1, debug=True)
            self.assertTrue(G)
            G.start()
            self._graphs.append(G)

        for G in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()

            self.assertTrue(G.record)
            nodes = sorted(G.record, key=lambda x: x['node'])
            for node in nodes:
                self.assertTrue(node['visited'] == 1)
                # how to handle None
                self.assertTrue(node['kwargs'])
                self.assertTrue(node['retval'])
                self.assertTrue(node['runtime'] <= 100)
            del G

    def tearDown(self):
        del self._loader


@unittest.skipIf(skip_tests['TestGeneratorRandom'], "skip")
class TestGeneratorRandom(NoSQLTestCase):

    def setUp(self):
        self._graphs = []

    def test_on_run(self):
        for i in range(3):
            # regresion
            #   constrain
            #kwargs = {
            #    ''
            #}
            self._gentor = Generator(**kwargs)
            #constrain = 
            G = self._gentor.create_random_graph(constrain)
            self.assertTrue(G)
            G.start()
            self._graphs.append(G)

        for G in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()
            
            self.assertTrue(G.record)
            nodes = sorted(G.record, key=lambda x: x['node'])
            print nodes
            for node in nodes:
                self.assertTrue(node['visited'] == 1)
                # how to handle None
                print node['node']
                print node['kwargs']
                print node['retval']
            del G

    def tearDown(self):
        del self._gentor
