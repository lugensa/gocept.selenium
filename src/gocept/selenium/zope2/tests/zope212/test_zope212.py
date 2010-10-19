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
import gocept.selenium.zope2
from gocept.selenium.zope2 import testing
from gocept.selenium.zope2 import BASE_LAYERS
import gocept.selenium.tests.isolation
import Testing.ZopeTestCase

Testing.ZopeTestCase.installProduct('Five')


class Zope212Tests(gocept.selenium.tests.isolation.IsolationTests,
                 gocept.selenium.zope2.TestCase):

    layer = gocept.selenium.zope2.Layer(testing.fixtureLayer, *BASE_LAYERS)


def test_suite():
    return unittest.makeSuite(Zope212Tests)
