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

import gocept.selenium.tests.isolation
import gocept.selenium.ztk.testing
import zope.app.testing.functional


class ZTKTests(gocept.selenium.tests.isolation.IsolationTests,
               gocept.selenium.ztk.testing.TestCase):

    def getDatabase(self):
        return zope.app.testing.functional.FunctionalTestSetup().db
