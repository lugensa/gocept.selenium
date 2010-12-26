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

import gocept.selenium.tests.isolation.views
import grok


class App(grok.Model):
    pass


class Index(grok.View):

    def render(self):
        return '''<html><body>Hello from grok</body></html>'''


class DelegatingView(grok.View):
    # delegates actual functionality to the common isolation fixture, but lets
    # us register the views grok-style

    grok.context(object)

    def render(self):
        view = getattr(
            gocept.selenium.tests.isolation.views, self.__class__.__name__)()
        view.context = self.context
        return view()


class Set(DelegatingView):

    grok.name('set.html')


class Get(DelegatingView):

    grok.name('get.html')


class IncrementVolatile(DelegatingView):

    grok.name('inc-volatile.html')
