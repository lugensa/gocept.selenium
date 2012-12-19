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

import gocept.selenium.webdriver

try:
    import unittest2 as unittest
except ImportError:
    import unittest


class LayerTest(unittest.TestCase):

    def test_connection_refused_should_raise_readable_error(self):
        layer = gocept.selenium.webdriver.Layer()
        layer['http_address'] = 'localhost:12345'
        layer._port = 4445  # default port is 4444
        try:
            layer.setUp()
        except Exception, e:
            self.assertIn('Failed to connect to Selenium server', str(e))
