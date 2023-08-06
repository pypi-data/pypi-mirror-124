# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['opyml']

package_data = \
{'': ['*']}

install_requires = \
['defusedxml>=0.7.1,<0.8.0']

setup_kwargs = {
    'name': 'opyml',
    'version': '0.1.1',
    'description': 'An OPML library for Python.',
    'long_description': '# opyml\n\nAn OPML library for Python.\n\nThis is a largely identical "port" of [the Rust crate](https://github.com/Holllo/opml).\n\n## Example\n\n```python\nfrom opyml import OPML, Outline\n\n# Create OPML documents from scratch.\ndocument = OPML()\ndocument.body.outlines.append(Outline(text="Example"))\n\n# Convert documents to XML.\nxml = document.to_xml()\n\n# Parse OPML documents from XML.\ndocument = OPML.from_xml(xml)\n```\n\nFor complete examples check out the `tests/` directory.\n\n## Development\n\n* Install dependencies with [Poetry](https://python-poetry.org) (`poetry shell` + `poetry install`).\n* Format code with `black opyml tests`.\n* Check types with `mypy opyml`.\n* Run tests and collect coverage with `pytest --cov=opyml --cov-report html`.\n* Generate documentation with `pdoc opyml`.\n\n## License\n\nDual-licensed with the [Apache License, Version 2.0](https://github.com/Holllo/opyml/blob/main/LICENSE-Apache) and [MIT license](https://github.com/Holllo/opyml/blob/main/LICENSE-MIT).\n',
    'author': 'Holllo',
    'author_email': 'helllo@holllo.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Holllo/opyml',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
