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

# BBB
from gocept.httpserverlayer.wsgi import FixupMiddleware as CleanerMiddleware  # noqa
from wsgiref.simple_server import WSGIRequestHandler
import gocept.httpserverlayer.wsgi
import gocept.selenium.webdriver
import os
import unittest


class LogWSGIRequestHandler(WSGIRequestHandler):

    # Add conditional logging to handler.
    def log_request(self, *args):
        if 'GOCEPT_SELENIUM_VERBOSE_LOGGING' in os.environ:
            WSGIRequestHandler.log_request(self, *args)


class Layer(gocept.selenium.webdriver.IntegrationBase,
            gocept.httpserverlayer.wsgi.Layer):

    request_handler_class = LogWSGIRequestHandler

    def __init__(self, application, *bases):
        name = self.make_layer_name(bases)
        # The name of the application class is used in order to help
        # the testrunner distinguish between layers with different
        # applications.
        name += '.' + application.__class__.__name__
        super().__init__(name=name, bases=bases)
        self.wsgi_app = self.setup_wsgi_stack(application)

    def setup_wsgi_stack(self, app):
        return app


class TestCase(gocept.selenium.webdriver.WebdriverSeleneseTestCase,
               unittest.TestCase):
    """Webdriver test case with unittest assertions"""
