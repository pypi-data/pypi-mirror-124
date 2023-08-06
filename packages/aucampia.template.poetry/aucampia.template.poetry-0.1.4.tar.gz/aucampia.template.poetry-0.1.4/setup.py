# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aucampia', 'aucampia.template', 'aucampia.template.poetry']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.0,<8.0.0', 'pydantic>=1.8.2,<2.0.0', 'typer>=0.3.2,<0.4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.8,<0.9']}

entry_points = \
{'console_scripts': ['aucampia.template.poetry = '
                     'aucampia.template.poetry.cli:main',
                     'aucampia.template.poetry.click = '
                     'aucampia.template.poetry.cli_click:main',
                     'aucampia.template.poetry.service = '
                     'aucampia.template.poetry.service:main',
                     'aucampia.template.poetry.typer = '
                     'aucampia.template.poetry.cli_typer:main']}

setup_kwargs = {
    'name': 'aucampia.template.poetry',
    'version': '0.1.4',
    'description': '',
    'long_description': '# ...\n\n```bash\npoetry run aucampia.template.poetry\npoetry run aucampia.template.poetry.click\npoetry run aucampia.template.poetry.typer version\n```\n',
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
