#!/usr/bin/env python
"""
Convert HTML selenium tests to gocept.selenium.seleniumrcd test cases.
"""

import re
import os
import glob
from string import Template
from optparse import OptionParser
try:
    from xml.etree import ElementTree as HTMLTreeBuilder
    from xml.etree.ElementTree import QName
except ImportError:
    # Python < 2.5
    from elementtree import HTMLTreeBuilder

    class QName(object):
        def __init__(self, text_or_uri, tag=None):
            if tag:
                text_or_uri = "{%s}%s" % (text_or_uri, tag)
            self.text = text_or_uri

        def __str__(self):
            return self.text

        def __hash__(self):
            return hash(self.text)

        def __cmp__(self, other):
            if isinstance(other, QName):
                return cmp(self.text, other.text)
            return cmp(self.text, other)


module_template = Template('''\
# -*- coding: $encoding -*-
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
encoding_regexp = re.compile(r'charset=(.*)$')

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
        # XXX selenese should implement storeText
        # else:
        #    arguments.append("self.getVar('%s')" % matched.group('varname'))
    return '        selenium.%s(%s)' % (command, ', '.join(arguments))


def make_parser():
    parser = OptionParser(
        usage="converthtmltests -l LAYER [options] directory",
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
XHTML_NAMESPACE = 'http://www.w3.org/1999/xhtml'


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
    prev_encoding = encoding = None
    for filename in glob.glob(pattern):
        if verbose:
            print "Parsing [%s]" % filename
        filename = os.path.abspath(filename)
        testname, commands, encoding = parse_file(filename)
        if encoding and prev_encoding is None:
            prev_encoding = encoding
            yield encoding
        # XXX raise an error, if prev_encoding and encoding don't match
        if testname is None or len(commands) == 0:
            continue
        method = method_template.substitute(dict(
            testname=testname,
            commands='\n'.join(commands)))
        yield method


def parse_file(filename):
    tree = HTMLTreeBuilder.parse(filename)

    try:
        testname = tree.find('.//%s' % QName(XHTML_NAMESPACE, 'title')).text
    except AttributeError:
        return None, None, None
    content_type = tree.find(".//%s" % QName(
        XHTML_NAMESPACE, "meta[@http-equiv='Content-Type']")).get('content')
    matched = encoding_regexp.search(content_type)
    if matched is not None:
        encoding = matched.group(1).lower()
    else:
        encoding = 'utf-8'
    commands = []
    for row in tree.findall('.//%s/%s' % (QName(XHTML_NAMESPACE, 'tbody'),
                                          QName(XHTML_NAMESPACE, 'tr'))):
        command = formatcommand(
            *[td.text
              for td in row.findall(str(QName(XHTML_NAMESPACE, 'td')))])
        commands.append(command)
    return testname, commands, encoding


def make_module(methods, layer, layer_module, encoding):
    return module_template.substitute(dict(
        testname='all',
        encoding=encoding,
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
    if methods:
        encoding = methods.pop(0)
    else:
        encoding = 'utf-8'

    if len(methods) == 0:
        print "No file was generated !"
        return
    if options.verbose:
        print "Generating [%s]" % target
    f = open(target, 'wb')
    module = make_module(methods, layer, layer_module, encoding)
    module = module.encode(encoding)
    f.write(module)
    f.close()


if __name__ == '__main__':
    main()
