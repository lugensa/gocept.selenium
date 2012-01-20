#############################################################################
#
# Copyright (c) 2010-2012 Zope Foundation and Contributors.
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

import os
import unittest
import gocept.selenium.static


class TestStaticFilesTestCase(unittest.TestCase):

    def setUp(self):
        self.testlayer = gocept.selenium.static.static_files_layer
        self.testlayer.setUp()

    def tearDown(self):
        self.testlayer.tearDown()

    def test_documentroot(self):
        self.assertTrue(self.testlayer.documentroot.startswith('/tmp'))

    def test_documentroot_initially_empty(self):
        documentroot = self.testlayer.documentroot
        self.assertEqual([], os.listdir(self.testlayer.documentroot))
        open(os.path.join(documentroot, 'foo.txt'), 'w').write('Hello World!')
        self.assertEqual(
            ['foo.txt'], os.listdir(self.testlayer.documentroot))

    def test_documentroot_empty_except_for_favicon_after_testsetup(self):
        documentroot = self.testlayer.documentroot
        self.assertEqual([], os.listdir(self.testlayer.documentroot))
        open(os.path.join(documentroot, 'bar.txt'), 'w').write('Hello World!')
        self.assertEqual(
            ['bar.txt'], os.listdir(self.testlayer.documentroot))
        self.testlayer.testSetUp()
        self.assertEqual(
            ['favicon.ico'], os.listdir(self.testlayer.documentroot))

    def test_server_startup_shutdown(self):
        self.assertTrue(self.testlayer.server_thread.isAlive())
        self.testlayer.stop_server()
        self.assertFalse(self.testlayer.server)
