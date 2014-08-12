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

from setuptools import setup, find_packages
import sys


script_requirements = []
try:
    import xml.etree
except ImportError:
    # Python < 2.5
    script_requirements.append('elementtree')


install_requires = [
    'gocept.httpserverlayer>1.2',
    'httpagentparser',
    'plone.testing',
    'selenium >= 2.28',
    'Pillow',
    'setuptools']

if sys.version_info < (2, 6):
    # needed but not declared by selenium
    install_requires.append('simplejson')

tests_require = ['mock',
                 'gocept.testing']
if sys.version_info < (2, 7):
    tests_require.append('unittest2')


setup(
    name='gocept.selenium',
    version='2.1.7',
    author='Zope Foundation and Contributors',
    author_email='ws@gocept.com',
    url='http://pypi.python.org/pypi/gocept.selenium',
    description=('Test-friendly Python API for Selenium and integration with '
                 'web application frameworks.'),
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: BFG',
        'Framework :: Plone',
        'Framework :: Plone :: 3.2',
        'Framework :: Plone :: 3.3',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Pylons',
        'Framework :: Pyramid',
        'Framework :: Zope2',
        'Framework :: Zope3',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Zope',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
        ],
    long_description=(
        open('README.txt').read() +
        '\n\n' +
        open('HACKING.txt').read() +
        '\n\n' +
        open('CHANGES.txt').read()),
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    zip_safe=False,
    license='ZPL 2.1',
    namespace_packages=['gocept'],
    install_requires=install_requires,
    extras_require=dict(
        grok=[
            'gocept.httpserverlayer[zopeappwsgi]',
            'zope.app.appsetup',
            ],
        test_grok=[
            'grok',
            'ZODB3',
            ],
        ztk=[
            'gocept.httpserverlayer[zopeapptesting]',
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
        zope2=[
            'gocept.httpserverlayer[zope2testcase]',
            ],
        test_zope2=[
            'Zope2',  # Zope2>=2.12 is eggified
            ],
        plone=[
            'gocept.httpserverlayer[plonetestcase]',
            ],
        test_plone=[
            'Plone',
            'Products.PloneTestCase',
            'Pillow',
            ],
        plonetesting=[
            'gocept.httpserverlayer[plonetestingz2]',
            ],
        test_plonetesting=[
            'Plone',
            'Pillow',
            'plone.app.testing',
            'plone.testing[z2]',
            ],
        screenshot=[
            'Pillow'
        ],
        script=script_requirements,
        test=tests_require,
    ),
    entry_points={
          'console_scripts': [
                  'converthtmltests = gocept.selenium.scripts.converthtmltests:main',
                  ],
          }
)
