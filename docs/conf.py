# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import datetime
import pkg_resources
import os
import sys
import yaml  # Requires: pip install PyYAML

__this_file = os.path.abspath(__file__)
__this_dir = os.path.dirname(__this_file)
__root = os.path.dirname(__this_dir)  # tk-katana repository root
sys.path.insert(0, __root)


def get_docs_deploy_branch(default='master'):
    """Get the branch which the docs are deployed from.

    Keyword Args:
        default (str): Defaults branch name to use if non found.

    Returns:
        str: Branch name which the docs are deployed from.
    """
    branch = None

    with open(os.path.join(__root, '.travis.yml'), 'r') as travis_yml:
        travis_data = yaml.load(travis_yml)
        for deployment in travis_data.get('deploy', []):
            if deployment.get('provider') == 'pages':
                # "on" key maps to "True" for some reason lol
                branch = deployment.get(True, {}).get('branch')
                break

    return branch or default


def get_version_from_changelog():
    """Fetch version string from headings in changelog.rst.

    Parse every word in the first 20 lines of changelog.rst for valid versions.

    Returns:
        str: Version number.
    """
    result = None

    with open('changelog.rst', 'r') as changelog:
        max_count = 20
        for line_count, line in enumerate(changelog, start=1):
            for word in line.split():
                try:
                    pkg_resources.packaging.version.Version(word)
                    result = word
                    break   # Break out of: for word in line.split()
                except pkg_resources.packaging.version.InvalidVersion:
                    pass

            if result is not None or line_count == max_count:
                break  # Break out of: for line in changelog

        if result is None:
            raise ValueError(
                'No valid version number/word found in the first {0} '
                'lines of changelog.rst'.format(max_count)
            )

    return result  # Return here in case the file does not get closed properly.


# -- Project information -----------------------------------------------------

project = u'tk-katana'

# For logos, images used
author = u'The Foundry, Shotgunsoftware, Rob Blau, Joseph Yu, Liam Hoflay'
copyright = u'{0.year}, {1}'.format(datetime.date.today(), author)

# The short X.Y version and the full version, including alpha/beta/rc tags
version = release = get_version_from_changelog()

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '1.8'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.githubpages',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
source_suffix = ['.rst', '.md']

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = None

# A boolean that decides whether module names are prepended to all object names
# (for object types where a “module” of some kind is defined),
# e.g. for py:function directives. Default is True.
add_module_names = False

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# A dictionary of values to pass into the template engine’s context for
# all pages. Single values can also be put in this dictionary using the
# -A command-line option of sphinx-build.
html_context = {
    # https://github.com/rtfd/sphinx_rtd_theme/blob/a3ab477aaa23f3b7ab7d62c7abc2cc74102ab2b8/sphinx_rtd_theme/breadcrumbs.html#L45
    'display_github': True,
    'github_user': 'wwfxuk',
    'github_repo': 'tk-katana',
    'github_version': get_docs_deploy_branch(),
    'conf_py_path': '/docs/',
}

# The URL which points to the root of the HTML documentation.
# It is used to indicate the location of document like canonical_url.
html_baseurl = u'https://{ctx[github_user]}.github.io/{ctx[github_repo]}'
html_baseurl = html_baseurl.format(ctx=html_context)

# If given, this must be the name of an image file
# (path relative to the configuration directory) that is the logo of the docs.
# It is placed at the top of the sidebar;
# its width should therefore not exceed 200 pixels. Default: None.
html_logo = '_static/icon_64_bw.png'

# If given, this must be the name of an image file
# (path relative to the configuration directory) that is the
# favicon of the docs. Modern browsers use this as the icon for tabs,
# windows and bookmarks. It should be a Windows-style icon file (.ico),
# which is 16x16 or 32x32 pixels large. Default: None.
html_favicon = html_logo

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}

# -- Extension configuration -------------------------------------------------

# This value contains a list of modules to be mocked up.
# This is useful when some external dependencies are
# not met at build time and break the building process.
# You may only specify the root package of the
# dependencies themselves and omit the sub-modules:
autodoc_mock_imports = [
    "sgtk", "tank",               # Shotgun imports
    "Katana", "AssetAPI", "UI4",  # Katana imports
    "Qt",                         # Qt imports
]

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
