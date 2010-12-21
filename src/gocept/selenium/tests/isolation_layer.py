from zope.configuration import xmlconfig

from plone.testing import Layer
from plone.testing.z2 import STARTUP
from plone.testing.z2 import FunctionalTesting

import gocept.selenium.zope2


class Isolation(Layer):

    defaultBases = (STARTUP, )

    def setUp(self):
        context = self['configurationContext']
        xmlconfig.file('testing.zcml', package=gocept.selenium.zope2,
            context=context)

ISOLATION = Isolation()

FUNCTIONAL_ISOLATION = FunctionalTesting(bases=(ISOLATION,),
    name="gocept.selenium:FunctionalIsolation")
