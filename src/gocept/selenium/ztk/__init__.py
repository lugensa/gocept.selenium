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
import threading
import zope.app.server.main
import zope.app.server.wsgi
import zope.app.testing.functional
import zope.app.wsgi


class Layer(gocept.selenium.base.Layer):

    # Hostname and port of the Zope webserver
    host = 'localhost'
    port = 8087

    def setUp(self):
        task_dispatcher = ThreadedTaskDispatcher()
        task_dispatcher.setThreadCount(1)
        db = zope.app.testing.functional.FunctionalTestSetup().db
        self.http = SwitchableDBServerType.create(
            'WSGI-HTTP', task_dispatcher, db, port=self.port)
        thread = threading.Thread(target=zope.app.server.main.run)
        thread.setDaemon(True)
        thread.start()

        super(Layer, self).setUp()

    def switch_db(self):
        """switches the HTTP-server's database to the currently active
        DemoStorage"""
        db = zope.app.testing.functional.FunctionalTestSetup().db
        self.http.application.set_db(db)


class TestCase(gocept.selenium.base.TestCase,
               zope.app.testing.functional.FunctionalTestCase):
    # note: MRO requires the gocept.selenium.base.TestCase to come first,
    # otherwise setUp/tearDown happens in the wrong order
    pass


class SwitchableDBApplication(zope.app.wsgi.WSGIPublisherApplication):

    def __init__(self, *args, **kw):
        self.db = kw.get('db', None)
        super(SwitchableDBApplication, self).__init__(*args, **kw)

    def __call__(self, environ, start_response):
        if self.db is not None:
            factory = type(self.requestFactory)
            self.requestFactory = factory(self.db)
        return super(SwitchableDBApplication, self).__call__(
            environ, start_response)

    def set_db(self, db):
        self.db = db


SwitchableDBServerType = zope.app.server.wsgi.ServerType(
    zope.server.http.wsgihttpserver.WSGIHTTPServer,
    SwitchableDBApplication,
    zope.server.http.commonaccesslogger.CommonAccessLogger,
    8087, True) # The port number here is just the default value
