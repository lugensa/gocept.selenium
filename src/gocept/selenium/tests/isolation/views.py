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

import zope.security.proxy


class Set(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        c.foo = 1
        return 'setting done'


class Get(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        return str(getattr(c, 'foo', 0))


class Error(object):

    def __call__(Self):
        raise ValueError()


class IncrementVolatile(object):

    def __call__(self):
        c = zope.security.proxy.removeSecurityProxy(self.context)
        if hasattr(c, 'aq_base'):
            c = c.aq_base

        if not hasattr(c, '_v_counter'):
            c._v_counter = 0
        c._v_counter += 1
        return str(c._v_counter)
