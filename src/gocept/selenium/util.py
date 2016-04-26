#############################################################################
#
# Copyright (c) 2012 Zope Foundation and Contributors.
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

import distutils.versionpredicate
import httpagentparser
import re


class skipUnlessBrowser(object):

    def __init__(self, name, version=None):
        self.required_name = name
        self.required_version = version

    def __call__(self, f):
        if isinstance(f, type):
            raise ValueError('%s cannot be used as class decorator' %
                             self.__class__.__name__)

        def test(test_case, *args, **kw):
            self.skip_unless_requirements_met(test_case)
            return f(test_case, *args, **kw)
        return test

    def eval(self, test_case, code):
        selenium = test_case.layer['seleniumrc']
        eval_js = getattr(selenium, 'get_eval', None)
        if eval_js is None:
            eval_js = selenium.execute_script
            code = 'return ' + code
        return eval_js(code)

    def skip_unless_requirements_met(self, test_case):
        user_agent_string = self.eval(test_case, 'window.navigator.userAgent')
        if user_agent_string[0] == user_agent_string[-1] == '"':
            user_agent_string = user_agent_string[1:-1]
        agent = httpagentparser.detect(user_agent_string)
        if re.match(self.required_name, agent['browser']['name']) is None:
            test_case.skipTest('Require browser %s, but have %s.' % (
                self.required_name, agent['browser']['name']))
        if self.required_version:
            requirement = distutils.versionpredicate.VersionPredicate(
                'Browser (%s)' % self.required_version)
            skip = not requirement.satisfied_by(
                str(agent['browser']['version']))
            if skip:
                test_case.skipTest('Require %s%s, got %s %s' % (
                    self.required_name, self.required_version,
                    agent['browser']['name'], agent['browser']['version']))
