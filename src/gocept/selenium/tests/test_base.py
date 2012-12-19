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

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class LayerTest(unittest.TestCase):

    def test_connection_refused_should_raise_readable_error(self):
        import gocept.selenium.base
        layer = gocept.selenium.base.Layer()
        layer.port = 1234  # doesn't matter, but > 0
        layer._port = 0  # reserved by IANA
        try:
            layer.setUp()
        except Exception, e:
            self.assertTrue(str(e).startswith(
                'Failed to connect to Selenium RC'))
