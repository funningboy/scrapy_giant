# -*- coding: utf-8 -*-

from django.test.simple import DjangoTestSuiteRunner
from django.test import TestCase

class NoSQLTestRunner(DjangoTestSuiteRunner):
    def setup_databases(self):
        pass
    def teardown_databases(self, *args):
        pass

class NoSQLTestCase(TestCase):
    def _fixture_setup(self):
        pass
    def _fixture_teardown(self):
        pass
