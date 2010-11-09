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
import SimpleHTTPServer
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import urllib

import gocept.selenium.base

_suffix = 'gocept.selenium.static'


class StaticFileRequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    # The documentroot is set on the class just before passing the class on
    # to the BaseHTTPServer.HTTPServer.
    documentroot = None

    def translate_path(self, path):
        # We subclass SimpleHTTPRequestHandler as it is dependent on
        # the cwd. We however want to inject a different path as the
        # "documentroot".
        # The rest of the method's implementation is copied verbatim from
        # SimpleHTTPServer.SimpleHTTPRequestHandler.
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)

        path = self.documentroot
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def log_request(self, *args):
        pass


class HTTPServer(BaseHTTPServer.HTTPServer):

    _continue = True

    def serve_until_shutdown(self):
        while self._continue:
            self.handle_request()

    def shutdown(self):
        self._continue = False
        urllib.urlopen('http://%s:%s/' % (self.server_name, self.server_port))
        self.server_close()


class StaticFilesLayer(gocept.selenium.base.Layer):

    host = 'localhost'
    port = 5698

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

    def switch_db(self):
        # Part of the gocept.selenium test layer contract. We use the
        # hook to clear out all the files from the documentroot.
        paths = os.listdir(self.documentroot)
        for path in paths:
            fullpath = os.path.join(self.documentroot, path)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
                continue
            os.remove(fullpath)


static_files_layer = StaticFilesLayer()


class StaticFilesTestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    layer = static_files_layer

    def setUp(self):
        super(StaticFilesTestCase, self).setUp()
        self.documentroot = self.layer.documentroot
