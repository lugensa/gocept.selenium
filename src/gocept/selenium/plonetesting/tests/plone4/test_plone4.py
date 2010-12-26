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
from gocept.selenium import plonetesting
from gocept.selenium.plonetesting.tests import isolation_layer
from gocept.selenium.plonetesting.tests.zope2.test_zope2 import Zope2Tests

PLONE_ISOLATION = FunctionalTesting(
    bases=(isolation_layer.ISOLATION, PLONE_FIXTURE),
    name="gocept.selenium:PloneIsolation")

PLONE_SELENIUM = plone.testing.Layer(
    bases=(plonetesting.SELENIUM, PLONE_ISOLATION,),
    name="gocept.selenium:Plone4")


class Plone4Tests(unittest.TestCase,
    gocept.selenium.tests.isolation.IsolationTests):

    layer = PLONE_SELENIUM

    @property
    def selenium(self):
        # property needed to reuse IsolationTests without touching them
        # should not be needed in usual tests; see hereunder
        return self.layer['selenese']

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
    suite.addTest(unittest.makeSuite(Zope2Tests))
    return suite