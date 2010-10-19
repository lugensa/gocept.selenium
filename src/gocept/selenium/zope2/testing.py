from Products.Five import zcml

from gocept.selenium import zope2


class FixtureLayer(object):

    __name__ = "gocept.selenium.tests.fixture"
    __bases__ = ()

    def setUp(cls):
        zcml.load_config('testing.zcml',
            package=zope2)
    setUp = classmethod(setUp)

fixtureLayer = FixtureLayer()
