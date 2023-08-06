# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aiovotifier']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'aiovotifier',
    'version': '0.1.1',
    'description': 'An asynchronous MInecraft server votifier client in Python',
    'long_description': '# Aio-Votifier ![Code Quality](https://www.codefactor.io/repository/github/iapetus-11/aio-votifier/badge) ![PYPI Version](https://img.shields.io/pypi/v/aio-votifier.svg) ![PYPI Downloads](https://img.shields.io/pypi/dw/aio-votifier?color=0FAE6E) ![Views](https://api.ghprofile.me/view?username=iapetus-11.aio-votifier&color=0FAE6E&label=views&style=flat)\n*An asynchronous MInecraft server votifier client in Python*\n\n## Example Usage:\n```py\nfrom aiovotifier import NuVotifierClient\nimport asyncio\n\nasync def main():\n    async with NuVotifierClient("127.0.0.1", 8192, "token") as client:\n        await client.vote("Iapetus11")\n\nasyncio.run(main())\n```\nor\n```py\nfrom aiovotifier import NuVotifierClient\nimport asyncio\n\nasync def main():\n    client = NuVotifierClient("127.0.0.1", 8192, "token")\n    await client.connect()\n\n    await client.vote("Iapetus11")\n\n    await client.close()\n\nasyncio.run(main())\n```\n',
    'author': 'Milo Weinberg',
    'author_email': 'iapetus011@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
