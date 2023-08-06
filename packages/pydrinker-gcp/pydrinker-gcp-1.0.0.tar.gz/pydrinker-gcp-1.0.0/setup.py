# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydrinker_gcp']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-pubsub>=2.8.0,<3.0.0', 'pydrinker>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pydrinker-gcp',
    'version': '1.0.0',
    'description': "Google Cloud Platform 'plugin' for pydrinker",
    'long_description': '# pydrinker-gcp\nGoogle Cloud Platform "plugin" for pydrinker \n\n---\n\nCalm down your fingers! This project is under construction... wait for scenes from the next chapters :smile:\n',
    'author': 'Rafael Henrique da Silva Correia',
    'author_email': 'rafael@abraseucodigo.com.br',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rafaelhenrique/pydrinker-gcp',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.10',
}


setup(**setup_kwargs)
