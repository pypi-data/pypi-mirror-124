# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['brsus', 'brsus.interfaces', 'brsus.sim', 'brsus.toolbox']

package_data = \
{'': ['*']}

install_requires = \
['cantools==36.4.0', 'dbfread==2.0.7', 'pandas==1.3.4', 'pyarrow==5.0.0']

entry_points = \
{'console_scripts': ['fmt = scripts.code_quality:do_code_formatting',
                     'fmt-check = scripts.code_quality:check_code_formatting',
                     'isort-check = scripts.code_quality:check_import_order',
                     'isort-fmt = scripts.code_quality:sort_import_order',
                     'linter = scripts.code_quality:linter',
                     'tests = scripts.code_quality:run_tests']}

setup_kwargs = {
    'name': 'brsus',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Ale Farias',
    'author_email': '0800alefarias@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
