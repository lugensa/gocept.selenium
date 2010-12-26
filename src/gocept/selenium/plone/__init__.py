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

import Products.PloneTestCase.PloneTestCase
import gocept.selenium.base
import gocept.selenium.zope2


class TestCase(gocept.selenium.base.TestCase,
               gocept.selenium.zope2.SandboxPatch,
               Products.PloneTestCase.PloneTestCase.FunctionalTestCase):

    def getRootFolder(self):
        """forward API-compatibility with zope.app.testing"""
        return self.app
