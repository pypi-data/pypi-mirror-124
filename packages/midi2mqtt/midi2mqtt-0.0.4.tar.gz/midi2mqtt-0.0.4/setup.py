# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['midi2mqtt']

package_data = \
{'': ['*']}

install_requires = \
['paho-mqtt>=1.6.0,<2.0.0', 'python-rtmidi>=1.4.9,<2.0.0']

entry_points = \
{'console_scripts': ['midi2mqtt = midi2mqtt.midi2mqtt:main']}

setup_kwargs = {
    'name': 'midi2mqtt',
    'version': '0.0.4',
    'description': 'Receive MIDI signals and forward them to a mqtt broker.',
    'long_description': '# midi2mqtt\nListen to MIDI signals and send them to a mqtt broker.\n\n## Installation\n\nIt can be installed by pip from pipy or from the git repo location\n\n\t# from PyPI\n\t$ pip install midi2mqtt\n\t\n\t# from sources\n\t$ pip install git+https://github.com/pintman/midi2mqtt\n\n',
    'author': 'Pintman',
    'author_email': 'pintman@0xabc.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pintman/midi2mqtt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
