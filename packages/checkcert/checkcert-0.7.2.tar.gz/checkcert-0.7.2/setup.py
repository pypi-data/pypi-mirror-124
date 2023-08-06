# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['checkcert']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0', 'pyOpenSSL>=21.0.0,<22.0.0']

entry_points = \
{'console_scripts': ['checkcert = checkcert.checkcert:main']}

setup_kwargs = {
    'name': 'checkcert',
    'version': '0.7.2',
    'description': 'CLI to check tls cert information and determine validity',
    'long_description': '# checkcert\n\nThis utility was based off of [this\ngist](https://gist.github.com/gdamjan/55a8b9eec6cf7b771f92021d93b87b2c).\n\ncheckcert has the logic of that gist wrapped in a click-based CLI and added command-line options\n(checkcert --help to see them)\n\nFull documentation is available at\n[https://checkcert.readthedocs.io](https://checkcert.readthedocs.io)\n\n# Installation\n\n## from PyPi\npip install checkert\n\n# Usage\n\nWhen you run `pip install checkcert`, you will get a `checkcert` command.  To\nshow all the options, simply run `checkcert --help` to get the most-current list\nof commands and options.\n\n### Basic Usage\nThe basic usage is `checkcert example.com`\n\n### Check cert with an alternate port\n\nAnywhere you specify the host, you may use the format `host:port` to specify an\nalternate port.  If no port is specified, 443 will be used.  To check something\nrunning on port 8081 for example, execute `checkcert example.com:8081`\n\n### Multiple domains\n\ncheckcert will take all domains specified on the command line.  Multiple values\nmay be specified as `checkcert example.com www.example.com alt.example.com:444`\n\n### Domain list from a file\n\ncheckcert can be instructed to pull the list of domains from a file instead with\nthe --filename option.  The file contents will just be a domain per line\n(specified in host:port format, or just host to default to port 443)\n\ncreate a file named domains.txt with contents like the following\n\n```\nexample.com\nwww.example.com\nalt.example.com:444\n```\n\nThen execute `checkcert --filename domains.txt`\n',
    'author': 'Alex Kelly',
    'author_email': 'kellya@arachnitech.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kellya/checkcert',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
