#############################################################################
#
# Copyright (c) 2009-2010 Zope Foundation and Contributors.
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

def _testcases_for_browser(testcases, browser, app_host, selenium_server):
    suite = unittest.TestSuite()
    for testcase in testcases:
        if app_host is not None:
            testcase.layer.host = app_host
        if selenium_server is not None:
            testcase._server = selenium_server
        # Create a new test class, subclassing the original test case. The
        # name of this new class reflects what browser is used.
        new_testcase = type(
            testcase.__name__+'_'+browser, (testcase,), {'browser': browser})
        suite.addTests(
            unittest.defaultTestLoader.loadTestsFromTestCase(new_testcase))
    return suite

def make_testsuite(testcases, browsers, app_host=None, selenium_server=None):
    """Creates a test suite, where each of the given test cases is replicated
    for each of the given browser names.

    Optionally pass in a selenium_server addresses for testing against a
    Selenium Grid. Note that the application_host address should be accessible
    from the Selenium Remote Control instances that have subscribed to the
    Selenium Grid.

    """
    suite = unittest.TestSuite()
    for browser in browsers:
        suite.addTests(
            _testcases_for_browser(
                testcases, browser, app_host, selenium_server))
    return suite
