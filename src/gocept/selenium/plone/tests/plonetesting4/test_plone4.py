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

import gocept.selenium.zope2
import gocept.selenium.tests.isolation
from gocept.selenium.zope2 import plonetesting
from gocept.selenium.tests import isolation_layer

PLONE_ISOLATION = FunctionalTesting(
    bases=(isolation_layer.ISOLATION, PLONE_FIXTURE),
    name="gocept.selenium:PloneIsolation")

PLONE_SELENIUM = plone.testing.Layer(
    bases=(plonetesting.SELENIUM, PLONE_ISOLATION,),
    name="gocept.selenium:Plone4")


class Plone4Tests(gocept.selenium.tests.isolation.IsolationTests,
                 plonetesting.TestCase):

    layer = PLONE_SELENIUM

    def test_plone_login(self):
        sel = self.selenium
        sel.open('/plone')
        sel.click('link=Log in')
        sel.waitForElementPresent('name=__ac_name')
        sel.type('name=__ac_name', SITE_OWNER_NAME)
        sel.type('name=__ac_password', SITE_OWNER_PASSWORD)
        sel.click('name=submit')
        sel.waitForPageToLoad()
        sel.assertTextPresent(SITE_OWNER_NAME)


def test_suite():
    return unittest.makeSuite(Plone4Tests)
