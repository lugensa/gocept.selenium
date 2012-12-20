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

from SimpleHTTPServer import SimpleHTTPRequestHandler
import BaseHTTPServer
import gocept.selenium.seleniumrc
import os
import os.path
import posixpath
import shutil
import tempfile
import threading
import time
import unittest
import urllib

# work around Python 2.4 lack of absolute_import,
# see gocept.selenium.seleniumrc for details
plonetesting = __import__('plone.testing', {}, {}, [''])


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
            urllib.urlopen('http://%s:%s/' % (self.server_address[0],
                                              self.server_port))
        except IOError:
            # If the server is already shut down, we receive a socket error,
            # which we ignore.
            pass
        self.server_close()


class StaticFiles(plonetesting.Layer):

    host = 'localhost'
    port = 0  # choose automatically

    def setUp(self):
        self.server = None
        self['documentroot'] = tempfile.mkdtemp(suffix=_suffix)
        self.start_server()

    def start_server(self):
        StaticFileRequestHandler.documentroot = self['documentroot']
        self.server = HTTPServer(
            (self.host, self.port), StaticFileRequestHandler)
        self.server_thread = threading.Thread(
            target=self.server.serve_until_shutdown)
        self.server_thread.daemon = True
        self.server_thread.start()
        # Wait a little as it sometimes takes a while to get the server
        # started.
        time.sleep(0.25)
        self.port = self.server.server_port
        self['http_host'] = self.host
        self['http_port'] = self.port
        self['http_address'] = '%s:%s' % (self.host, self.port)

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
        shutil.rmtree(self['documentroot'])

    def testSetUp(self):
        paths = os.listdir(self['documentroot'])
        for path in paths:
            fullpath = os.path.join(self['documentroot'], path)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
                continue
            os.remove(fullpath)
        # silence annoying 404s
        open(os.path.join(self['documentroot'], 'favicon.ico'), 'w').close()

STATIC_FILES = StaticFiles()


class StaticFilesLayer(gocept.selenium.seleniumrc.IntegrationBase,
                       StaticFiles):

    def __init__(self):
        super(StaticFilesLayer, self).__init__(
            name='StaticFilesLayer', bases=())

    @property
    def documentroot(self):
        return self['documentroot']

static_files_layer = StaticFilesLayer()


class TestCase(gocept.selenium.seleniumrc.TestCase, unittest.TestCase):

    layer = static_files_layer

    @property
    def documentroot(self):
        return self.layer['documentroot']
