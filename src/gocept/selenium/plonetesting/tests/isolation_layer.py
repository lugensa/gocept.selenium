from zope.configuration import xmlconfig

from plone.testing import Layer
from plone.testing.z2 import STARTUP
from plone.testing.z2 import FunctionalTesting

from gocept.selenium import plonetesting


class Isolation(Layer):

    defaultBases = (STARTUP, )

    def setUp(self):
        context = self['configurationContext']
        xmlconfig.file('testing.zcml', package=plonetesting.tests,
            context=context)

ISOLATION = Isolation()

FUNCTIONAL_ISOLATION = FunctionalTesting(bases=(ISOLATION,),
    name="gocept.selenium:FunctionalIsolation")
