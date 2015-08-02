# -*- coding: utf-8 -*-

import unittest
from main.tests import NoSQLTestCase
from routers.loader import Loader
from routers.generator import Constraint, Generator

skip_tests = {
    # static 
    'TestLoaderStrategy': True,
    'TestAlwaysRunStrategy': False,
    'TestGeneratorRandom': True
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
                print node['kwargs']
                self.assertTrue(node['kwargs'])
                self.assertTrue(node['retval'])
                self.assertTrue(node['runtime'] <= 100)
            del G

    def tearDown(self):
        del self._loader


@unittest.skipIf(skip_tests['TestAlwaysRunStrategy'], "skip")
class TestAlwaysRunStrategy(NoSQLTestCase):
 
    _paths = [
        'routers/table/ExcAlgDualema.yaml',
        'routers/table/ExcRptDualema.yaml',
        'routers/table/ExcAlgBBands.yaml',
        'routers/table/ExcRptBBands.yaml',
        #'routers/table/ExcAlgBTrader.yaml',
        #'routers/table/ExcRptBTrader.yaml'
    ]

    def setUp(self):
        self._loader = Loader()
        self._graphs = []

    def test_on_run(self):
        for path in self._paths:
            G = self._loader.create_graph(path, priority=1, debug=False)
            self.assertTrue(G)
            G.start()
            self._graphs.append(G)

        for G in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()
            del G

    def tearDown(self):
        del self._loader


@unittest.skipIf(skip_tests['TestGeneratorRandom'], "skip")
class TestGeneratorRandom(NoSQLTestCase):

    _paths = [
        'routers/learn/TestLearn0.yaml'
    ]

    def setUp(self):
        self._graphs = []

    def test_on_run(self):
        for path in self._paths:
            cst = Constraint.load(path)
            print cst
            self._gntor = Generator(cst, debug=True)
            self._gntor.run()
            self._gntor.report()
            self._gntor.export()
   
    def tearDown(self):
        del self._gntor
