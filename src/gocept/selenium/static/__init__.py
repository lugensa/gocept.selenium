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

import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

import gocept.selenium.base

_suffix = 'gocept.selenium.static'


class StaticFilesLayer(gocept.selenium.base.Layer):

    host = 'localhost'
    port = 5698

    def setUp(self):
        super(StaticFilesLayer, self).setUp()
        self.server = None
        self.documentroot = tempfile.mkdtemp(suffix=_suffix)
        self.start_server()

    def start_server(self):
        cmd = [sys.executable, '-m', 'SimpleHTTPServer', str(self.port)]
        self.server = subprocess.Popen(cmd, cwd=self.documentroot)
        # Wait a little as it sometimes takes a while to get the server
        # started.
        time.sleep(0.25)

    def stop_server(self):
        if self.server is None:
            return
        self.server.kill()
        self.server = None

    def tearDown(self):
        # Clean up after our behinds.
        self.stop_server()
        shutil.rmtree(self.documentroot)
        super(StaticFilesLayer, self).tearDown()

    def switch_db(self):
        # Part of the gocept.selenium test layer contract. We use the
        # hook to clear out all the files from the documentroot.
        paths = os.listdir(self.documentroot)
        for path in paths:
            fullpath = os.path.join(self.documentroot, path)
            if os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
                continue
            os.remove(fullpath)


static_files_layer = StaticFilesLayer()


class StaticFilesTestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    layer = static_files_layer

    def setUp(self):
        super(StaticFilesTestCase, self).setUp()
        self.documentroot = self.layer.documentroot
