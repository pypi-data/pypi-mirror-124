# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['paseto', 'paseto.keys', 'paseto.protocols']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.1.2,<3.0.0',
 'pycryptodomex>=3.10.1,<4.0.0',
 'pysodium>=0.7.10,<0.8.0']

setup_kwargs = {
    'name': 'paseto',
    'version': '1.0.1',
    'description': 'Platform-Agnostic Security Tokens for Python (PASETO)',
    'long_description': 'PASETO Tokens for Python\n============================================\n[![PyPI](https://img.shields.io/pypi/v/paseto.svg)](https://pypi.python.org/pypi/paseto)\n[![PyPI - License](https://img.shields.io/pypi/l/paseto.svg)](https://pypi.python.org/pypi/paseto)\n[![CI](https://github.com/rlittlefield/pypaseto/actions/workflows/main.yml/badge.svg)](https://github.com/rlittlefield/pypaseto/actions/workflows/main.yml)\n\nThis is an unofficial implementation of\n![PASETO: Platform-Agnostic Security Tokens](https://paseto.io/) for Python.\n\nPASETO versions supported: v2, v3, and v4\n\nPlease note that the v2 token type standard is expected to be deprecated in 2022, so new development should be done ideally on versions 3 or 4.\n\nInstallation\n------------\n\n    pip install paseto\n\n\nUsage\n-----\n\nTo create/parse paseto tokens, use the create/parse functions. These will\nautomatically handle encoding/decoding the JSON payload for you, and validate\nclaims (currently just the \'exp\' expiration registered claim).\n\n```python\nimport paseto\nfrom paseto.keys.symmetric_key import SymmetricKey\nfrom paseto.protocols.v4 import ProtocolVersion4\nmy_key = SymmetricKey.generate(protocol=ProtocolVersion4)\n\n# create a paseto token that expires in 5 minutes (300 seconds)\ntoken = paseto.create(\n    key=my_key,\n    purpose=\'local\',\n    claims={\'my claims\': [1, 2, 3]},\n    exp_seconds=300\n)\n\nparsed = paseto.parse(\n    key=my_key,\n    purpose=\'local\',\n    token=token,\n)\nprint(parsed)\n# {\'message\': {\'exp\': \'2021-10-25T22:43:20-06:00\', \'my claims\': [1, 2, 3]}, \'footer\': None}\n```\n\nYou can also make and verify "public" tokens, which are signed but not\nencrypted:\n\n```python\nimport paseto\nfrom paseto.keys.asymmetric_key import AsymmetricSecretKey\nfrom paseto.protocols.v4 import ProtocolVersion4\nmy_key = AsymmetricSecretKey.generate(protocol=ProtocolVersion4)\n\n# create a paseto token that expires in 5 minutes (300 seconds)\ntoken = paseto.create(\n    key=my_key,\n    purpose=\'public\',\n    claims={\'my claims\': [1, 2, 3]},\n    exp_seconds=300\n)\n\nparsed = paseto.parse(\n    key=my_key,\n    purpose=\'public\',\n    token=token,\n)\nprint(parsed)\n# {\'message\': {\'exp\': \'2021-10-25T22:43:20-06:00\', \'my claims\': [1, 2, 3]}, \'footer\': None}\n```\n',
    'author': 'Ryan Littlefield',
    'author_email': 'ryan@ryanlittlefield.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/rlittlefield/pypaseto',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
