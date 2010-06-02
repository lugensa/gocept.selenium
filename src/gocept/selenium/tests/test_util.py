#############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import unittest
from gocept.selenium.base import Layer
from gocept.selenium.util import make_testsuite

class MakeTestSuiteTestCase(unittest.TestCase):
    layer = Layer()

    def test_one_two_three(self):
        self.assert_(True)

class Another(unittest.TestCase):
    def test_four_five(self):
        self.assert_(True)

class SubFromMakeTestSuiteTestCase(MakeTestSuiteTestCase):
    layer = Layer()

class MakeTestSuite(unittest.TestCase):

    def test_make_testsuite(self):
        tests = make_testsuite(
            (MakeTestSuiteTestCase,), ('*firefox', '*googlechrome'))
        self.assertEquals(2, tests.countTestCases())

        tests = make_testsuite(
            (MakeTestSuiteTestCase, Another), ('*firefox', '*googlechrome'))
        self.assertEquals(4, tests.countTestCases())

        tests = make_testsuite(
            (MakeTestSuiteTestCase, SubFromMakeTestSuiteTestCase, Another),
            ('*firefox', '*googlechrome'))
        self.assertEquals(6, tests.countTestCases())

        tests = make_testsuite(
            (MakeTestSuiteTestCase, SubFromMakeTestSuiteTestCase, Another),
            ('*firefox', '*googlechrome', '*ie', '*epihany', '*safari'))
        self.assertEquals(15, tests.countTestCases())

    def test_override_app_host(self):
        tests = make_testsuite(
            (MakeTestSuiteTestCase,), ('*firefox', '*googlechrome'),
            app_host='192.168.1.1')
        for test in tests:
            self.assertEquals('192.168.1.1', test.layer.host)

    def test_override_selenium_server(self):
        tests = make_testsuite(
            (MakeTestSuiteTestCase,), ('*firefox', '*googlechrome'),
            selenium_server='192.168.1.2')
        for test in tests:
            self.assertEquals('192.168.1.2', test._server)

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(MakeTestSuite))
    return suite
