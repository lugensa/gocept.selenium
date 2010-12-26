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

from Products.PloneTestCase.layer import PloneSiteLayer
import Products.PloneTestCase.PloneTestCase
import gocept.selenium.tests.isolation
import gocept.selenium.zope2
import gocept.selenium.zope2.testing
import unittest


Products.PloneTestCase.PloneTestCase.setupPloneSite(id='plone')


class PloneTests(gocept.selenium.tests.isolation.IsolationTests,
                 gocept.selenium.plone.TestCase):

    layer = gocept.selenium.zope2.Layer(
        PloneSiteLayer,
        gocept.selenium.zope2.testing.Layer)

    def getDatabase(self):
        return gocept.selenium.zope2.get_current_db()

    def test_plone_login(self):
        sel = self.selenium
        sel.open('/plone')
        sel.type('name=__ac_name', 'portal_owner')
        sel.type('name=__ac_password', 'secret')
        sel.click('name=submit')
        sel.waitForPageToLoad()
        sel.assertTextPresent('Welcome! You are now logged in.')


def test_suite():
    return unittest.makeSuite(PloneTests)
