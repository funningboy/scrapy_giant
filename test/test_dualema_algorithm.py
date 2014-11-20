# -*- coding: utf-8 -*-

from algorithm.dualema_algorithm import run
from test.test_start import TestTwseHisAll

class TestDualEMATaLib(TestTwseHisAll):

    def test_on_run(self):
        run('twse', True, 0)

if __name__ == '__main__':
    unittest.main()
