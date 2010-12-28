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
import unittest

from zope.app.appsetup.testlayer import ZODBLayer
import zope.app.wsgi

import gocept.selenium.selenese
import gocept.selenium.wsgi


class Layer(ZODBLayer, gocept.selenium.wsgi.Layer):

    # we can't use super, since our base classes are not built for multiple
    # inheritance (they don't consistently call super themselves, so parts of
    # the hierarchy might be missed)

    def __init__(self, *args, **kw):
        # since the request factory class is only a parameter default of
        # WSGIPublisherApplication and not easily accessible otherwise, we fake
        # it into creating a requestFactory instance, so we can read the class
        # off of that in testSetUp()
        fake_db = object()
        gocept.selenium.wsgi.Layer.__init__(
            self, zope.app.wsgi.WSGIPublisherApplication(fake_db))
        ZODBLayer.__init__(self, *args, **kw)

    def setUp(self):
        ZODBLayer.setUp(self)
        gocept.selenium.wsgi.Layer.setUp(self)

    def tearDown(self):
        gocept.selenium.wsgi.Layer.tearDown(self)
        ZODBLayer.tearDown(self)

    def testSetUp(self):
        gocept.selenium.wsgi.Layer.testSetUp(self)
        ZODBLayer.testSetUp(self)
        # tell the publisher to use ZODBLayer's current database
        factory = type(self.application.requestFactory)
        self.application.requestFactory = factory(self.db)


class TestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        self.getRootFolder = self.layer.getRootFolder
