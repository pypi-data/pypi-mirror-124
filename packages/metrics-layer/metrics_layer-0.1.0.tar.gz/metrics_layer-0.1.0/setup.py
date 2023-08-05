# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['metrics_layer',
 'metrics_layer.api',
 'metrics_layer.api.blueprints',
 'metrics_layer.api.models',
 'metrics_layer.core',
 'metrics_layer.core.convert',
 'metrics_layer.core.model',
 'metrics_layer.core.parse',
 'metrics_layer.core.query',
 'metrics_layer.core.sql']

package_data = \
{'': ['*'], 'metrics_layer': ['webapp/*']}

install_requires = \
['GitPython>=3.1.20,<4.0.0',
 'PyPika>=0.48.8,<0.49.0',
 'PyYAML>=5.4.1,<6.0.0',
 'lkml>=1.1.0,<2.0.0',
 'networkx>=2.6.3,<3.0.0',
 'requests>=2.26.0,<3.0.0',
 'sqlparse>=0.4.1,<0.5.0']

extras_require = \
{'all': ['pandas>=1.2.2,<2.0.0',
         'snowflake-connector-python>=2.5.1,<2.6.0',
         'pyarrow==3.0.0',
         'google-cloud-bigquery>=2.24.1,<3.0.0',
         'Flask>=1.1.4,<1.2.0',
         'Flask-RESTful>=0.3.9,<0.4.0',
         'Flask-SQLAlchemy>=2.5.1,<3.0.0',
         'gunicorn>=20.1.0,<21.0.0',
         'Flask-Bcrypt>=0.7.1,<0.8.0',
         'PyJWT>=2.1.0,<3.0.0'],
 'bigquery': ['pandas>=1.2.2,<2.0.0',
              'pyarrow==3.0.0',
              'google-cloud-bigquery>=2.24.1,<3.0.0'],
 'flask': ['Flask>=1.1.4,<1.2.0',
           'Flask-RESTful>=0.3.9,<0.4.0',
           'Flask-SQLAlchemy>=2.5.1,<3.0.0',
           'gunicorn>=20.1.0,<21.0.0',
           'Flask-Bcrypt>=0.7.1,<0.8.0',
           'PyJWT>=2.1.0,<3.0.0'],
 'snowflake': ['pandas>=1.2.2,<2.0.0',
               'snowflake-connector-python>=2.5.1,<2.6.0',
               'pyarrow==3.0.0']}

setup_kwargs = {
    'name': 'metrics-layer',
    'version': '0.1.0',
    'description': 'The open source metrics layer.',
    'long_description': '# Metrics Layer\n\nTODO\n',
    'author': 'Paul Blankley',
    'author_email': 'paul@zenlytic.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Zenlytic/metrics_layer',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.10',
}


setup(**setup_kwargs)
