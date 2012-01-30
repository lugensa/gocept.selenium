#############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os.path
from setuptools import setup, find_packages


setup(
    name='gocept.selenium',
    version='0.13',
    author='Zope Foundation and Contributors',
    author_email='ws@gocept.com',
    url='http://packages.python.org/gocept.selenium',
    description='zope.testing layer that integrates Selenium-RC for '
                'any WSGI, Zope 2, Plone, ZTK, or grok application.',
    long_description=(
        open(os.path.join('src', 'gocept', 'selenium', 'README.txt')).read() +
        '\n\n' +
        open('CHANGES.txt').read()),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL 2.1',
    namespace_packages=['gocept'],
    install_requires=[
        'selenium',
        'setuptools',
        ],
    extras_require=dict(
        grok=[
            'zope.app.appsetup',
            'zope.app.wsgi',
            ],
        test_grok=[
            'grok',
            'ZODB3',
            ],
        ztk=[
            'zope.app.server',
            'zope.app.testing',
            'zope.app.wsgi',
            'zope.server',
            ],
        test_ztk=[
            'zope.app.appsetup',
            'zope.app.zcmlfiles',
            'zope.securitypolicy',
            'zope.testing >= 3.8.0',
            'zope.interface',
            'zope.schema',
            'ZODB3',
            ],
        zope2=[ # Zope2>=2.12 is eggified
            'Zope2',
            ],
        plone=[
            'Products.PloneTestCase',
            ],
        test_plone=[
            'Plone',
            'PILwoTK',
            ],
        plonetesting=[
            'plone.testing[z2]',
            ],
        test_plonetesting=[
            'Plone',
            'PILwoTK',
            'plone.app.testing',
            ],
        script=[
            'elementtree',
            ],
        test_script=[
            'mock',
            ],
    ),
    entry_points={
          'console_scripts': [
                  'converthtmltests = gocept.selenium.scripts.converthtmltests:main',
                  ],
          }
)
