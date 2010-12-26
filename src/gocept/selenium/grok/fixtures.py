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

import gocept.selenium.tests.fixture.dummy
import grok


class App(grok.Model):
    pass


class Index(grok.View):

    def render(self):
        return '''<html><body>Hello from grok</body></html>'''


# delegate to the common isolation fixture, but register the views grok-style

class Set(grok.View):
    grok.name('set.html')
    grok.context(object)

    def render(self):
        view = gocept.selenium.tests.fixture.dummy.Set()
        view.context = self.context
        return view()


class Get(grok.View):
    grok.name('get.html')
    grok.context(object)

    def render(self):
        view = gocept.selenium.tests.fixture.dummy.Get()
        view.context = self.context
        return view()


class IncrementVolatile(grok.View):
    grok.name('inc-volatile.html')
    grok.context(object)

    def render(self):
        view = gocept.selenium.tests.fixture.dummy.IncrementVolatile()
        view.context = self.context
        return view()
