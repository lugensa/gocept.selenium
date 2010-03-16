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

ENSURE_ORDER = False


class IsolationTests(object):

    def test_0_set(self):
        global ENSURE_ORDER
        self.selenium.open('http://%s/set.html' % self.selenium.server)
        self.selenium.open('http://%s/get.html' % self.selenium.server)
        self.selenium.assertBodyText('1')
        ENSURE_ORDER = True

    def test_1_get(self):
        global ENSURE_ORDER
        self.assertEquals(ENSURE_ORDER, True,
                          'Set test was not run before get test')
        self.selenium.open('http://%s/get.html' % self.selenium.server)
        self.selenium.assertNotBodyText('1')
        ENSURE_ORDER = False
