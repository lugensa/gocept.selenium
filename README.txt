======================
buildout configuration
======================

gocept.selenium integrates with quite a lot of different testing approaches and
needs to work across a wide spectrum of software versions, e. g. Zope2 before
and after eggification (2.10/2.12), ZTK-KGS, Grok-KGS, Plone3, Plone4 etc.

This has two consequences, one is that we use different extras_require for the
different flavours, so clients will need to specify that, e. g.
gocept.selenium[ztk] or gocept.selenium[grok].

The second is that there is no single buildout configuration for this package,
but rather quite a lot of them, so we are able to run our tests against all the
different software versions we integrate with.

The base package itself is tested with ``selenium.cfg``, this has no further
dependencies except the ``selenium`` package. The various flavours have their
own cfg file, in some cases in several versions (e.g. Plone3/Plone4, Zope2
pre/post eggs etc.). This means that in order to set up the buildout, you'll
need to specify the configuration you want to test, like this::

    $ python bootstrap.py -c ztk.cfg
    $ bin/buildout -c ztk.cfg

Note that the zope210 and plone3 configurations require Python-2.4, while the
others should work at least up to Python-2.6.
