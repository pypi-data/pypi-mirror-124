# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['eoplatform']

package_data = \
{'': ['*'], 'eoplatform': ['platforms/*']}

install_requires = \
['rich>=10.12.0,<11.0.0', 'typer[all]>=0.4.0,<0.5.0']

entry_points = \
{'console_scripts': ['eoplatform = eoplatform.cli:app']}

setup_kwargs = {
    'name': 'eoplatform',
    'version': '0.1.0',
    'description': 'Earth Observation made easy.',
    'long_description': '<br/>\n<p align="center">\n  <a href="https://github.com/mtralka/EOPlatform">\n    <img src="images/logo.jpg" alt="EOP Logo" width="300" height="300">\n  </a>\n\n  <h3 align="center">An Earth Observation Platform</h3>\n\n  <p align="center">\n    Earth Observation made easy. \n    <br/>\n    <br/>\n    <a href="https://github.com/mtralka/EOPlatform/issues">Report Bug</a>\n    |\n    <a href="https://github.com/mtralka/EOPlatform/issues">Request Feature</a>\n  </p>\n</p>\n\n![Downloads](https://img.shields.io/github/downloads/mtralka/EOPlatform/total) ![Forks](https://img.shields.io/github/forks/mtralka/EOPlatform?style=social) ![Stargazers](https://img.shields.io/github/stars/mtralka/EOPlatform?style=social) <br/> ![Issues](https://img.shields.io/github/issues/mtralka/EOPlatform) ![License](https://img.shields.io/github/license/mtralka/EOPlatform) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) ![mypy](https://img.shields.io/badge/mypy-checked-brightgreen)\n\n## About\n\n*eoplatform* is a Python package that aims to simplify Remote Sensing Earth Observation by providing actionable information on a wide swath of RS platforms and provide a simple API for downloading and visualizing RS imagery. Made for scientsits, educators, and hobbiests alike.\n\n* Easy to access **information** on RS platforms\n  * Band information\n  * Orbit regimes\n  * Scene statistics\n* Accessible data downloading (in-progress)\n  * Landsat 8\n  * Sentinel-2\n* Common band composites\n\n### Installation\n\n`eoplatform` can be installed by running `pip install eoplatform`. It requires Python 3.7 or above to run. \n\nIf you want to install the latest version from git you can run \n\n```sh\npip install git+git://github.com/mtralka/eoplatform\n```\n\n### Example\n\n<img src="images/eoplatform-info-landsat8.PNG" alt="Landsat8 Info" width="600">\n\n## Usage\n\n*eoplatform* is fully accessible through the command line (CLI) and as a module import.\n\n### CLI\n\nCommands:\n\n* `info` - find platform info\n* `download` - download platform scenes\n\n#### Querying platform info (cli)\n\n```sh\nUsage: eoplatform info [OPTIONS] PLATFORM\n\nArguments:\n  PLATFORM  [required]\n\nOptions:\n  -d, --description / -nd, --no-description\n                                  [default: description]     \n  --help                          Show this message and exit.\n```\n\nEX:\n\n```sh\neoplatform info Landsat8\n```\n\nshow all info *eoplatform* has on `Landsat8`\n\n```sh\neoplatform info Landsat8 -b\n```\n\nshows only `Landsat8`\'s bands\n\n#### Downloading platform scenes (cli)\n\nin-progress\n\n```sh\nUsage: eoplatform download [OPTIONS] PLATFORM\n\nArguments:\n  PLATFORM  [required]\n\nOptions:\n  --help  Show this message and exit.\n```\n\n### Module import\n\n#### Querying platform info (import)\n\nYou can import your desired platform\n\n```python\nfrom eoplatform import Landsat8\n\nLandsat8.info()  # OR print(Landsat8)\n```\n\nor search from the *eoplatform* module itself\n\n```python\nimport eoplatform as eop\n\neop.info("Landsat8")\n```\n\n#### Downloading platform scenes (import)\n\n in-progress\n\n ```python\nfrom eoplatform import Landsat8\n\nLandsat8.download()\n```\n\n```python\nimport eoplatform as eop\n\neop.download("Landsat8")\n```\n\nboth methods accept the full range of search keword arguments\n\n## Roadmap\n\nSee the [open issues](https://github.com/mtralka/EOPlatform/issues) for a list of proposed features (and known issues).\n\n* download support\n\n\n## Contributing\n\nContributions are welcome. Any contributions you make are appreciated.\n\n* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/mtralka/EOPlatform/issues/new) to discuss it, or directly create a pull request with the proposed changes.\n* Create individual PR for each suggestion.\n* Use pre-commit hooks - `pre-commit install`\n* Code style is `black`, `mypy --strict`\n\n## License\n\nDistributed under the GNU GPL-3.0 License. See [LICENSE](https://github.com/mtralka/EOPlatform/blob/main/LICENSE.md) for more information.\n\n## Built With\n\n* [Rich](https://github.com/willmcgugan/rich)\n* [Typer](https://github.com/tiangolo/typer)\n\n## Authors\n\n* [**Matthew Tralka**](https://github.com/mtralka/)\n',
    'author': 'Matthew Tralka',
    'author_email': 'matthew@tralka.xyz',
    'maintainer': 'Matthew Tralka',
    'maintainer_email': 'matthew@tralka.xyz',
    'url': 'https://github.com/mtralka/EOPlatform',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
