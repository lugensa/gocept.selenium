from util import skipUnlessBrowser
from seleniumrc import Layer as RCLayer, TestCase as RCTestCase

import sys
if sys.version_info >= (2, 6):
    from webdriver import Layer as WebdriverLayer
    from webdriver import WebdriverSeleneseLayer, WebdriverSeleneseTestCase
