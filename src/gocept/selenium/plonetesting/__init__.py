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

import gocept.httpserverlayer.plonetestingz2
import gocept.selenium.seleniumrc
import unittest


class Layer(gocept.selenium.seleniumrc.IntegrationBase,
            gocept.httpserverlayer.plonetestingz2.Layer):
    pass


SELENIUM = Layer()


class TestCase(gocept.selenium.seleniumrc.TestCase, unittest.TestCase):
    """NOTE: MRO requires gocept.selenium.seleniumrc.TestCase to come first,
    otherwise its setUp/tearDown is never called, since unittest.TestCase
    does not call super().
    """

    @property
    def selenium(self):
        return self.layer['selenium']

    def getRootFolder(self):
        return self.layer['app']
