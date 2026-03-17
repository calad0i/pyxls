import os
import sys
from unittest.mock import MagicMock

# Pre-mock xls.raw so the C extension is never imported during the doc build.
# This avoids nanobind/Python 3.14 functools.wraps incompatibilities and means
# no compiled extension is needed to build the documentation.
_raw_mock = MagicMock()
for _mod in (
    'xls.raw',
    'xls.raw.c_api',
    'xls.raw.ir_builder',
    'xls.raw.dslx',
    'xls.raw.vast',
):
    sys.modules[_mod] = _raw_mock

sys.path.insert(0, os.path.abspath('../src'))

from importlib.metadata import version as _pkg_version  # noqa: E402

try:
    release = _pkg_version('pyxls')
except Exception:
    release = '0.0.0'
version = release

project = 'pyxls'
copyright = '2025, Chang Sun'
author = 'Chang Sun'

myst_enable_extensions = [
    'amsmath',
    'deflist',
    'dollarmath',
    'fieldlist',
    'html_admonition',
    'html_image',
    'replacements',
    'smartquotes',
    'strikethrough',
    'substitution',
    'tasklist',
]

autosummary_generate = True

extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx_rtd_theme',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

templates_path = ['_templates']
exclude_patterns = ['_build', 'autodoc/modules.rst']

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_context = {
    'display_github': True,
    'github_user': 'calad0i',
    'github_repo': 'pyxls',
    'github_version': 'master',
    'conf_py_path': '/docs/',
}
