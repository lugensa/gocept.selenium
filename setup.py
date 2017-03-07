from setuptools import setup, find_packages

install_requires = [
    'gocept.httpserverlayer >= 2.0.dev0',
    'httpagentparser',
    'plone.testing',
    'selenium !=2.53.0, !=2.53.1, !=2.53.2, <3.0',
    'Pillow',
    'setuptools']

setup(
    name='gocept.selenium',
    version='3.1.1',
    author='gocept and contributors',
    author_email='mail@gocept.com',
    url='https://goceptselenium.readthedocs.org/',
    description=('Test-friendly Python API for Selenium and integration with '
                 'web application frameworks.'),
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: BFG',
        'Framework :: Plone',
        'Framework :: Plone :: 4.0',
        'Framework :: Plone :: 4.1',
        'Framework :: Plone :: 4.2',
        'Framework :: Plone :: 4.3',
        'Framework :: Plone :: 5.0',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Zope',
        'Topic :: Software Development',
        'Topic :: Software Development :: Testing',
    ],
    long_description=(
        open('README.rst').read() +
        '\n\n' +
        open('HACKING.rst').read() +
        '\n\n' +
        open('CHANGES.rst').read()),
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
        plonetesting=[
            'gocept.httpserverlayer[plonetestingz2]',
        ],
        screenshot=[
            'Pillow'
        ],
    ),
    entry_points={
        'console_scripts': [
            'converthtmltests = gocept.selenium.scripts.converthtmltests:main',
        ],
    },
)
