# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['aws_shepherd',
 'aws_shepherd.cli',
 'aws_shepherd.lambda',
 'aws_shepherd.tester']

package_data = \
{'': ['*']}

install_requires = \
['Flask>=2.0.2,<3.0.0',
 'boto3>=1.18.61,<2.0.0',
 'pyngrok>=5.1.0,<6.0.0',
 'rich>=10.3.0,<11.0.0']

entry_points = \
{'console_scripts': ['shepherd = aws_shepherd.cli:main']}

setup_kwargs = {
    'name': 'aws-shepherd',
    'version': '0.1.0',
    'description': 'Sepherds AWS Lamb(das) to your local machine',
    'long_description': None,
    'author': 'Futurebank',
    'author_email': 'opensource@futurebank.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
