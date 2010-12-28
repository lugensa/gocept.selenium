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
import gocept.selenium.plonetesting.testing_plone
import gocept.selenium.tests.isolation


class Plone3Tests(gocept.selenium.tests.isolation.IsolationTests,
                  gocept.selenium.plonetesting.testing.IsolationTestHelper,
                  gocept.selenium.plonetesting.TestCase):

    layer = gocept.selenium.plonetesting.testing_plone.selenium_layer

    def test_plone_login(self):
        sel = self.selenium
        sel.open('/plone')
        sel.type('name=__ac_name', SITE_OWNER_NAME)
        sel.type('name=__ac_password', SITE_OWNER_PASSWORD)
        sel.click('name=submit')
        sel.waitForPageToLoad()
        sel.assertTextPresent('Welcome! You are now logged in.')
