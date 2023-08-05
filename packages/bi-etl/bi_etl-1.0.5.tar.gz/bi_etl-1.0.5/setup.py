# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bi_etl',
 'bi_etl.bulk_loaders',
 'bi_etl.components',
 'bi_etl.components.get_next_key',
 'bi_etl.components.performance_testing',
 'bi_etl.components.row',
 'bi_etl.database',
 'bi_etl.exceptions',
 'bi_etl.informatica',
 'bi_etl.lookups',
 'bi_etl.notifiers',
 'bi_etl.parallel',
 'bi_etl.parameters',
 'bi_etl.performance_test',
 'bi_etl.scheduler',
 'bi_etl.scheduler.scheduler_etl_jobs',
 'bi_etl.test_notebooks',
 'bi_etl.tests',
 'bi_etl.tests.etl_jobs',
 'bi_etl.utility',
 'bi_etl.utility.postgresql',
 'bi_etl.utility.sql_server']

package_data = \
{'': ['*'],
 'bi_etl.components': ['performance_testing/temp/*'],
 'bi_etl.tests': ['test_files/*']}

install_requires = \
['CaseInsensitiveDict>=1.0.0,<2.0.0',
 'SQLAlchemy>=1.3,<1.4',
 'btrees>=4.7.2,<5.0.0',
 'gevent>=20.9.0,<21.0.0',
 'openpyxl>=3.0.5,<4.0.0',
 'psutil>=5.7.2,<6.0.0',
 'semidbm>=0.5.1,<0.6.0',
 'sqlparse>=0.3.1,<0.4.0']

extras_require = \
{':extra == "keyring"': ['keyring'],
 'scheduler': ['pyramid>=1.10.4,<2.0.0', 'pytest>=6.1.1,<7.0.0'],
 'test': ['pytest>=6.1.1,<7.0.0']}

setup_kwargs = {
    'name': 'bi-etl',
    'version': '1.0.5',
    'description': 'Python ETL Framework',
    'long_description': '# bi_etl Python ETL Framework for BI\n\n## Docs\n\n[Please see the documentation site for detailed documentation.](https://bietl.dev/docs/index.html)\n\nPython based ETL (Extract Transform Load) framework geared towards BI databases in particular. The goal of the project is to create reusable objects with typical technical transformations used in loading dimension tables.\n\n## Guiding Design Principles\n1. Don’t Repeat Yourself (DRY).\n\n1. The source or target of an ETL owns the metadata (list of columns and data types). The ETL generally has no reason to define those again unless the ETL requires a change. If a datatype must be changed, only that one column’s new type should be specified. If a column name must be changed, only the source & target column names that differ should be specified.\n\n1. Data Quality is King\n\n1. Data quality is more important than performance. For example, the process should fail before truncating data contents (i.e. loading 6 characters into a 5 character field) even if that means sacrificing some load performance.\n\n1. Give helpful error messages.\n\n1. Make it as easy as possible to create re-usable modules.\n\n1. SQL is a very powerful transformation language. The Transform Extract Load (TEL) model should be supported.',
    'author': 'Derek Wood',
    'author_email': 'bietl_info@bietl.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://bitbucket.org/DatastrongTeam/bi_etl/src/master/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
