# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['rafm']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0',
 'numpy',
 'pandas>=1.3.4,<2.0.0',
 'statsdict>=0.1.3,<0.2.0',
 'typer']

entry_points = \
{'console_scripts': ['rafm = rafm.__main__:main']}

setup_kwargs = {
    'name': 'rafm',
    'version': '0.2.0',
    'description': 'rafm',
    'long_description': 'rafm\n====\n\n|PyPI| |Status| |Python Version| |License|\n\n|Read the Docs| |Tests| |Codecov|\n\n|pre-commit| |Black|\n\n.. |PyPI| image:: https://img.shields.io/pypi/v/rafm.svg\n   :target: https://pypi.org/project/rafm/\n   :alt: PyPI\n.. |Status| image:: https://img.shields.io/pypi/status/rafm.svg\n   :target: https://pypi.org/project/rafm/\n   :alt: Status\n.. |Python Version| image:: https://img.shields.io/pypi/pyversions/rafm\n   :target: https://pypi.org/project/rafm\n   :alt: Python Version\n.. |License| image:: https://img.shields.io/pypi/l/rafm\n   :target: https://opensource.org/licenses/MIT\n   :alt: License\n.. |Read the Docs| image:: https://img.shields.io/readthedocs/rafm/latest.svg?label=Read%20the%20Docs\n   :target: https://rafm.readthedocs.io/\n   :alt: Read the documentation at https://rafm.readthedocs.io/\n.. |Tests| image:: https://github.com/unmtransinfo/rafm/workflows/Tests/badge.svg\n   :target: https://github.com/unmtransinfo/rafm/actions?workflow=Tests\n   :alt: Tests\n.. |Codecov| image:: https://codecov.io/gh/unmtransinfo/rafm/branch/main/graph/badge.svg\n   :target: https://codecov.io/gh/unmtransinfo/rafm\n   :alt: Codecov\n.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white\n   :target: https://github.com/pre-commit/pre-commit\n   :alt: pre-commit\n.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg\n   :target: https://github.com/psf/black\n   :alt: Black\n\n\nFeatures\n--------\n\n* TODO\n\n\nRequirements\n------------\n\n* TODO\n\n\nInstallation\n------------\n\nYou can install *rafm* via pip_ from PyPI_:\n\n.. code:: console\n\n   $ pip install rafm\n\n\nUsage\n-----\n\nPlease see the `Command-line Reference <Usage_>`_ for details.\n\n\nContributing\n------------\n\nContributions are very welcome.\nTo learn more, see the `Contributor Guide`_.\n\n\nLicense\n-------\n\nDistributed under the terms of the `MIT license`_,\n*rafm* is free and open source software.\n\n\nIssues\n------\n\nIf you encounter any problems,\nplease `file an issue`_ along with a detailed description.\n\n\nCredits\n-------\n\nThis project was generated from the `UNM Translational Informatics Python Cookiecutter`_ template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _MIT license: https://opensource.org/licenses/MIT\n.. _PyPI: https://pypi.org/\n.. _UNM Translational Informatics Python Cookiecutter: https://github.com/unmtransinfo/cookiecutter-unmtransinfo-python\n.. _file an issue: https://github.com/unmtransinfo/rafm/issues\n.. _pip: https://pip.pypa.io/\n.. github-only\n.. _Contributor Guide: CONTRIBUTING.rst\n.. _Usage: https://rafm.readthedocs.io/en/latest/usage.html\n',
    'author': 'UNM Translational Informatics Team',
    'author_email': 'datascience.software@salud.unm.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/unmtransinfo/rafm',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.10',
}


setup(**setup_kwargs)
