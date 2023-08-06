# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qtawk', 'qtawk.ui']

package_data = \
{'': ['*'], 'qtawk': ['ico/*', 'man/*', 'scripts/*']}

install_requires = \
['PyQt5==5.14.1', 'pyqtgraph==0.11.0']

entry_points = \
{'console_scripts': ['qtawk = qtawk.__main__:run']}

setup_kwargs = {
    'name': 'qtawk',
    'version': '0.1.2',
    'description': 'Qtawk is a WYSIWYG tool to generate bash scripts very quickly',
    'long_description': '\n# Description\n\nQtawk is a graphical tool to generate bash scripts very quickly and without pain.\n\n\n# official website\n\nhttps://qtawk.ntik.org/\n\n\n# documentation\n\nhttps://qtawk.ntik.org/docs/index.html\n\n\n# contact\n\nmail : qtawk-dev@ntik.org\nIRC  : ntick.org  #qtawk (port 6667 SSL)\n',
    'author': 'Pierrick Lebourgeois',
    'author_email': 'qtawk-dev@ntik.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://qtawk.ntik.org/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
