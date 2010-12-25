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

import Testing.ZopeTestCase
import Zope2
import gocept.selenium.tests.isolation
import gocept.selenium.zope2
import unittest

Testing.ZopeTestCase.installProduct('Five')


class Zope2Tests(gocept.selenium.tests.isolation.IsolationTests,
                 gocept.selenium.zope2.TestCase):

    def getRootFolder(self):
        return self.app

    def getDatabase(self):
        db, aname, version = Zope2.bobo_application._stuff
        return db


def test_suite():
    return unittest.makeSuite(Zope2Tests)
