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

from zope.server.taskthreads import ThreadedTaskDispatcher
import gocept.selenium.base
import gocept.selenium.selenese
import asyncore
import threading
import zope.app.server.wsgi
import zope.app.testing.functional
import zope.app.wsgi


class Layer(gocept.selenium.base.Layer):

    def setUp(self):
        task_dispatcher = ThreadedTaskDispatcher()
        task_dispatcher.setThreadCount(1)
        db = zope.app.testing.functional.FunctionalTestSetup().db
        self.http = zope.app.server.wsgi.http.create(
            'WSGI-HTTP', task_dispatcher, db, port=self.port)
        self.thread = threading.Thread(target=self.run_server)
        self.thread.setDaemon(True)
        self.thread.start()
        super(Layer, self).setUp()

    def tearDown(self):
        self.running = False
        self.thread.join()
        super(Layer, self).tearDown()

    def run_server(self):
        self.running = True
        while self.running:
            asyncore.poll(0.1)
        self.http.close()


class TestCase(gocept.selenium.base.TestCase,
               zope.app.testing.functional.FunctionalTestCase):
    # note: MRO requires the gocept.selenium.base.TestCase to come first,
    # otherwise setUp/tearDown happens in the wrong order

    def setUp(self):
        # switches the HTTP-server's database to the currently active
        # DemoStorage (which is set by FunctionalTestCase)
        super(TestCase, self).setUp()
        db = zope.app.testing.functional.FunctionalTestSetup().db
        application = self.layer.http.application
        assert isinstance(application, zope.app.wsgi.WSGIPublisherApplication)
        factory = type(application.requestFactory)
        application.requestFactory = factory(db)
