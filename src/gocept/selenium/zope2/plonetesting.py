from zope.configuration import xmlconfig

from plone.testing import Layer
from plone.testing.z2 import STARTUP

from gocept.selenium import zope2


class Isolation(Layer):

    defaultBases = (STARTUP,)

    def setUp(self):
        context = self['configurationContext']
        xmlconfig.file('testing.zcml', package=zope2, context=context)

ISOLATION = Isolation()
