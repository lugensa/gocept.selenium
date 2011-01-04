#!/usr/bin/env python
"""
Convert HTML selenium tests to gocept.selenium based test cases.
"""

import re
import os
import glob
from elementtree import HTMLTreeBuilder
from string import Template
from optparse import OptionParser

module_template = Template('''\
import unittest

import gocept.selenium.plonetesting
import $layer_module


class TestAll(gocept.selenium.plonetesting.TestCase):

    layer = $layer

$tests

def test_suite():
    return unittest.makeSuite(TestAll)
''')

variable_regexp = re.compile('\$\{(?P<varname>\w*)\}')

method_body_template = Template('''\
    def test_$testname(self):
        selenium = self.selenium
$commands
''')


def formatcommand(command, *args):
    if not command:
        return ''

    arguments = []
    for arg in args:
        if not arg:
            continue
        matched = variable_regexp.match(arg)
        if matched is None:
            arguments.append('"%s"' % arg)
        else:
            arguments.append("self.getVar('%s')" % matched.group('varname'))
    return '        selenium.%s(%s)' % (command, ', '.join(arguments))


def parse_options():
    parser = OptionParser(usage="generatetests -l LAYER [options] directory",
        version="%prog 1.0")
    parser.add_option("-f", "--file", dest="target",
                      default="tests_all_selenium.py",
                      help="write tests to OUTPUT", metavar="FILE")
    parser.add_option("-l", "--layer", dest="layer",
                      help="full python import path to layer instance",
                      metavar="LAYER")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      help="print progress messages to stdout")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="do not print progress messages to stdout")

    options, args = parser.parse_args()
    if not args:
        parser.error('source directory is required')
    elif len(args) > 1:
        parser.error('only one source directory should be provided')
    if not options.layer:
        parser.error('layer is required')
    if len(options.layer.split('.')) <= 1:
        parser.error('layer option should include the module')
    directory = args[0]
    return options, directory


def main():
    options, directory = parse_options()
    tests = []
    pattern = os.path.join(directory, '*.html')
    for filename in glob.glob(pattern):
        if options.verbose:
            print "Parsing %s" % filename
        tree = HTMLTreeBuilder.parse(filename)
        root = tree.getroot()

        try:
            testname = root.find('.//title').text
        except AttributeError:
            continue
        commands = []
        for row in root.findall('.//tbody/tr'):
            command = formatcommand(*[td.text for td in row.findall('td')])
            commands.append(command)

        method_body = method_body_template.substitute(dict(
            testname=testname,
            commands='\n'.join(commands)))
        tests.append(method_body)

    if options.verbose:
        print "Generating %s" % options.target
    f = open(options.target, 'wb')
    layer = options.layer
    layer_module = ".".join(layer.split('.')[:-1])
    f.write(module_template.substitute(dict(
        testname='all',
        tests='\n'.join(tests),
        layer=layer,
        layer_module=layer_module,
        )))
    f.close()

if  __name__ == '__main__':
    main()
