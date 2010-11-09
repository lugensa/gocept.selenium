#############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
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
from gocept.selenium.grok import GrokLayer
from gocept.selenium.grok.fixtures import App

class TestGrokTestCase(gocept.selenium.grok.TestCase):

    layer = GrokLayer(gocept.selenium.grok)

    def setUp(self):
        super(TestGrokTestCase, self).setUp()
        root = self.layer.getRootFolder()
        root['app'] = App()
        transaction.commit()

    def test_grok_layer(self):
        layer = self.layer
        self.assertTrue(layer.thread.is_alive())

    def test_grok_app(self):
        self.selenium.open('/app')
        self.selenium.assertTextPresent('Hello from grok')

