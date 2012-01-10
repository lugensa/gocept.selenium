#############################################################################
#
# Copyright (c) 2010-2012 Zope Foundation and Contributors.
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
import transaction

import gocept.selenium.grok
import gocept.selenium.grok.fixtures

import gocept.selenium.tests.isolation

test_layer = gocept.selenium.grok.Layer(gocept.selenium.grok)


class TestGrokTestCase(gocept.selenium.grok.TestCase):

    layer = test_layer

    def setUp(self):
        super(TestGrokTestCase, self).setUp()
        root = self.getRootFolder()
        root['app'] = gocept.selenium.grok.fixtures.App()
        transaction.commit()

    def test_grok_layer(self):
        layer = self.layer
        self.assertTrue(layer.thread.isAlive())

    def test_grok_app(self):
        self.selenium.open('/app')
        self.selenium.assertTextPresent('Hello from grok')


class GrokIsolation(gocept.selenium.tests.isolation.IsolationTests,
    gocept.selenium.grok.TestCase):

    layer = test_layer

    def getDatabase(self):
        return self.layer.db
