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


def make_parser():
    parser = OptionParser(usage="generatetests -l LAYER [options] directory",
        version="%prog 1.0")
    parser.add_option("-f", "--file", dest="target",
                      default=DEFAULT_TARGET,
                      help="write tests to FILE", metavar="FILE")
    parser.add_option("-l", "--layer", dest="layer", default=None,
                      help="full python import path to layer instance",
                      metavar="LAYER")
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose",
                      help="print progress messages to stdout")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose", default=True,
                      help="do not print progress messages to stdout")
    return parser

DEFAULT_TARGET = 'tests_all_selenium.py'
LAYER_REQUIRED = 'Layer (-l) argument is required.'
DIRECTORY_REQUIRED = 'Source directory is required.'
LAYER_WITH_MODULE = 'Layer (-l) should include a module.'
ONE_DIRECTORY = 'Only one source directory should be provided.'
DIRECTORY_NOT_EXIST = 'Source directory does not exist.'


def parse_options(parser, args=None):
    directory = ''
    options, args = parser.parse_args(args=args)
    if not options.layer:
        parser.error(LAYER_REQUIRED)
    elif not args:
        parser.error(DIRECTORY_REQUIRED)
    elif len(options.layer.split('.')) <= 1:
        parser.error(LAYER_WITH_MODULE)
    elif len(args) > 1:
        parser.error(ONE_DIRECTORY)
    else:
        directory = os.path.abspath(args[0])
        if not os.path.exists(directory):
            parser.error(DIRECTORY_NOT_EXIST)
    return options, directory


def main():
    parser = make_parser()
    options, directory = parse_options(parser)
    tests = []
    pattern = os.path.join(directory, '*.html')
    for filename in glob.glob(pattern):
        filename = os.path.abspath(filename)
        if options.verbose:
            print "Parsing [%s]" % filename
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

    target = os.path.abspath(options.target)
    if options.verbose:
        print "Generating [%s]" % target
    f = open(target, 'wb')
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
