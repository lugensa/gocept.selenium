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

import gocept.httpserverlayer.zope2testcase
import gocept.selenium.seleniumrc


class Layer(gocept.selenium.seleniumrc.IntegrationBase,
            gocept.httpserverlayer.zope2testcase.Layer):

    def __init__(self, *bases):
        name = self.make_layer_name(bases)
        super(Layer, self).__init__(name=name, bases=bases)


class TestCase(gocept.selenium.seleniumrc.TestCase,
               gocept.httpserverlayer.zope2testcase.TestCase):
    """NOTE: MRO requires gocept.selenium.seleniumrc.TestCase to come first,
    otherwise its setUp/tearDown is never called, since unittest.TestCase
    does not call super().
    """
