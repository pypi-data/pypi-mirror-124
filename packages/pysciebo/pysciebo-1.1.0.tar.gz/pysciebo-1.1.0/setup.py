# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pysciebo']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.3,<9.0.0', 'pyocclient>=0.6,<0.7']

entry_points = \
{'console_scripts': ['pysciebo = pysciebo.cmd:cmd']}

setup_kwargs = {
    'name': 'pysciebo',
    'version': '1.1.0',
    'description': 'A Python client for sciebo aka hochschulcloud.nrw',
    'long_description': '# PySciebo<!-- omit in toc -->\n\n[PySciebo](https://gitlab.ub.uni-bielefeld.de/nils.mueller/pysciebo) is a Python\nclient library for interfacing with [sciebo](https://www.hochschulcloud.nrw/),\nthe official "Hochschulcloud NRW".\n\nThe library is not endorsed officially and should be used accordingly.\n\n## Table of Contents<!-- omit in toc -->\n\n- [1. Installation](#1-installation)\n- [2. Usage](#2-usage)\n  - [2.1. As a Command-Line Interface](#21-as-a-command-line-interface)\n  - [2.2. As a Library](#22-as-a-library)\n- [3. Development](#3-development)\n- [4. Todo](#4-todo)\n\n## 1. Installation\n\nPySciebo is available on [PyPI](https://pypi.org/project/pysciebo/) and can be installed using `pip`:\n\n```bash\npip install pysciebo\n```\n\n## 2. Usage\n\n### 2.1. As a Command-Line Interface\n\nThe PySciebo command-line interface is automatically installed when installing\nthe package via `pip`. Authentication works either via command-line arguments\nor by setting the following environment variables:\n\n- `SCIEBO_URL`\n- `SCIEBO_USERNAME`\n- `SCIEBO_PASSWORD`\n\n```shell\n# example using CLI arguments\npysciebo upload --url $URL --username $USERNAME --password $PASSWORD /remote/file/path /local/file/path\n\n# example using environment variables\npysciebo upload /remote/file/path /local/file/path\n```\n\n### 2.2. As a Library\n\nUsing your university\'s sciebo URL, your username, and your password, the client\nworks like this:\n\n```python\nimport os\nfrom pysciebo import ScieboClient\n\nurl = os.environ["SCIEBO_URL"]\nusername = os.environ["SCIEBO_USERNAME"]\npassword = os.environ["SCIEBO_PASSWORD"]\n\n# Login\nclient = ScieboClient(url, username, password)\n\n# Upload a file to sciebo\nclient.upload("/sciebo/file/path", "/local/file/path")\n\n# Download a file from sciebo (local path is optional)\nclient.download("/sciebo/file/path", "/local/file/path")\n\n# Delete a file from sciebo\nclient.delete("/sciebo/file/path")\n```\n\n## 3. Development\n\nThe project uses pre-commit hooks using [pre-commit](https://pre-commit.com/).\nFollow the [installation instructions](https://pre-commit.com/#install) to set\nthem up properly.\n\nNew functionality should at least be covered by integration tests. The rest is\noptional but recommended.\n\n## 4. Todo\n\n- [x] Implement command-line interface\n- [ ] Extend feature list\n',
    'author': 'Nils Müller',
    'author_email': 'nils.mueller@uni-bielefeld.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.ub.uni-bielefeld.de/nils.mueller/pysciebo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
