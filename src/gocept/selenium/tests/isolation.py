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

ENSURE_ORDER = False


class IsolationTests(object):

    # test_0_set and test_1_get verify that different test methods are isolated
    # from each other, i.e. that the underlying DemoStorage stacking is wired
    # up correctly

    def test_0_set(self):
        global ENSURE_ORDER
        self.selenium.open('http://%s/set.html' % self.selenium.server)
        self.selenium.open('http://%s/get.html' % self.selenium.server)
        self.selenium.assertBodyText('1')
        ENSURE_ORDER = True

    def test_1_get(self):
        global ENSURE_ORDER
        self.assertEquals(ENSURE_ORDER, True,
                          'Set test was not run before get test')
        self.selenium.open('http://%s/get.html' % self.selenium.server)
        self.selenium.assertNotBodyText('1')
        ENSURE_ORDER = False

    # subclasses need to implement getRootFolder() and getDatabase()
    # for the tests below to work

    def test_each_request_gets_a_separate_zodb_connection(self):
        self.selenium.open(
            'http://%s/inc-volatile.html' % self.selenium.server)
        self.selenium.assertBodyText('1')
        # We demonstrate isolation using volatile attributes (which are
        # guaranteed not to be present on separate connections). But since
        # there is no guarantee that volatile attributes disappear on
        # transaction boundaries, we need to prevent re-use of the first
        # connection -- to avoid trouble like "it's the same connection, so the
        # volatile attribute is still there".
        #
        # The proper way to do this would be two requests that are processing
        # concurrently, but a) gocept.selenium is not prepared for
        # multi-threaded requests and b) simulating that would be a major pain,
        # so we cheat and force the opening of another connection by claiming
        # one here.
        db = self.getDatabase()
        conn = db.open()
        self.selenium.open(
            'http://%s/inc-volatile.html' % self.selenium.server)
        conn.close()
        self.selenium.assertBodyText('1')

    def test_requests_get_different_zodb_connection_than_tests(self):
        root = self.getRootFolder()
        root._v_counter = 1
        self.selenium.open(
            'http://%s/inc-volatile.html' % self.selenium.server)
        self.selenium.assertBodyText('1')
