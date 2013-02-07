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

import gocept.httpserverlayer.static
import gocept.selenium.seleniumrc
import unittest


class StaticFilesLayer(gocept.selenium.seleniumrc.IntegrationBase,
                       gocept.httpserverlayer.static.Layer):

    def __init__(self):
        super(StaticFilesLayer, self).__init__(
            name='StaticFilesLayer', bases=())

static_files_layer = StaticFilesLayer()


class TestCase(gocept.selenium.seleniumrc.TestCase, unittest.TestCase):

    layer = static_files_layer

    @property
    def documentroot(self):
        return self.layer['documentroot']
