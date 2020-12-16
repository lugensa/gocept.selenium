from setuptools import setup, find_packages

install_requires = [
    'gocept.httpserverlayer >= 3',
    'httpagentparser',
    'plone.testing >= 7.0',
    'selenium >= 3.141.0',
    'Pillow',
    'setuptools',
]

setup(
    name='gocept.selenium',
    version='6.0',
    author='gocept and contributors',
    author_email='mail@gocept.com',
    url='https://goceptselenium.readthedocs.org/',
    description=('Test-friendly Python API for Selenium and integration with '
                 'web application frameworks.'),
    keywords='selenium zope grok plone pyramid pylons testing',
    classifiers=[
        'Development Status :: 6 - Mature',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Framework :: BFG',
        'Framework :: Plone',
        'Framework :: Plone :: 5.2',
        'Framework :: Plone :: 5.3',
        'Framework :: Plone :: 6.0',
        'Framework :: Pylons',
        'Framework :: Pyramid',
        'Framework :: Zope :: 3',
        'Framework :: Zope :: 4',
        'Framework :: Zope :: 5',
        'Intended Audience :: Developers',
        'License :: OSI Approved',
        'License :: OSI Approved :: Zope Public License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
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
    python_requires='>=3.7, <4',
    install_requires=install_requires,
    extras_require=dict(
        grok=[
            'gocept.httpserverlayer[zopeappwsgi]',
            'zope.app.appsetup',
        ],
        plonetesting=[
            'gocept.httpserverlayer[plonetestingzope]',
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
