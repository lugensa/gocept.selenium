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

import gocept.selenium.plonetesting
import gocept.selenium.plonetesting.testing
import gocept.selenium.tests.isolation
import unittest


class Zope2Tests(gocept.selenium.tests.isolation.IsolationTests,
                 gocept.selenium.plonetesting.testing.IsolationTestHelper,
                 gocept.selenium.plonetesting.TestCase):

    layer = gocept.selenium.plonetesting.testing.selenium_layer


def test_suite():
    return unittest.makeSuite(Zope2Tests)
