# python package

import imp
import sys
import unittest


if sys.version_info < (2, 6):
    for name in (
        'gocept.selenium.tests.test_webdriver',
        'gocept.selenium.tests.test_wd_selenese',
        ):
        m = sys.modules[name] = imp.new_module(name)
        m.test_suite = lambda: unittest.TestSuite()
