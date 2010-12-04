#############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
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

import gocept.selenium.base
import gocept.selenium.wsgi
import zope.app.testing.functional
import zope.app.wsgi


class Layer(gocept.selenium.wsgi.Layer):

    def __init__(self, *bases):
        # since the request factory class is only a parameter default of
        # WSGIPublisherApplication and not easily accessible otherwise, we fake
        # it into creating a requestFactory instance, so we can read the class
        # off of that in TestCase.setUp()
        fake_db = object()
        super(Layer, self).__init__(
            zope.app.wsgi.WSGIPublisherApplication(fake_db), *bases)


class TestCase(gocept.selenium.base.TestCase,
               zope.app.testing.functional.FunctionalTestCase):
    # note: MRO requires the gocept.selenium.base.TestCase to come first,
    # otherwise setUp/tearDown happens in the wrong order

    def setUp(self):
        # switches the HTTP-server's database to the currently active
        # DemoStorage (which is set by FunctionalTestCase)
        super(TestCase, self).setUp()
        db = zope.app.testing.functional.FunctionalTestSetup().db
        application = self.layer.application
        factory = type(application.requestFactory)
        application.requestFactory = factory(db)
