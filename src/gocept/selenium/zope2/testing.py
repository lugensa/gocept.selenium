from Products.Five import zcml

from gocept.selenium import zope2


class IsolationLayer(object):

    __name__ = "gocept.selenium.tests.isolation"
    __bases__ = ()

    def setUp(cls):
        zcml.load_config('testing.zcml',
            package=zope2)
    setUp = classmethod(setUp)

isolationLayer = IsolationLayer()
