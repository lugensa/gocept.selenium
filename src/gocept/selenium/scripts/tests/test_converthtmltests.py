from io import StringIO
import unittest
from unittest import mock
import tempfile
import os
import sys

PLONE3LOGIN_METHOD = '''\
    def test_plone3login(self):
        selenium = self.selenium
        selenium.open("/plone/login_form")
        selenium.type("__ac_name", "admin")
        selenium.type("__ac_password", "admin")
        selenium.clickAndWait("submit")
        selenium.assertText("//a[@id=\'user-name\']/span", "admin")
'''

LAYER = "module.layer"

PLONE3LOGIN_MODULE = '''\
# -*- coding: utf-8 -*-
import unittest

import gocept.selenium.plonetesting
import module


class TestAll(gocept.selenium.plonetesting.TestCase):

    layer = module.layer

    def test_plone3login(self):
        selenium = self.selenium
        selenium.open("/plone/login_form")
        selenium.type("__ac_name", "admin")
        selenium.type("__ac_password", "admin")
        selenium.clickAndWait("submit")
        selenium.assertText("//a[@id=\'user-name\']/span", "admin")


def test_suite():
    return unittest.makeSuite(TestAll)
'''


class TestConversion(unittest.TestCase):

    def test_parse_options_no_layer(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import LAYER_REQUIRED
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, [])
        self.assertTrue(parser.error.called)
        parser.error.assert_called_with(LAYER_REQUIRED)

    def test_parse_options_no_directory(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import DIRECTORY_REQUIRED
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', LAYER])
        self.assertTrue(parser.error.called)
        parser.error.assert_called_with(DIRECTORY_REQUIRED)

    def test_parse_options_no_module(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import LAYER_WITH_MODULE
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', 'layer', 'dummy'])
        self.assertTrue(parser.error.called)
        parser.error.assert_called_with(LAYER_WITH_MODULE)

    def test_parse_options_one_directory(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import ONE_DIRECTORY
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', LAYER, 'first', 'second'])
        self.assertTrue(parser.error.called)
        parser.error.assert_called_with(ONE_DIRECTORY)

    def test_parse_options_directory_not_exist(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import (
            DIRECTORY_NOT_EXIST)
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', LAYER, 'first'])
        self.assertTrue(parser.error.called)
        parser.error.assert_called_with(DIRECTORY_NOT_EXIST)

    def test_parse_options_directory_exists(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import DEFAULT_TARGET
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.gettempdir()
        options, directory = parse_options(parser, ['-l', LAYER, source])
        self.assertEqual(source, directory)
        self.assertEqual(options.layer, LAYER)
        self.assertEqual(options.target, DEFAULT_TARGET)
        self.assertTrue(options.verbose)

    def test_parse_options_quiet(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.mkdtemp()
        options, directory = parse_options(parser, ['-q', '-l', LAYER, source])
        self.assertFalse(options.verbose)

    def test_parse_options_target(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.mkdtemp()
        target = tempfile.mktemp()
        options, directory = parse_options(
            parser, ['-f', target, '-l', LAYER, source])
        self.assertEqual(options.target, target)

    def test_parse_file(self):
        from gocept.selenium.scripts.converthtmltests import parse_file

        import gocept.selenium.scripts.tests
        tests_dir = os.path.dirname(gocept.selenium.scripts.tests.__file__)
        filename = os.path.join(tests_dir, 'plone3login.html')

        testname, commands, encoding = parse_file(filename)
        self.assertEqual(encoding, 'utf-8')
        self.assertEqual(testname, 'plone3login')
        self.assertEqual(len(commands), 5)
        self.assertEqual('        selenium.open("/plone/login_form")',
                         commands[0])

    def test_parse_file_no_title(self):
        from gocept.selenium.scripts.converthtmltests import parse_file

        import gocept.selenium.scripts.tests
        tests_dir = os.path.dirname(gocept.selenium.scripts.tests.__file__)
        filename = os.path.join(tests_dir, 'notitle.html')

        testname, commands, encoding = parse_file(filename)
        self.assertEqual(None, testname)

    def test_parse_file_no_commands(self):
        from gocept.selenium.scripts.converthtmltests import parse_file

        import gocept.selenium.scripts.tests
        tests_dir = os.path.dirname(gocept.selenium.scripts.tests.__file__)
        filename = os.path.join(tests_dir, 'nocommands.html')

        testname, commands, encoding = parse_file(filename)
        self.assertEqual('nocommands', testname)
        self.assertEqual(len(commands), 0)

    def test_formatcommand_no_command(self):
        from gocept.selenium.scripts.converthtmltests import formatcommand
        line = formatcommand('')
        self.assertEqual(line, '')

    def test_formatcommand_command_without_args(self):
        from gocept.selenium.scripts.converthtmltests import formatcommand
        line = formatcommand('command')
        self.assertEqual(line, '        selenium.command()')

    def test_formatcommand_command_with_single_arg(self):
        from gocept.selenium.scripts.converthtmltests import formatcommand
        line = formatcommand('command', 'arg')
        self.assertEqual(line, '        selenium.command("arg")')

    def test_formatcommand_command_with_two_args(self):
        from gocept.selenium.scripts.converthtmltests import formatcommand
        line = formatcommand('command', 'arg1', 'arg2')
        self.assertEqual(line, '        selenium.command("arg1", "arg2")')

    def test_formatcommand_command_with_three_args_one_empty(self):
        from gocept.selenium.scripts.converthtmltests import formatcommand
        line = formatcommand('command', 'arg1', '', 'arg2')
        self.assertEqual(line, '        selenium.command("arg1", "arg2")')

    def test_parse_directory(self):
        from gocept.selenium.scripts.converthtmltests import parse_directory

        import gocept.selenium.scripts.tests
        tests_dir = os.path.dirname(gocept.selenium.scripts.tests.__file__)

        tests = [test for test in parse_directory(tests_dir, False)]
        tests.pop(0)  # this is the encoding
        self.assertEqual(len(tests), 1)
        self.assertEqual(tests[0], PLONE3LOGIN_METHOD)

    def test_parse_directory_no_html(self):
        from gocept.selenium.scripts.converthtmltests import parse_directory

        import gocept.selenium.scripts
        tests_dir = os.path.dirname(gocept.selenium.scripts.__file__)

        tests = [test for test in parse_directory(tests_dir, False)]
        self.assertEqual(len(tests), 0)

    def test_make_module(self):
        from gocept.selenium.scripts.converthtmltests import make_module

        module = make_module([PLONE3LOGIN_METHOD], LAYER, 'module', 'utf-8')
        self.assertEqual(module, PLONE3LOGIN_MODULE)

    def test_main(self):
        from gocept.selenium.scripts.converthtmltests import main
        import gocept.selenium.scripts.tests
        tests_dir = os.path.dirname(gocept.selenium.scripts.tests.__file__)
        target = tempfile.mktemp()

        output = StringIO()

        sys.stdout = output
        try:
            main(['-f', target, '-l', LAYER, tests_dir])
            module = open(target).read()
            self.assertEqual(module, PLONE3LOGIN_MODULE)
            text = output.getvalue()
            lines = text.splitlines()
            self.assertEqual(len(lines), 4)
            self.assertTrue(lines[0].startswith('Parsing ['))
            self.assertIn('plone3login.html]', text)
            self.assertTrue(lines[1].startswith('Parsing ['))
            self.assertIn('nocommands.html]', text)
            self.assertTrue(lines[2].startswith('Parsing ['))
            self.assertIn('notitle.html]', text)
            self.assertTrue(lines[3].startswith('Generating ['))
            self.assertIn(target, lines[3])
        finally:
            sys.stdout = sys.__stdout__

    def test_main_no_html(self):
        from gocept.selenium.scripts.converthtmltests import main
        import gocept.selenium.scripts
        tests_dir = os.path.dirname(gocept.selenium.scripts.__file__)
        target = tempfile.mktemp()

        output = StringIO()

        sys.stdout = output
        try:
            main(['-f', target, '-l', LAYER, tests_dir])
            self.assertFalse(os.path.exists(target))
            self.assertEqual(output.getvalue(), 'No file was generated !\n')
        finally:
            sys.stdout = sys.__stdout__
