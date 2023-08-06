# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['colabfold']

package_data = \
{'': ['*']}

install_requires = \
['absl-py>=0.13.0,<0.14.0',
 'alphafold-colabfold==2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'jax>=0.2.20,<0.3.0',
 'matplotlib==3.1.3',
 'numpy>=1.19.0,<2.0.0',
 'pandas>=1.3.3,<2.0.0',
 'py3Dmol>=1.7.0,<2.0.0',
 'requests>=2.26.0,<3.0.0',
 'tensorflow-cpu>=2.6.0,<3.0.0',
 'tqdm>=4.62.2,<5.0.0']

entry_points = \
{'console_scripts': ['colabfold_batch = colabfold.batch:main']}

setup_kwargs = {
    'name': 'colabfold',
    'version': '0.1.0b1',
    'description': 'Making protein folding accessible to all. Predict proteins structures both in google colab and on your machine',
    'long_description': None,
    'author': 'Milot Mirdita',
    'author_email': 'milot.mirdita@mpibpc.mpg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<3.11',
}


setup(**setup_kwargs)
