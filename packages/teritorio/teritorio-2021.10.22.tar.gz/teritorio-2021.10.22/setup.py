# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['teritorio']

package_data = \
{'': ['*'], 'teritorio': ['_data/*']}

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7.0,<0.8.0']}

setup_kwargs = {
    'name': 'teritorio',
    'version': '2021.10.22',
    'description': 'A library for country and currency ISO codes',
    'long_description': '<p align="center">\n<a href="https://github.com/spapanik/teritorio/actions/workflows/build.yml"><img alt="Build" src="https://github.com/spapanik/teritorio/actions/workflows/build.yml/badge.svg"></a>\n<a href="https://lgtm.com/projects/g/spapanik/teritorio/alerts/"><img alt="Total alerts" src="https://img.shields.io/lgtm/alerts/g/spapanik/teritorio.svg"/></a>\n<a href="https://github.com/spapanik/teritorio/blob/master/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/teritorio"></a>\n<a href="https://pypi.org/project/teritorio"><img alt="PyPI" src="https://img.shields.io/pypi/v/teritorio"></a>\n<a href="https://pepy.tech/project/teritorio"><img alt="Downloads" src="https://pepy.tech/badge/teritorio"></a>\n<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n# teritorio: ISO codes for countries and currencies\n\n## Installation and usage\n\n### Installation\n\n_teritorio_ can be installed by running `pip install teritorio`. It requires Python 3.6.2+ to run.\n\n### Usage\n\nThe two main objects are `Countries` and `Currencies`:\n\n#### Countries usage\n\n```python\nfrom teritorio import Countries\n\n# list all countries\nfor country in Countries():\n    print(country)\n\n# get a specific country\ncountries = Countries()\n\n# access the country as an attribute\nprint(countries.DEU)  # Country(english_name=\'Germany\', french_name="Allemagne (l\')", alpha_2_code=\'DE\', alpha_3_code=\'DEU\', numeric_code=276)\n# access the country with square brackets\nprint(countries["DEU"])  # Country(english_name=\'Germany\', french_name="Allemagne (l\')", alpha_2_code=\'DE\', alpha_3_code=\'DEU\', numeric_code=276)\n```\n\n#### Currencies usage\n\n```python\nfrom teritorio import Currencies\n\n# list all currencies\nfor currency in Currencies():\n    print(currency)\n\n# get a specific currency\ncurrencies = Currencies()\n\n# access the currency as an attribute\nprint(currencies.GBP)  # Currency(code=\'GBP\', name=\'Pound Sterling\', entities=[\'GUERNSEY\', \'ISLE OF MAN\', \'JERSEY\', \'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)\'], numeric_code=826, minor_units=2)\n# access the currency with square brackets\nprint(currencies["GBP"])  # Currency(code=\'GBP\', name=\'Pound Sterling\', entities=[\'GUERNSEY\', \'ISLE OF MAN\', \'JERSEY\', \'UNITED KINGDOM OF GREAT BRITAIN AND NORTHERN IRELAND (THE)\'], numeric_code=826, minor_units=2)\n```\n\n## Versioning\n\nThe project project adheres to [Calendar Versioning][calver]. The reason is that the data are dominated by political decisions, making semantic versioning largely irrelevant.\n\n\n\n[calver]: https://calver.org\n',
    'author': 'Stephanos Kuma',
    'author_email': 'stephanos@kuma.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/spapanik/teritorio',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
