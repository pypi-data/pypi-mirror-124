# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['maison']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.0.1,<9.0.0']

entry_points = \
{'console_scripts': ['maison = maison.__main__:main']}

setup_kwargs = {
    'name': 'maison',
    'version': '0.0.0',
    'description': 'Maison',
    'long_description': '# Maison\n\nRead configuration settings from `python` configuration files.\n\n## Motivation\n\nWhen developing a `python` application, e.g a command-line tool, it can be\nhelpful to allow the user to set their own configuration options to allow them\nto tailor the tool to their needs. These options are typically set in files in\nthe root of a project directory that uses the tool, for example in a\n`pyproject.toml` file.\n\n`maison` aims to provide a simple and flexible way to read and validate those\nconfiguration options so that they may be used in the application.\n\n## Help\n\nSee the [documentation](https://dbatten5.github.io/maison) for more details.\n\n## Installation\n\n```bash\npip install maison\n```\n\n## Licence\n\nMIT\n',
    'author': 'Dom Batten',
    'author_email': 'dominic.batten@googlemaill.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dbatten5/maison',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
