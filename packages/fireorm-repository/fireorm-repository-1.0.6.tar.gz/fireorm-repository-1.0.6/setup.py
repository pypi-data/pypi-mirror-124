# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fireorm_repository',
 'fireorm_repository.repositories',
 'fireorm_repository.types']

package_data = \
{'': ['*']}

modules = \
['README', 'LICENSE']
install_requires = \
['fireorm==0.0.14', 'python-interface==1.6.0']

setup_kwargs = {
    'name': 'fireorm-repository',
    'version': '1.0.6',
    'description': 'Layer base repository for fireorm',
    'long_description': '# fireorm-repository\nLayer base repository for fireorm\n',
    'author': 'sergey',
    'author_email': 'alekseyserzh88@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Sergey199408081/fireorm-repository',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '==3.10.0',
}


setup(**setup_kwargs)
