# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['testreverseautoslitcode']

package_data = \
{'': ['*']}

install_requires = \
['astropy==4.3.post1',
 'astroquery==0.4.3',
 'matplotlib==3.4.2',
 'numpy==1.21.1',
 'panstamps==0.6.1',
 'pytest-shutil==1.7.0',
 'pyyaml==5.3.1',
 'regions==0.5',
 'shapely']

setup_kwargs = {
    'name': 'testreverseautoslitcode',
    'version': '0.1.35',
    'description': 'Test Compiling of Code',
    'long_description': None,
    'author': 'Jessica Sullivan',
    'author_email': 'jsulli27@nd.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
