# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_moysklad',
 'py_moysklad.clients',
 'py_moysklad.entities',
 'py_moysklad.entities.agents',
 'py_moysklad.entities.discounts',
 'py_moysklad.entities.documents',
 'py_moysklad.entities.documents.positions',
 'py_moysklad.entities.products',
 'py_moysklad.responses']

package_data = \
{'': ['*']}

install_requires = \
['api-client>=1.3.1,<2.0.0', 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'py-moysklad',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'NerV',
    'author_email': 'voldemar.krs@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
