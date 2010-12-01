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

import gocept.selenium.wsgi
from gocept.selenium.wsgi.testing import SimpleApp

class TestLayer(gocept.selenium.wsgi.WSGILayer):
    application = SimpleApp()

test_layer = TestLayer()

class TestWSGITestCase(gocept.selenium.wsgi.TestCase):

    layer = test_layer

    def test_wsgi_layer(self):
        self.assertTrue(self.layer.thread.isAlive)

    def test_simple_app(self):
        self.selenium.open('/')
        self.selenium.assertTextPresent('Hello from javascript')
