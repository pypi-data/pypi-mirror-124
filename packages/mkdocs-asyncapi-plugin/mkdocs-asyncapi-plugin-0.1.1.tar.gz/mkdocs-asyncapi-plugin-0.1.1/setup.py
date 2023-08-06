# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['mkdocs_asyncapi_plugin']
entry_points = \
{'mkdocs.plugins': ['render_asyncapi = mkdocs_asyncapi_plugin:AsyncAPIPlugin']}

setup_kwargs = {
    'name': 'mkdocs-asyncapi-plugin',
    'version': '0.1.1',
    'description': 'mkdocs plugin to generate pages from asyncapi spec files',
    'long_description': '# Mkdocs Async API Plugin\n\n[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)\n[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)\n[![PyPi](https://img.shields.io/pypi/v/mkdocs-asyncapi-plugin.svg)](https://pypi.python.org/pypi/mkdocs-asyncapi-plugin)\n[![Supported python versions](https://img.shields.io/pypi/pyversions/mkdocs-asyncapi-plugin.svg)](https://pypi.org/project/mkdocs-asyncapi-plugin/)\n\n## Setup\n\n1. Install [`asyncapi/generator`](https://github.com/asyncapi/generator)\n\n``` sh\nnpm install -g @asyncapi/generator\n```\n\n2. Install this plugin.\n\n``` sh\npip install mkdocs-asyncapi-plugin\n```\n\n3. Add `render_asyncapi` to `mkdocs.yml`:\n\n``` yaml\nplugins:\n  - render_asyncapi\n```\n\n## Usage\n\nCreate a new markdown file which contains only this line:\n\n``` markdown\n!!asyncapi <path-to-spec-file>!!\n```\n\n`path-to-spec-file` is the path to the AsyncAPI spec file relative to the root of the repository (where you run `mkdocs`).\n\nThen, the entire content of this file will be the AsyncAPI spec.\n',
    'author': 'YushiOMOTE',
    'author_email': 'yushiomote@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/yushiomote/mkdocs-asyncapi-plugin',
    'py_modules': modules,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
