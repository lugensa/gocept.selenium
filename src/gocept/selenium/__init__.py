from util import skipUnlessBrowser
from seleniumrc import Layer as RCLayer

import sys
if sys.version_info >= (2, 6):
    from webdriver import Layer as WebdriverLayer
