import unittest
import mock
import tempfile


class TestConversion(unittest.TestCase):

    def test_parse_options_no_layer(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import LAYER_REQUIRED
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, [])
        self.failUnless(parser.error.called)
        parser.error.assert_called_with(LAYER_REQUIRED)

    def test_parse_options_no_directory(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import DIRECTORY_REQUIRED
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', 'module.layer'])
        self.failUnless(parser.error.called)
        parser.error.assert_called_with(DIRECTORY_REQUIRED)

    def test_parse_options_no_module(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import LAYER_WITH_MODULE
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', 'layer', 'dummy'])
        self.failUnless(parser.error.called)
        parser.error.assert_called_with(LAYER_WITH_MODULE)

    def test_parse_options_one_directory(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import ONE_DIRECTORY
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', 'module.layer', 'first', 'second'])
        self.failUnless(parser.error.called)
        parser.error.assert_called_with(ONE_DIRECTORY)

    def test_parse_options_directory_not_exist(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import (
            DIRECTORY_NOT_EXIST)
        parser = make_parser()
        parser.error = mock.Mock()
        parse_options(parser, ['-l', 'module.layer', 'first'])
        self.failUnless(parser.error.called)
        parser.error.assert_called_with(DIRECTORY_NOT_EXIST)

    def test_parse_options_directory_exists(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        from gocept.selenium.scripts.converthtmltests import DEFAULT_TARGET
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.gettempdir()
        layer = 'module.layer'
        options, directory = parse_options(parser,
            ['-l', layer, source])
        self.assertEquals(source, directory)
        self.assertEquals(options.layer, layer)
        self.assertEquals(options.target, DEFAULT_TARGET)
        self.failUnless(options.verbose)

    def test_parse_options_quiet(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.mkdtemp()
        layer = 'module.layer'
        options, directory = parse_options(parser,
            ['-q', '-l', layer, source])
        self.failIf(options.verbose)

    def test_parse_options_target(self):
        from gocept.selenium.scripts.converthtmltests import parse_options
        from gocept.selenium.scripts.converthtmltests import make_parser
        parser = make_parser()
        parser.error = mock.Mock()
        source = tempfile.mkdtemp()
        target = tempfile.mktemp()
        layer = 'module.layer'
        options, directory = parse_options(parser,
            ['-f', target, '-l', layer, source])
        self.assertEquals(options.target, target)
