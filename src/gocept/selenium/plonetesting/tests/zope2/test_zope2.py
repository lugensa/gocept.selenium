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
import gocept.selenium.tests.isolation
from gocept.selenium.plonetesting.tests import isolation_layer


ZOPE2_ISOLATION = plone.testing.Layer(
    bases=(plonetesting.SELENIUM, isolation_layer.FUNCTIONAL_ISOLATION,),
    name="gocept.selenium:Zope2")


class Zope2Tests(unittest.TestCase,
    gocept.selenium.tests.isolation.IsolationTests):

    layer = ZOPE2_ISOLATION

    @property
    def selenium(self):
        # property needed to reuse IsolationTests without touching them
        # should not be needed in usual tests; see plone4 tests for example
        return self.layer['selenese']


def test_suite():
    return unittest.makeSuite(Zope2Tests)
