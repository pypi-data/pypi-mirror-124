# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arc',
 'arc.application',
 'arc.autocomplete',
 'arc.builtin',
 'arc.callbacks',
 'arc.command',
 'arc.present',
 'arc.prompt',
 'arc.types',
 'arc.types.converters',
 'arc.utils']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['arc = arc.application:cli']}

setup_kwargs = {
    'name': 'arc-cli',
    'version': '5.0.0',
    'description': 'A Regular CLI',
    'long_description': '# ARC: A Regular CLI\nA tool for building declartive, and highly extendable CLI systems for Python 3.9\n\n# ARC Features\n- Automatic type convertsion\n- Command Namespacing\n- Help Documentation Generation\n- User-extension via Dynamic namespace loading\n\n# Docs\n- [Docs](http://arc.seanrcollings.com)\n- [Wiki](https://github.com/seanrcollings/arc/wiki)\n- [Changelog](https://github.com/seanrcollings/arc/wiki/Changelog)\n\n# Installation\n\n```\n$ pip install arc-cli\n```\n\nClone for development\n```\n$ git clone https://github.com/seanrcollings/arc\n$ poetry install\n```\n\n\n# Quick Start\n\n```py\nfrom arc import CLI\n\ncli = CLI()\n\n@cli.command()\ndef hello():\n    print("Hello, World!")\n\ncli()\n```\n\n```\n$ python example.py hello\nHello, World!\n```\nReference [getting started](https://github.com/seanrcollings/arc/wiki) for more info\n\n# Tests\nTests are written with `pytest`\n```\n$ pytest\n```\n',
    'author': 'Sean Collings',
    'author_email': 'seanrcollings@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/seanrcollings/arc',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
