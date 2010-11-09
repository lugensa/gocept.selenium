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
import time
import urllib
import unittest
import threading
from wsgiref.simple_server import WSGIServer, WSGIRequestHandler

import gocept.selenium.base
import gocept.selenium.selenese


class LogWSGIRequestHandler(WSGIRequestHandler):

    # Add conditional logging to handler.
    def log_request(self, *args):
        if os.environ.has_key('GOCEPT_SELENIUM_VERBOSE_LOGGING'):
            WSGIRequestHandler.log_request(self, *args)


class WSGILayer(gocept.selenium.base.Layer):

    def __init__(self, application=None, *bases):
        super(WSGILayer, self).__init__(*bases)
        self.application = application

    def setUp(self):
        super(WSGILayer, self).setUp()

        self.http = WSGIServer((self.host, self.port), LogWSGIRequestHandler)
        self.http.set_app(self.application)

        self.thread = threading.Thread(target=self.http.serve_forever)
        self.thread.start()

    def tearDown(self):
        self.http.shutdown()
        self.thread.join()
        # Make the server really go away and give up the socket:
        self.http = None
        super(WSGILayer, self).tearDown()


class TestCase(unittest.TestCase):

    def setUp(self):
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer.selenium, self)
