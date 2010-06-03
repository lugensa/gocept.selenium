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

import os
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest

import gocept.selenium.base

class StaticFilesLayer(gocept.selenium.base.Layer):

    host = 'localhost'
    port = 5698

    def setUp(self):
        super(StaticFilesLayer, self).setUp()
        self.server = None
        self.documentroot = tempfile.mkdtemp(suffix='tha.selenium.staticfiles')
        self.start_server()

    def start_server(self):
        cmd = [sys.executable, '-m', 'SimpleHTTPServer', str(self.port)]
        self.server = subprocess.Popen(cmd, cwd=self.documentroot)
        # Wait a little as it sometimes takes a while to
        # get the server started.
        time.sleep(0.25)

    def stop_server(self):
        if self.server is None:
            return
        try:
            # Kill the previously started SimpleHTTPServer process.
            os.kill(self.server.pid, signal.SIGKILL)
            self.server = None
        except OSError, e:
            print 'Could not kill process, do so manually. Reason:\n' + str(e)

    def tearDown(self):
        # Clean up after our behinds.
        self.stop_server()
        shutil.rmtree(self.documentroot)

    def switch_db(self):
        # Part of the gocept.selenium test layer contract. We use the
        # hook to clear out all the files from the documentroot.
        shutil.rmtree(self.documentroot)
        self.documentroot = tempfile.mkdtemp(suffix='doctree.tinydocbook')

static_files_layer = StaticFilesLayer()

class StaticFilesTestCase(gocept.selenium.base.TestCase, unittest.TestCase):

    layer = static_files_layer

    def setUp(self):
        super(StaticFilesTestCase, self).setUp()
        self.documentroot = self.layer.documentroot
