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
import Testing.ZopeTestCase.ZopeLite
import Testing.ZopeTestCase.connections
import Testing.ZopeTestCase.sandbox
import Testing.ZopeTestCase.utils
import Zope2
import gocept.selenium.base
import random
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
        # five threads
        self.startZServer()
        super(Layer, self).setUp()

    @property
    def host(self):
        return Testing.ZopeTestCase.utils._Z2HOST

    @property
    def port(self):
        return Testing.ZopeTestCase.utils._Z2PORT

    def startZServer(self):
        if self.host is not None:
            return
        host = '127.0.0.1'
        port = random.choice(range(55000, 55500))
        from Testing.ZopeTestCase.threadutils import setNumberOfThreads
        setNumberOfThreads(5)
        from Testing.ZopeTestCase.threadutils import QuietThread, zserverRunner
        t = QuietThread(target=zserverRunner, args=(host, port, None))
        t.setDaemon(1)
        t.start()
        time.sleep(0.1)  # Sandor Palfy

        Testing.ZopeTestCase.utils._Z2HOST = host
        Testing.ZopeTestCase.utils._Z2PORT = port

    def tearDown(self):
        Lifetime.shutdown(0, fast=1)
        super(Layer, self).tearDown()

    def switch_db(self):
        # Nothing to do, we rely on ZopeLiteLayer et. al.
        pass


class TestCase(gocept.selenium.base.TestCase,
               Testing.ZopeTestCase.FunctionalTestCase):

    layer = Layer(*BASE_LAYERS)

    def _app(self):
        # Testing.ZopeTestCase.Sandbox handling of the DemoStorage change is a
        # little... crude:
        #
        # ZApplicationWrapper is instantiated with a DB from
        # Testing/custom_zodb, but that is never used later on, but Sandbox
        # passes in the connection (to the current DB) to use instead.
        # While this is fine for "normal" tests (using testbrowser or whatnot),
        # this means that there only ever is one single ZODB connection, even
        # among multiple threads -- which clearly is not what we want.
        #
        # Thus, this rewrite of the upstream method, that properly changes the
        # DB in ZApplicationWrapper, yielding a new connection upon each
        # traversal.
        Zope2.startup()
        db, aname, version = Zope2.bobo_application._stuff
        db = Testing.ZopeTestCase.ZopeLite.sandbox()
        Zope2.bobo_application._stuff = db, aname, version
        app = Zope2.bobo_application()
        Testing.ZopeTestCase.sandbox.AppZapper().set(app)
        app = Testing.ZopeTestCase.utils.makerequest(app)
        Testing.ZopeTestCase.connections.register(app)
        return app
