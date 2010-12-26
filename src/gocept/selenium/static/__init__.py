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

import BaseHTTPServer
import os
import os.path
import posixpath
import shutil
from SimpleHTTPServer import SimpleHTTPRequestHandler
import tempfile
import threading
import time
import unittest
import urllib

import gocept.selenium.base

_suffix = 'gocept.selenium.static'


class StaticFileRequestHandler(SimpleHTTPRequestHandler):

    # The documentroot is set on the class just before passing the class on
    # to the BaseHTTPServer.HTTPServer.
    documentroot = None

    def translate_path(self, path):
        # We subclass SimpleHTTPRequestHandler as it is dependent on
        # the cwd. We however want to inject a different path as the
        # "documentroot".
        # The rest of the method's implementation is copied verbatim from
        # SimpleHTTPServer.SimpleHTTPRequestHandler.
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)

        path = self.documentroot
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    # Add conditional logging to handler.
    def log_request(self, *args):
        if 'GOCEPT_SELENIUM_VERBOSE_LOGGING' in os.environ:
            SimpleHTTPRequestHandler.log_request(self, *args)


class HTTPServer(BaseHTTPServer.HTTPServer):

    _continue = True

    def serve_until_shutdown(self):
        while self._continue:
            self.handle_request()

    def shutdown(self):
        self._continue = False
        # We fire a last request at the server in order to take it out of the
        # while loop in `self.serve_until_shutdown`.
        try:
            urllib.urlopen('http://%s:%s/' % (self.server_name,
                                              self.server_port))
        except IOError:
            # If the server is already shut down, we receive a socket error,
            # which we ignore.
            pass
        self.server_close()


class StaticFilesLayer(gocept.selenium.base.Layer):

    def __init__(self):
        # we don't need any __bases__
        super(StaticFilesLayer, self).__init__()

    def setUp(self):
        super(StaticFilesLayer, self).setUp()
        self.server = None
        self.documentroot = tempfile.mkdtemp(suffix=_suffix)
        self.start_server()

    def start_server(self):
        StaticFileRequestHandler.documentroot = self.documentroot
        self.server = HTTPServer(
            (self.host, self.port), StaticFileRequestHandler)
        self.server_thread = threading.Thread(
            target=self.server.serve_until_shutdown)
        self.server_thread.daemon = True
        self.server_thread.start()
        # Wait a little as it sometimes takes a while to get the server
        # started.
        time.sleep(0.25)

    def stop_server(self):
        if self.server is None:
            return
        self.server.shutdown()
        self.server_thread.join()
        # Make the server really go away and give up the socket:
        self.server = None

    def tearDown(self):
        # Clean up after our behinds.
        self.stop_server()
        shutil.rmtree(self.documentroot)
        super(StaticFilesLayer, self).tearDown()

    def testSetUp(self):
        super(StaticFilesLayer, self).testSetUp()
        paths = os.listdir(self.documentroot)
        for path in paths:
            fullpath = os.path.join(self.documentroot, path)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
                continue
            os.remove(fullpath)
        # silence annoying 404s
        open(os.path.join(self.documentroot, 'favicon.ico'), 'w').close()


static_files_layer = StaticFilesLayer()


class TestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    layer = static_files_layer

    def setUp(self):
        super(TestCase, self).setUp()
        self.documentroot = self.layer.documentroot
