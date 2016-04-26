import sys
import os

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
sys.path.insert(0, os.path.abspath('_themes'))
extensions = []
templates_path = ['_templates']
html_theme_path = ['_themes']
html_static_path = ['_static']

source_suffix = '.rst'
master_doc = 'index'
exclude_patterns = ['_build']

project = u'gocept.selenium'
copyright = u"""\
    2011-2015, Zope Foundation and Contributors.
    <a href="http://sphinx.pocoo.org/">Sphinx</a>-Theme adapted from
    <a href="http://jinja.pocoo.org/docs/">Jinja</a>
"""
version = '3.0'  # XXX determine automatically
release = version

pygments_style = 'sphinx'
html_theme = 'jinja'

html_sidebars = {
    'index': [
        'sidebarlogo.html',
        'sidebarintro.html',
        'sourcelink.html',
        'searchbox.html'
    ],
    '**': [
        'sidebarlogo.html',
        'localtoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html'
    ]
}

html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = True
