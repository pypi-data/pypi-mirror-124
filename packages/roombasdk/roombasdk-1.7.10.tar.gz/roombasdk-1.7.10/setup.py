# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['roombapy', 'roombapy.mapping']

package_data = \
{'': ['*'], 'roombapy': ['assets/*']}

install_requires = \
['paho-mqtt>=1.5.1,<2.0.0', 'pillow>=8.3.0']

entry_points = \
{'console_scripts': ['roomba-connect = roombapy.entry_points:connect',
                     'roomba-discovery = roombapy.entry_points:discovery',
                     'roomba-password = roombapy.entry_points:password']}

setup_kwargs = {
    'name': 'roombasdk',
    'version': '1.7.10',
    'description': 'Python program and library to control Wi-Fi enabled iRobot Roombas',
    'long_description': '# roombasdk\n\n[![CI](https://github.com/pschmitt/roombasdk/actions/workflows/ci.yaml/badge.svg)](https://github.com/pschmitt/roombasdk/actions/workflows/ci.yaml)\n![PyPI](https://img.shields.io/pypi/v/roombasdk)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/roombasdk)\n![PyPI - License](https://img.shields.io/pypi/l/roombasdk)\n\nUnofficial iRobot Roomba python library (SDK).\n\nFork of [NickWaterton/Roomba980-Python](https://github.com/NickWaterton/Roomba980-Python)<br/>\nFork of [pschmitt/roombapy](https://github.com/pschmitt/roombapy)\n\nThis library was created for the [Home Assistant Roomba integration](https://www.home-assistant.io/integrations/roomba/).\n\n# Installation\n\n```shell\npip install roombasdk\n```\n\n# Notes\n\nThis library is only for firmware 2.x.x [Check your robot version!](http://homesupport.irobot.com/app/answers/detail/a_id/529) \n\nOnly local connections are supported.\n\n# How to get your username/blid and password\n\nTo get password from Roomba type in console:\n\n```shell\n$ roomba-password <ip>\n```\n\nIt will find your Roomba in local network, then follow the instructions in console to get password.\nIf IP address not provided password will be request for auto discovered robot. \n\nAlso you can just ask Roomba for info:\n\n```shell\n$ roomba-discovery <optional ip address>\n```\n\nTo test connection with iRobot:\n\n```shell\n$ roomba-connect <ip> <password>\n```\n\n# Mapping Information\n\nThe Roomba position is given as three coordinates: `x`, `y`, and `theta`.  The unit of measure for `x` and `y` is *cm*, theta is *degrees*.  The origin of the mapping coordinates is the position of the dock, which will have coordinates `(0,0,0)`\n\n## Coordinates \n- Dock Front = -y\n- Dock Back = +y\n- Dock Left = -x\n- Dock Right = -y\n\n```\n         | -y \n         |\n-x -------------- +x\n         |\n         | +y\n```\n\n### Coordinates for Map Definitions\n\nWhen defining maps, you will need to define two points, the upper left `p1` and lower right `p2`.  These coordinates would yield the maximum range for the roomba and will be translated into the image coordinate system automatically.\n\n```\np1       | -y \n         |\n-x -------------- +x\n         |\n         | +y   p2\n```\n\n## Degrees\n\nRoomba reports positive degrees when turning left, and negative degrees when turning right, yielding a counter-clockwise direction.\n\n```\n         0\n         | \n         |\n90 -------------- -90\n         |\n         |\n      -180/180    \n```\n\n',
    'author': 'Philipp Schmitt',
    'author_email': 'philipp@schmitt.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simbaja/roombapy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
