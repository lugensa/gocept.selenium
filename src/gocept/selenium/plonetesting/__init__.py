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

import gocept.selenium.base
import plone.testing
import plone.testing.z2
import unittest


# XXX it would be nicer to reuse plone.testing.z2.ZSERVER_FIXTURE,
# but we can't since we want to be able to override host/port via the
# mechanisms exposed by gocept.selenium.base.Layer
ZSERVER = plone.testing.z2.ZServer()


class Layer(gocept.selenium.base.Layer, plone.testing.Layer):

    defaultBases = (ZSERVER, plone.testing.z2.FUNCTIONAL_TESTING)

    def __init__(self, *args, **kw):
        # we can't use super, since our base classes are not built for multiple
        # inheritance (they don't consistently call super themselves, so parts
        # of the hierarchy might be missed).
        #
        # plone.testing.Layer has noops for everything except __init__, so this
        # only matters here.

        gocept.selenium.base.Layer.__init__(self)
        plone.testing.Layer.__init__(self, *args, **kw)
        ZSERVER.host = self.host
        ZSERVER.port = self.port

    def testSetUp(self):
        super(Layer, self).testSetUp()
        # conform to the plone.testing contract that layers expose interesting
        # stuff via getitem
        self['selenium'] = self.selenium


SELENIUM = Layer()


class TestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    @property
    def selenium(self):
        return self.layer['selenium']

    def getRootFolder(self):
        return self.layer['app']
