# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tap_feed', 'tap_feed.tests', 'tap_feed.tests.parser']

package_data = \
{'': ['*']}

install_requires = \
['feedparser>=6.0.8,<7.0.0',
 'requests>=2.25.1,<3.0.0',
 'singer-sdk>=0.3.11,<0.4.0']

entry_points = \
{'console_scripts': ['tap-feed = tap_feed.tap:TapFeed.cli']}

setup_kwargs = {
    'name': 'tap-feed',
    'version': '1.0.0',
    'description': '`tap-feed` is a Singer tap for various feeds (RSS, Atom, CDF, iTunes, and Dublin Core), built with the Meltano SDK for Singer Taps.',
    'long_description': None,
    'author': 'Jon Watson',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<3.10',
}


setup(**setup_kwargs)
