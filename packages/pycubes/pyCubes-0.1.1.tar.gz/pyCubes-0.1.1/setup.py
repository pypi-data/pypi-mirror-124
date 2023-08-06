# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cubes']

package_data = \
{'': ['*']}

install_requires = \
['async-timeout>=3.0.1,<4.0.0']

setup_kwargs = {
    'name': 'pycubes',
    'version': '0.1.1',
    'description': 'Library for serializing/deserilizing Minecraft JE packets',
    'long_description': "# pyCubes\n\npyCubes is a library for serializing and deserializing Minecraft Java Edition packets.\n\n**❗ 0.x versions are not stable. The library API is subject to change.**\n\n[Русская версия](https://github.com/DavisDmitry/pyCubes/blob/master/README.ru.md)\n\nInstallation:\n\n```bash\npip install pyCubes\n```\n\n## Usage:\n\nFirst you need to create application instance:\n\n```python3\nimport cubes\n\napp = cubes.Application('127.0.0.1', 25565)\n```\n\nAfter that add a low-level handler:\n\n```python3\nasync def process_handshake(packet: cubes.ReadBuffer) -> None:\n    print('Protocol version:', packet.varint)\n    print('Server host:', packet.string)\n    print('Server port:', packet.unsigned_short)\n    print('Next state:', cubes.ConnectionStatus(packet.varint))\n\napp.add_low_level_handler(cubes.ConnectionStatus.HANDSHAKE, 0x00, process_handshake)\n```\n\nAll that remains is to launch the application:\n\n```python3\napp.run()\n```\n\nA more detailed example can be found [here](https://github.com/DavisDmitry/pyCubes/blob/master/example.py).\n\nAll packages are described [here](https://wiki.vg/Protocol).\n\n## Development\n\nRun formatting:\n\n```bash\nmake format\n```\n\nRun linters:\n\n```bash\nmake lint\n```\n\nRun tests:\n\n```bash\nmake test\n```\n",
    'author': 'Dmitry Davis',
    'author_email': 'dmitrydavis@protonmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DavisDmitry/pyCubes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
