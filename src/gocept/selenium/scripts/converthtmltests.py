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

$methods

def test_suite():
    return unittest.makeSuite(TestAll)
''')

variable_regexp = re.compile('\$\{(?P<varname>\w*)\}')

method_template = Template('''\
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
        #XXX selenese should implement storeText
        #else:
        #    arguments.append("self.getVar('%s')" % matched.group('varname'))
    return '        selenium.%s(%s)' % (command, ', '.join(arguments))


def make_parser():
    parser = OptionParser(usage="converthtmltests -l LAYER [options] directory",
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


def parse_directory(directory, verbose):
    pattern = os.path.join(directory, '*.html')
    for filename in glob.glob(pattern):
        if verbose:
            print "Parsing [%s]" % filename
        filename = os.path.abspath(filename)
        testname, commands = parse_file(filename)
        if testname is None or len(commands) == 0:
            continue
        method = method_template.substitute(dict(
            testname=testname,
            commands='\n'.join(commands)))
        yield method


def parse_file(filename):
    tree = HTMLTreeBuilder.parse(filename)
    root = tree.getroot()

    try:
        testname = root.find('.//title').text
    except AttributeError:
        return None, None
    commands = []
    for row in root.findall('.//tbody/tr'):
        command = formatcommand(*[td.text for td in row.findall('td')])
        commands.append(command)
    return testname, commands


def make_module(methods, layer, layer_module):
    return module_template.substitute(dict(
        testname='all',
        methods='\n'.join(methods),
        layer=layer,
        layer_module=layer_module,
        ))


def main(args=None):
    parser = make_parser()
    options, directory = parse_options(parser, args)
    verbose = options.verbose
    target = os.path.abspath(options.target)
    layer = options.layer
    layer_module = ".".join(layer.split('.')[:-1])

    methods = [method for method in parse_directory(directory, verbose)]

    if len(methods) == 0:
        print "No file was generated !"
        return
    if options.verbose:
        print "Generating [%s]" % target
    f = open(target, 'wb')
    module = make_module(methods, layer, layer_module)
    f.write(module)
    f.close()


if  __name__ == '__main__':
    main()
