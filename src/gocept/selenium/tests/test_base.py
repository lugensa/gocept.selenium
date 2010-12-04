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
import unittest


class LayerTest(unittest.TestCase):

    def test_connection_refused_should_raise_readable_error(self):
        layer = gocept.selenium.base.Layer()
        layer._port = 0 # reserved by IANA
        try:
            layer.setUp()
        except Exception, e:
            self.assertTrue(str(e).startswith(
                'Failed to connect to Selenium RC'))
