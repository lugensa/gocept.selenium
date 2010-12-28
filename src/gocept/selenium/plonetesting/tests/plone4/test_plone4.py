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

import unittest

import plone.testing
from plone.testing.z2 import FunctionalTesting

from plone.app.testing.layers import PLONE_FIXTURE
from plone.app.testing.layers import SITE_OWNER_NAME
from plone.app.testing.layers import SITE_OWNER_PASSWORD

from gocept.selenium import plonetesting
from gocept.selenium.plonetesting import testing
import gocept.selenium.tests.isolation


PLONE_ISOLATION = FunctionalTesting(
    bases=(testing.ISOLATION, PLONE_FIXTURE),
    name="gocept.selenium:PloneIsolation")

PLONE_SELENIUM = plone.testing.Layer(
    bases=(plonetesting.SELENIUM, PLONE_ISOLATION,),
    name="gocept.selenium:Plone4")


class Plone4Tests(gocept.selenium.tests.isolation.IsolationTests,
                  testing.IsolationTestHelper,
                  plonetesting.TestCase):

    layer = PLONE_SELENIUM

    def test_plone_login(self):
        sel = self.layer['selenese']
        sel.open('/plone')
        sel.click('link=Log in')
        sel.waitForElementPresent('name=__ac_name')
        sel.type('name=__ac_name', SITE_OWNER_NAME)
        sel.type('name=__ac_password', SITE_OWNER_PASSWORD)
        sel.click('name=submit')
        sel.waitForPageToLoad()
        sel.assertTextPresent(SITE_OWNER_NAME)


def test_suite():
    suite = unittest.makeSuite(Plone4Tests)
    from gocept.selenium.plonetesting.tests.zope2 import test_zope2
    suite.addTest(test_zope2.test_suite())
    return suite
