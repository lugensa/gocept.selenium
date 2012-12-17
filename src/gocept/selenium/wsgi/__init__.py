#############################################################################
#
# Copyright (c) 2010-2012 Zope Foundation and Contributors.
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

from wsgiref.simple_server import WSGIRequestHandler
import gocept.httpserverlayer.wsgi
import gocept.selenium.base
import os
import unittest


class LogWSGIRequestHandler(WSGIRequestHandler):

    # Add conditional logging to handler.
    def log_request(self, *args):
        if 'GOCEPT_SELENIUM_VERBOSE_LOGGING' in os.environ:
            WSGIRequestHandler.log_request(self, *args)


class Layer(gocept.selenium.base.IntegrationBase,
            gocept.httpserverlayer.wsgi.Layer):

    request_handler_class = LogWSGIRequestHandler

    def __init__(self, application, *bases):
        self.wsgi_app = self.setup_wsgi_stack(application)
        name = self.make_layer_name(bases)
        # The name of the application class is used in order to help
        # the testrunner distinguish between layers with different
        # applications.
        name += '.' + application.__class__.__name__
        super(Layer, self).__init__(name=name, bases=bases)

    def setup_wsgi_stack(self, app):
        return app


class TestCase(gocept.selenium.base.TestCase, unittest.TestCase):
    """NOTE: MRO requires gocept.selenium.base.TestCase to come first,
    otherwise its setUp/tearDown is never called, since unittest.TestCase
    does not call super().
    """


class CleanerMiddleware(object):
    """Fix problems between WSGI server and middlewares."""

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        # wsgiref.simple_server.ServerHandler.setup_environ adds
        # 'CONTENT_LENGTH' key to environ which has the value '', but
        # repoze.retry.Retry.__call__ 1.0. expects the value to be
        # convertable to `int` See http://bugs.repoze.org/issue171.
        if environ.get('CONTENT_LENGTH') == '':
            del environ['CONTENT_LENGTH']

        # gocept.selenium uses wsgiref but
        # wsgiref.simple_server.ServerHandler.start_response bails when it
        # sees the 'Connection' header, so we frankly remove it here:
        def clean_start_response(status, headers, exc_info):
            headers = [(k, v) for (k, v) in headers if k != 'Connection']
            return start_response(status, headers, exc_info)

        return self.app(environ, clean_start_response)
