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

from plone.app.testing.layers import SITE_OWNER_NAME
from plone.app.testing.layers import SITE_OWNER_PASSWORD
import gocept.selenium.plonetesting
import gocept.selenium.plonetesting.testing
import gocept.selenium.tests.isolation
import plone.app.testing.layers
import plone.testing
import plone.testing.z2
import unittest


layer = plone.testing.Layer(
    bases=(gocept.selenium.plonetesting.SELENIUM,
           gocept.selenium.plonetesting.testing.ISOLATION,
           plone.app.testing.layers.PLONE_FIXTURE),
    name='layer')


class Plone3Tests(gocept.selenium.tests.isolation.IsolationTests,
                  gocept.selenium.plonetesting.testing.IsolationTestHelper,
                  gocept.selenium.plonetesting.TestCase):

    layer = layer

    def test_plone_login(self):
        sel = self.selenium
        sel.open('/plone')
        sel.type('name=__ac_name', SITE_OWNER_NAME)
        sel.type('name=__ac_password', SITE_OWNER_PASSWORD)
        sel.click('name=submit')
        sel.waitForPageToLoad()
        sel.assertTextPresent('Welcome! You are now logged in.')


def test_suite():
    suite = unittest.makeSuite(Plone3Tests)
    from gocept.selenium.plonetesting.tests.zope2 import test_zope2
    suite.addTest(test_zope2.test_suite())
    return suite
