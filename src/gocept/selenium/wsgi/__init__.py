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

import os
import unittest
import threading
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

import gocept.selenium.base
import gocept.selenium.selenese


class LogWSGIRequestHandler(WSGIRequestHandler):

    # Add conditional logging to handler.
    def log_request(self, *args):
        if 'GOCEPT_SELENIUM_VERBOSE_LOGGING' in os.environ:
            WSGIRequestHandler.log_request(self, *args)


class Layer(gocept.selenium.base.SaneLayer):

    application = None

    def setup_wsgi_stack(self, app):
        return app

    def setUp(self):
        gocept.selenium.base.SaneLayer.setUp(self)

        self.http = WSGIServer((self.host, self.port), LogWSGIRequestHandler)
        self.http.set_app(self.setup_wsgi_stack(self.application))

        self.thread = threading.Thread(target=self.http.serve_forever)
        self.thread.daemon = True
        self.thread.start()

    def tearDown(self):
        self.http.shutdown()
        self.thread.join()
        # Make the server really go away and give up the socket:
        self.http = None
        gocept.selenium.base.SaneLayer.tearDown(self)


class TestCase(unittest.TestCase):

    def setUp(self):
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer.selenium, self)
