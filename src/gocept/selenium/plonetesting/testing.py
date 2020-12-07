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

import gocept.selenium.plonetesting.tests
import plone.testing
import plone.testing.zope
import zope.configuration.xmlconfig


class Layer(plone.testing.Layer):

    defaultBases = (plone.testing.zope.STARTUP,)

    def setUp(self):
        zope.configuration.xmlconfig.file(
            'testing.zcml', package=gocept.selenium.plonetesting.tests,
            context=self['configurationContext'])


layer = Layer()


selenium_layer = plone.testing.Layer(
    bases=(layer, gocept.selenium.plonetesting.SELENIUM),
    name='layer')


class IsolationTestHelper:
    """
    plone.testing implementation of methods needed by common isolation tests
    """

    def getDatabase(self):
        return self.layer['zodbDB']
