# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyclouds',
 'pyclouds.dev',
 'pyclouds.dev.plots',
 'pyclouds.integration',
 'pyclouds.integration.parcel',
 'pyclouds.models',
 'pyclouds.models.ccfm',
 'pyclouds.models.ccfm.ccfmfortran',
 'pyclouds.models.ccfm.ccfmpython',
 'pyclouds.models.ccfm.version0',
 'pyclouds.plot',
 'pyclouds.reference',
 'pyclouds.reference.atmos',
 'pyclouds.reference.atmos.plots',
 'pyclouds.utils']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0',
 'notebook>=6.4.5,<7.0.0',
 'numpy>=1.12.1,<2.0.0',
 'scipy>=1.2.0,<2.0.0',
 'xarray>=0.19.0,<0.20.0']

setup_kwargs = {
    'name': 'pyclouds',
    'version': '0.2.1',
    'description': '1D parcel models for convective clouds',
    'long_description': None,
    'author': 'Leif Denby',
    'author_email': 'leif@denby.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
