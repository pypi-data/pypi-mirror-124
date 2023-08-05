# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ioemu']

package_data = \
{'': ['*']}

install_requires = \
['PyQt5>=5.11.3,<6.0.0']

entry_points = \
{'console_scripts': ['ioemu = ioemu:run']}

setup_kwargs = {
    'name': 'ioemu',
    'version': '0.3.2',
    'description': 'IO Emulator with LEDs and buttons',
    'long_description': "# ioemu\n\n![screenshot](ioemu-screenshot.png)\n\nThe ioemu-project provides an  emulator for input/output operations with simple electronic components like LEDs and push buttons.\n\n## Installation and Upgrade\n\nUse pip for a simple installation. For an update use `install --upgrade`. \n\n- Linux, MacOS: `python3 -m pip install ioemu`\n- Windows: `python -m pip install ioemu`\n\n## Starting the emulator\n\nFirst start the emulator by entering `ioemu` on the commandline. A Gui will show up.\n\n![screenshot](ioemu-screenshot.png)\n\nIt contains a slider for analog values between 0 and 99, threee LEDs and two push buttons from left to right.\n\n## LEDs\n\nIf the emulator is running, you can interact with it from any python program running on the same machine. First import the class `Emulator` from the `ioemu` package.\n\n\n```python\nfrom ioemu import Emulator\n```\n\nNow create an instance of the emulator and switch some LEDs on. They can be controlled by setting the `leds` attribute.\n\n\n```python\nemu = Emulator()\nemu.leds = [True, False, True]\n```\n\n## Buttons\n\n![screenshot](buttons.gif)\n\nThe emulator has two buttons. Their current state (pressed or not pressed) can be read from the attribute `buttons`. It's a bool array corresponding to the state of being pressed.\n\nThe following program lights up some LEDs depending on the button being pressed.\n\n\n```python\nemu = Emulator()\nwhile True:\n    if emu.buttons[0]:\n        emu.leds = [False, True, True]\n        \n    if emu.buttons[1]:\n        emu.leds = [True, True, False]\n\n    if not (emu.buttons[0] or emu.buttons[1]):\n        emu.leds = [False, False, False]\n```\n\n## Analog Value (0-99)\n\nLet's look into a program that allows you to control the LEDs with the slider at the left. The current sliders value can be read from the `analog_value` attribute of the Emulator. Its value ranges from 0 to 99.\n\n![image](analog_value.gif)\n\n\n```python\nimport time\n\nemu = Emulator()\nled_on = 0\n\nwhile True:\n    if 0 <= emu.analog_value < 25:\n        emu.leds = [False, False, False]\n    elif 25 <= emu.analog_value < 50:\n        emu.leds = [True, False, False]\n    elif 50 <= emu.analog_value < 75:\n        emu.leds = [True, True, False]\n    else:\n        emu.leds = [True, True, True]\n```\n\n## Demo\n\nThere is a demo program that can be started with `python -m ioemu.demo`. It will blink the LEDs and print the current button state as well as the analog value to console.\n\n![demo](demo.gif)\n\nYou can find the source code in [demo.py](ioemu/demo.py).\n\n## Bugs\n\nIf you find any bugs or have a feature request, feel free to file a ticket at the projects [bugtracker](https://github.com/tbs1-bo/ioemu/issues/new) on github.\n",
    'author': 'Marco Bakera',
    'author_email': 'marco@bakera.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://tbs1-bo.github.io/ioemu/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
