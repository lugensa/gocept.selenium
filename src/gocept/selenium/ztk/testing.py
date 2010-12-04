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

import gocept.selenium.ztk
import pkg_resources
import zope.app.testing.functional

zcml_layer = zope.app.testing.functional.ZCMLLayer(
    pkg_resources.resource_filename(
        'gocept.selenium.ztk.tests', 'ftesting.zcml'),
    __name__, 'zcml_layer', allow_teardown=True)

selenium_layer = gocept.selenium.ztk.Layer(zcml_layer)


class TestCase(gocept.selenium.ztk.TestCase):

    layer = selenium_layer
