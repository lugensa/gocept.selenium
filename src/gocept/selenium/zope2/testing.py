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

import Products.Five.zcml
import Zope2
import gocept.selenium.tests.isolation


class Layer(object):

    @classmethod
    def setUp(cls):
        Products.Five.zcml.load_config(
            'configure.zcml', package=gocept.selenium.tests.isolation)


# required for Zope2 >= 2.12
class FiveLayer(object):

    @classmethod
    def setUp(cls):
        Products.Five.zcml.load_config(
            'configure.zcml', package=Products.Five)


def get_current_db():
    """helper for gocept.selenium.tests.isolation"""
    return Zope2.bobo_application._stuff[0]
