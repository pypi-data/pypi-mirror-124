# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redditwarp',
 'redditwarp._cli',
 'redditwarp.auth',
 'redditwarp.core',
 'redditwarp.http',
 'redditwarp.http.misc',
 'redditwarp.http.transport',
 'redditwarp.http.util',
 'redditwarp.iterators',
 'redditwarp.models',
 'redditwarp.models.load',
 'redditwarp.paginators',
 'redditwarp.paginators.implementations',
 'redditwarp.paginators.implementations.listing',
 'redditwarp.paginators.implementations.listing.mixins',
 'redditwarp.siteprocs',
 'redditwarp.siteprocs.account',
 'redditwarp.siteprocs.collection',
 'redditwarp.siteprocs.comment',
 'redditwarp.siteprocs.comment_tree',
 'redditwarp.siteprocs.custom_feed',
 'redditwarp.siteprocs.draft',
 'redditwarp.siteprocs.flair',
 'redditwarp.siteprocs.flair_emoji',
 'redditwarp.siteprocs.front',
 'redditwarp.siteprocs.live_thread',
 'redditwarp.siteprocs.message',
 'redditwarp.siteprocs.misc',
 'redditwarp.siteprocs.moderation',
 'redditwarp.siteprocs.modmail',
 'redditwarp.siteprocs.submission',
 'redditwarp.siteprocs.subreddit',
 'redditwarp.siteprocs.user',
 'redditwarp.util',
 'redditwarp.websocket',
 'redditwarp.websocket.transport']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'redditwarp',
    'version': '0.2.0',
    'description': 'The unofficial Reddit API library for Python',
    'long_description': None,
    'author': 'Pyprohly',
    'author_email': 'pyprohly@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
