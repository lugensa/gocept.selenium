#############################################################################
#
# Copyright (c) 2010 Zope Foundation and Contributors.
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

from zope.configuration import xmlconfig

from plone.testing import Layer
from plone.testing.z2 import STARTUP
from plone.testing.z2 import FunctionalTesting

from gocept.selenium import plonetesting
import gocept.selenium.tests.isolation


class Isolation(Layer):

    defaultBases = (STARTUP, )

    def setUp(self):
        context = self['configurationContext']
        xmlconfig.file('testing.zcml', package=plonetesting.tests,
            context=context)

ISOLATION = Isolation()

FUNCTIONAL_ISOLATION = FunctionalTesting(bases=(ISOLATION,),
    name="gocept.selenium:FunctionalIsolation")


class IsolationTests(gocept.selenium.tests.isolation.IsolationTests):
    """plone.testing implementation of methods needed by base class"""

    @property
    def selenium(self):
        return self.layer['selenese']

    def getDatabase(self):
        return self.layer['zodbDB']

    def getRootFolder(self):
        return self.layer['app']
