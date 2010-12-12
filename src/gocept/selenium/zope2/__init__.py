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

import Lifetime
import Testing.ZopeTestCase
import Testing.ZopeTestCase.utils
import gocept.selenium.base
import time


try:
    # Zope 2 >= 2.11
    import Testing.ZopeTestCase.layer
    BASE_LAYERS = (Testing.ZopeTestCase.layer.ZopeLiteLayer, )
except ImportError:
    # Zope 2 < 2.11
    BASE_LAYERS = ()


class Layer(gocept.selenium.base.Layer):

    def setUp(self):
        self.startZServer()
        super(Layer, self).setUp()

    def startZServer(self):
        from Testing.ZopeTestCase.threadutils import setNumberOfThreads
        setNumberOfThreads(5)
        from Testing.ZopeTestCase.threadutils import QuietThread, zserverRunner
        t = QuietThread(
            target=zserverRunner, args=(self.host, self.port, None))
        t.setDaemon(1)
        t.start()
        time.sleep(0.1)  # Sandor Palfy

        Testing.ZopeTestCase.utils._Z2HOST = self.host
        Testing.ZopeTestCase.utils._Z2PORT = self.port

    def tearDown(self):
        Lifetime.shutdown(0, fast=1)
        super(Layer, self).tearDown()


class TestCase(gocept.selenium.base.TestCase,
               Testing.ZopeTestCase.FunctionalTestCase):

    layer = Layer(*BASE_LAYERS)
