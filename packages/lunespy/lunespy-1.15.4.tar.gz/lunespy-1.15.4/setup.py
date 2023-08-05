# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lunespy',
 'lunespy.client',
 'lunespy.client.transactions',
 'lunespy.client.transactions.alias',
 'lunespy.client.transactions.burn',
 'lunespy.client.transactions.cancel',
 'lunespy.client.transactions.issue',
 'lunespy.client.transactions.lease',
 'lunespy.client.transactions.mass',
 'lunespy.client.transactions.reissue',
 'lunespy.client.transactions.transfer',
 'lunespy.client.wallet',
 'lunespy.server',
 'lunespy.server.address',
 'lunespy.server.blocks',
 'lunespy.server.transactions',
 'lunespy.utils',
 'lunespy.utils.crypto',
 'lunespy.utils.settings']

package_data = \
{'': ['*']}

install_requires = \
['base58>=2.1.0,<3.0.0',
 'python-axolotl-curve25519>=0.4.1.post2,<0.5.0',
 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'lunespy',
    'version': '1.15.4',
    'description': 'Library for communication with nodes in mainnet or testnet of the lunes-blockchain network',
    'long_description': "# LunesPy\n\n**The [old version](https://github.com/Lunes-platform/LunesPy/tree/old) is being discontinued, but it can still be used at your own and risk.**\n\nLibrary for communication with nodes in mainnet or testnet of the lunes-blockchain network\nAllows the automation of **sending assets**, **issue end reissue tokens**, **lease** and **create new wallet**.\n\n\n## [What's new?](./CHANGELOG.md)\n\n\n## [How to use LunesPy?](./docs/TUTORIAL.md)\n\n## [Want to contribute to LunesPy?](./CONTRIBUTING.md)\n\n## Contributors\n\nThanks to the following people who have contributed to this project:\n\n* [olivmath](https://github.com/olivmath)\n* [marcoslkz](https://github.com/marcoslkz)\n* [VanJustin](https://github.com/VanJustin)\n\n## Contact\n\nIf you want to contact me you can reach me at <lucas.oliveira@lunes.io>.\n\n## License\n\n[Apache License Version 2.0](./LICENSE).\n",
    'author': 'Lunes Platform',
    'author_email': 'lucas.oliveira@lunes.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
