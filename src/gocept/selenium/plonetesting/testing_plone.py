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

import gocept.selenium.plonetesting
import gocept.selenium.plonetesting.testing
import plone.app.testing.layers
import plone.testing


layer = plone.testing.Layer(
    bases=(gocept.selenium.plonetesting.testing.layer,
           plone.app.testing.layers.PLONE_FIXTURE),
    name='Isolation')


selenium_layer = plone.testing.Layer(
    bases=(layer, gocept.selenium.plonetesting.SELENIUM),
    name='layer')
