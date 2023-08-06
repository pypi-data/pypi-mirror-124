# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['niaaml_gui',
 'niaaml_gui.widgets',
 'niaaml_gui.windows',
 'niaaml_gui.windows.threads']

package_data = \
{'': ['*']}

install_requires = \
['NiaPy>=2.0.0rc18,<3.0.0',
 'PyQt5>=5.15.0,<6.0.0',
 'QtAwesome>=1.0.2,<2.0.0',
 'niaaml>=1.1.1rc2,<2.0.0']

setup_kwargs = {
    'name': 'niaaml-gui',
    'version': '0.1.11',
    'description': 'GUI for NiaAML Python package',
    'long_description': '',
    'author': 'Luka Pečnik',
    'author_email': 'lukapecnik96@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/lukapecnik/NiaAML-GUI',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
