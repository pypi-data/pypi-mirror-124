# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esak']

package_data = \
{'': ['*']}

install_requires = \
['marshmallow>=3.13.0,<4.0.0', 'requests>=2.26.0,<3.0.0']

extras_require = \
{'docs': ['sphinx-rtd-theme>=0.5.2,<0.6.0']}

setup_kwargs = {
    'name': 'esak',
    'version': '1.0.0',
    'description': 'Marvel API wrapper for python.',
    'long_description': 'esak - Marvel API wrapper for python 3\n===========================================\n\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/psf/black\n\n- `Code on Github <https://github.com/bpepple/esak>`_\n- `Published on PyPi <https://pypi.python.org/pypi/esak>`_\n- `Marvel API documentation <https://developer.marvel.com/docs>`_\n\n**To install:**\n\n.. code-block:: bash\n\n    $ pip3 install --user esak\n\n**Example Usage:**\n\n.. code-block:: python\n\n    import esak\n\n    # Your own config file to keep your private key local and secret\n    from config import public_key, private_key\n\n    # Authenticate with Marvel, with keys I got from http://developer.marvel.com/\n    m = esak.api(public_key, private_key)\n\n    # Get all comics from this week, sorted alphabetically by title\n    pulls = sorted(m.comics_list({\n        \'format\': "comic",\n        \'formatType\': "comic",\n        \'noVariants\': True,\n        \'dateDescriptor\': "thisWeek",\n        \'limit\': 100}),\n        key=lambda comic: comic.title)\n\n    for comic in pulls:\n        # Write a line to the file with the name of the issue, and the\n        # id of the series\n        print(\'{} (series #{})\'.format(comic.title, comic.series.id))\n\n\nContributing\n------------\n\n- When running a new test for the first time, set the environment variables\n  ``PUBLIC_KEY`` and ``PRIVATE_KEY`` to any Marel API keys. The result will be\n  stored in the `tests/testing_mock.sqlite` database without your keys.\n\n',
    'author': 'Brian Pepple',
    'author_email': 'bdpepple@gmail.com',
    'maintainer': 'Brian Pepple',
    'maintainer_email': 'bdpepple@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
