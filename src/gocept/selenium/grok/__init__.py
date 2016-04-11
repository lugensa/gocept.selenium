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

from zope.app.appsetup.testlayer import ZODBLayer
import gocept.httpserverlayer.wsgi
import gocept.httpserverlayer.zopeappwsgi
import gocept.selenium.seleniumrc
import os
import plone.testing
import sys
import unittest


class Layer(ZODBLayer, plone.testing.Layer):

    # This is rather kludgy. To keep the public API of calling
    # grok.Layer(package), we need to bundle four different things here.
    # Also, we can't use super, since our base classes don't consistently call
    # super themselves.
    #
    # See an example of the recommended way of setting this up in
    # gocept.httpserverlayer.zopeappwsgi.testing

    # we can't inherit from IntegrationBase, since we need more control here.
    host = os.environ.get('GOCEPT_SELENIUM_APP_HOST', 'localhost')
    port = int(os.environ.get('GOCEPT_SELENIUM_APP_PORT', 0))

    def __init__(self, package, *args, **kw):
        ZODBLayer.__init__(self, package, *args, **kw)
        plone.testing.Layer.__init__(
            self, name='Layer(%s)' % package.__name__,
            module=sys._getframe(1).f_globals['__name__'])

        self.WSGI_LAYER = gocept.httpserverlayer.zopeappwsgi.Layer(
            name='IntegratedWSGILayer', bases=[self])
        self.HTTP_LAYER = gocept.httpserverlayer.wsgi.Layer(
            name='IntegratedHTTPLayer', bases=[self.WSGI_LAYER])
        self.HTTP_LAYER['http_host'] = self.host
        self.HTTP_LAYER['http_port'] = self.port
        self.SELENIUM_LAYER = gocept.selenium.seleniumrc.Layer(
            name='IntegratedSeleniumLayer', bases=[self.HTTP_LAYER])

    def setUp(self):
        ZODBLayer.setUp(self)
        self['zodbDB'] = self.db
        self.WSGI_LAYER.setUp()
        self.HTTP_LAYER.setUp()
        self.SELENIUM_LAYER.setUp()

    def tearDown(self):
        self.SELENIUM_LAYER.tearDown()
        self.HTTP_LAYER.tearDown()
        self.WSGI_LAYER.tearDown()
        ZODBLayer.tearDown(self)

    def testSetUp(self):
        ZODBLayer.testSetUp(self)
        self['zodbDB'] = self.db
        self.WSGI_LAYER.testSetUp()
        self.HTTP_LAYER.testSetUp()
        self.SELENIUM_LAYER.testSetUp()
        self['selenium'] = self.SELENIUM_LAYER['selenium']


class TestCase(gocept.selenium.seleniumrc.TestCase, unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.getRootFolder = self.layer.getRootFolder
