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

import gocept.httpserverlayer.plonetestcase
import gocept.selenium.seleniumrc


class TestCase(gocept.selenium.seleniumrc.TestCase,
               gocept.httpserverlayer.plonetestcase.TestCase):
    """NOTE: MRO requires gocept.selenium.seleniumrc.TestCase to come first,
    otherwise its setUp/tearDown is never called, since unittest.TestCase
    does not call super().
    """
