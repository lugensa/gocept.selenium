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
from zope.app.wsgi import WSGIPublisherApplication
from zope.app.publication.httpfactory import HTTPPublicationRequestFactory

import gocept.selenium.selenese
import gocept.selenium.wsgi


class Layer(ZODBLayer, gocept.selenium.wsgi.Layer):

    application = WSGIPublisherApplication()

    def setUp(self):
        ZODBLayer.setUp(self)
        gocept.selenium.wsgi.Layer.setUp(self)

    def tearDown(self):
        gocept.selenium.wsgi.Layer.tearDown(self)
        ZODBLayer.tearDown(self)

    def testSetUp(self):
        # A fresh database is created in the setup of the ZODBLayer:
        ZODBLayer.testSetUp(self)
        # We tell the publisher to use this new database:
        self.application.requestFactory = \
            HTTPPublicationRequestFactory(self.db)


class TestCase(unittest.TestCase):

    def setUp(self):
        self.selenium = gocept.selenium.selenese.Selenese(
            self.layer.selenium, self)
        self.getRootFolder = self.layer.getRootFolder
