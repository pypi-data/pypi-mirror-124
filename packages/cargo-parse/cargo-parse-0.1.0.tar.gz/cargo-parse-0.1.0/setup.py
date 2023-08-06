# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cargo_parse', 'cargo_parse.models']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.8.2,<2.0.0', 'toml>=0.10.2,<0.11.0']

setup_kwargs = {
    'name': 'cargo-parse',
    'version': '0.1.0',
    'description': 'Library to parse the Cargo.toml manifest file.',
    'long_description': '# cargo-parse\n\nA Python package to parse `Cargo.toml` manifest files.\n\n## Installation\n\nThis package is not (yet) published on PyPI. For now, the best way to install the package is to use\n[Poetry](https://python-poetry.org/).\n\nClone this repository and run `poetry install`.\n\n### Install in another environment\n\nTo install the package in a system environment, or another virtual\nenvironment besides the Poetry project environment:\n\n1. Build the package wheel with `poetry build`.\n2. Install the package using the correct environment\'s `pip`:\n```\n<your-python> -m pip install <path-to-repo>/dist/cargo-parse-*.whl\n```\n\n\n## Usage\n\nImport the `parse_manifest_from_toml` function and use it to parse the contents of `Cargo.toml`:\n\n\n```python\nfrom cargo_parse import parse_manifest_from_toml\n\nfrom pathlib import Path\n\ncargo_toml_file = "Cargo.toml"\nmanifest = parse_manifest_from_toml(Path(cargo_toml_file))\n\n# Print out the package version\nprint(manifest.package.version)\n\n# Print out the dependencies\nif manifest.dependencies is not None:\n    print(manifest.dependencies)\nelse:\n    print(f"No dependencies defined in {cargo_toml_file}")\n```\n',
    'author': 'Andrew Hoetker',
    'author_email': 'andrew.hoetker@thinkdeca.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Deca-Technologies/cargo-parse',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
