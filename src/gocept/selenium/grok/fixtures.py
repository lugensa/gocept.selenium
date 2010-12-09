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

import grok


class App(grok.Model):
    pass


class Index(grok.View):

    def render(self):
        return '''<html><body>Hello from grok</body></html>'''


class Set(grok.View):
    grok.name('set.html')
    grok.context(object)

    def render(self):
        self.context.foo = 1
        return u'setting done'


class Get(grok.View):
    grok.name('get.html')
    grok.context(object)

    def render(self):
        return str(getattr(self.context, 'foo', 0))
