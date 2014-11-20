# -*- coding: utf-8 -*-

from algorithm.superman_algorithm import run
from test.test_start import TestTwseHisAll

class TestSuperManAlgorithm(TestTwseHisAll):

    def test_on_run(self):
        run(True, 0)

if __name__ == '__main__':
    unittest.main()
