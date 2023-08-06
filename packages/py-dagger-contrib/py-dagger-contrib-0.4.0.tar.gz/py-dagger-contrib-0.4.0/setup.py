# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dagger_contrib',
 'dagger_contrib.serializer',
 'dagger_contrib.serializer.dask',
 'dagger_contrib.serializer.dask.dataframe',
 'dagger_contrib.serializer.pandas',
 'dagger_contrib.serializer.pandas.dataframe',
 'dagger_contrib.serializer.path']

package_data = \
{'': ['*']}

install_requires = \
['py-dagger>=0.4,<0.5']

extras_require = \
{'all': ['PyYAML>=5.4,<6.0',
         'pandas>=1.3,<2.0',
         'dask[dataframe]>=2021.9,<2022.0'],
 'dask': ['pandas>=1.3,<2.0', 'dask[dataframe]>=2021.9,<2022.0'],
 'pandas': ['pandas>=1.3,<2.0'],
 'yaml': ['PyYAML>=5.4,<6.0']}

setup_kwargs = {
    'name': 'py-dagger-contrib',
    'version': '0.4.0',
    'description': 'Extensions for the Dagger library (py-dagger in PyPI).',
    'long_description': '# Dagger Contrib\n\nThis repository contains extensions and experiments using the [`py-dagger` library](https://github.com/larribas/dagger)\n\n\n![Python Versions Supported](https://img.shields.io/badge/python-3.8+-blue.svg)\n[![Latest PyPI version](https://badge.fury.io/py/py-dagger-contrib.svg)](https://badge.fury.io/py/py-dagger-contrib)\n[![Test Coverage (Codecov)](https://codecov.io/gh/larribas/dagger-contrib/branch/main/graph/badge.svg?token=fKU68xYUm8)](https://codecov.io/gh/larribas/dagger-contrib)\n![Continuous Integration](https://github.com/larribas/dagger-contrib/actions/workflows/continuous-integration.yaml/badge.svg)\n\n\n---\n\n## Extensions\n\n- `dagger_contrib.serializer`\n    * `AsYAML` - Serializes primitive data types using [YAML](https://yaml.org/spec/).\n    * `path` - Serializes local files or directories given their path name.\n        - `AsTar` - As tarfiles with optional compression.\n        - `AsZip` - As zip files with optional compression.\n    * `pandas.dataframe` - Serializes [Pandas DataFrames](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html).\n        - `AsCSV` - As CSV files.\n        - `AsParquet` - As Parquet files.\n    * `dask.dataframe` - Serializes [Dask DataFrames](https://docs.dask.org/en/latest/dataframe.html).\n        - `AsCSV` - As a directory containing multiple partitioned CSV files.\n        - `AsParquet` - As a directory containing multiple partitioned Parquet files.\n\n\n## Installation\n\n_Dagger Contrib_ is published to the Python Package Index (PyPI) under the name `py-dagger-contrib`. To install it, you can simply run:\n\n```\npip install py-dagger-contrib\n```\n\n### Extras\n\nMany of the packages require extra dependencies. You can install those on your own, or via\n\n```\npip install py-dagger-contrib[pandas]\n```\n\nWhere `pandas` could also be `dask`, `yaml` or `all`.\n',
    'author': 'larribas',
    'author_email': 'lorenzo.s.arribas@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/larribas/dagger-contrib',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
