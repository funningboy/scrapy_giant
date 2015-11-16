# -*- coding: utf-8 -*-

import unittest
from main.tests import NoSQLTestCase
from routers.loader import Loader
from routers.generator import Constraint, Generator

skip_tests = {
    # static 
    'TestLoaderStrategy': False,
    'TestAlwaysRunStrategy': True,
    'TestGeneratorRandom': True
    #
} 

@unittest.skipIf(skip_tests['TestLoaderStrategy'], "skip")
class TestLoaderStrategy(NoSQLTestCase):

    _paths = [
        ('routers/table/TestStock.yaml', False),
        ('routers/table/TestTrader.yaml', False),
        ('routers/table/TestStockProfile0.yaml', False), 
        ('routers/table/TestTraderProfile0.yaml', False),
        ('routers/table/TestExcAlgDualema.yaml', True),
        ('routers/table/TestExcRptDualema.yaml', False)
        #('routers/table/TestNtyAll.yaml', True)
    ]

    def setUp(self):
        self._loader = Loader()
        self._graphs = []

    def test_on_run(self):
        for path, skip in self._paths:
            G = self._loader.create_graph(path, priority=1, debug=True)
            self._loader.finalize(G)
            self.assertTrue(G)
            G.start()
            self._graphs.append((G, skip))

        for G, skip in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()

            self.assertTrue(G.record)
            nodes = sorted(G.record, key=lambda x: x['node'])
            if not skip:
                for node in nodes:
                    self.assertTrue(node['visited'] == 1)
                    self.assertTrue(node['kwargs'])
                    self.assertTrue(node['retval'])
                    self.assertTrue(node['runtime'] <= 100)
            del G

    def tearDown(self):
        del self._loader


@unittest.skipIf(skip_tests['TestAlwaysRunStrategy'], "skip")
class TestAlwaysRunStrategy(NoSQLTestCase):
 
    # register daily regress as notifier
    _paths = [
        ('routers/table/ExcAlgDualema.yaml', True),
        ('routers/table/ExcRptDualema.yaml', False),
        ('routers/table/ExcAlgBBands.yaml', True),
        ('routers/table/ExcRptBBands.yaml', False),
        ('routers/table/ExcAlgBTrader.yaml', True),
        ('routers/table/ExcRptBTrader.yaml', False)
    ]

    def setUp(self):
        self._loader = Loader()
        self._graphs = []

    def test_on_run(self):
        for path, skip in self._paths:
            G = self._loader.create_graph(path, priority=1, debug=False)
            self._loader.finalize(G)
            self.assertTrue(G)
            G.start()
            self._graphs.append((G, skip))

        for G, skip in self._graphs:
            while True:
                if not G.isAlive():
                    break
            G.join()

            self.assertTrue(G.record)
            nodes = sorted(G.record, key=lambda x: x['node'])
            if not skip:
                for node in nodes:
                    self.assertTrue(node['visited'] == 1)
                    self.assertTrue(node['kwargs'])
                    self.assertTrue(node['retval'])
                    self.assertTrue(node['runtime'] <= 100)
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
