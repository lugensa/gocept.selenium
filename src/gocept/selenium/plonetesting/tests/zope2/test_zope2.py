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
from gocept.selenium import plonetesting
from gocept.selenium.plonetesting.tests import isolation


ZOPE2_ISOLATION = plone.testing.Layer(
    bases=(plonetesting.SELENIUM, isolation.FUNCTIONAL_ISOLATION,),
    name="gocept.selenium:Zope2")


class Zope2Tests(unittest.TestCase,
    isolation.IsolationTests):

    layer = ZOPE2_ISOLATION


def test_suite():
    return unittest.makeSuite(Zope2Tests)
