#!/usr/bin/env python
"""
Generate selenium test controller files from HTML selenium tests
"""

import re
import glob
from elementtree import HTMLTreeBuilder
from string import Template

template = Template('''
from seleniumtestcase import SeleniumTestCase
import unittest, time

class seltest_$testname(SeleniumTestCase):

$tests

def test_suite():
    return unittest.makeSuite(seltest_$testname)

if __name__ == "__main__":
    unittest.main()
''')

variable_regexp = re.compile('\$\{(?P<varname>\w*)\}')


def formatcommand(command, *args):
    if not command:
        return '' # Change this to raise an exception?

    arguments = []
    for arg in args:
        if not arg:
            continue
        matched = variable_regexp.match(arg)
        if matched is None:
            arguments.append('"%s"' % arg)
        else:
            arguments.append("self.getVar('%s')" % matched.group('varname'))
    return 'self.%s(%s)' % (command, ', '.join(arguments))

htmlparser = HTMLTreeBuilder.TreeBuilder()
tests = []
for filename in glob.glob('*.html'):
    tree = HTMLTreeBuilder.parse(filename)
    root = tree.getroot()

    try:
        testname = root.find('.//title').text
    except AttributeError:
        continue
    commands = []
    for row in root.findall('.//tbody/tr'):
        commands.append(formatcommand(*[td.text for td in row.findall('td')]))

    testfilename = 'seltest_%s.py' % testname
    testbody = ('    def test_%s(self):\n' % testname + ' ' * 8 +
        '\n        '.join(commands) + '\n')
    tests.append(testbody)

f = open('seltest_all.py', 'wb')
f.write(template.substitute(dict(
    testname=testname,
    tests='\n'.join(tests),
    )))
f.close()
