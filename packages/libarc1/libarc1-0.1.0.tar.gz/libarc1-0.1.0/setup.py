# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['libarc1', 'libarc1.modules']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.14,<2.0', 'pyserial>=3.0,<4.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['dataclasses>=0.7,<0.8']}

setup_kwargs = {
    'name': 'libarc1',
    'version': '0.1.0',
    'description': 'Minimal interface library to ArC1',
    'long_description': '# libarc1: Minimal interface to ArC1\n\n## Scope\n\nLibarc1 provides a minimal way to interact with ArC1. Sometimes you need a\ncustom testing procedure that operates independently of the full ArC1\ninterface. Libarc1 enables you to build your own testing frameworks by\nleveraging the capabilities of the instrument without employing the graphical\nuser interface. That being said libarc1 only provices a shell around the\nread/write operations as well as most of the modules. Complex processing or\nvisualisation are beyond the scope of this library and are left to user to\ndevelop as they see fit. Please note that libarc1 is not meant to be used in\nconjuction with the ArC ONE control software but instead it\'s here to help you\ndevelop application-specific tools based on the ArC1 platform.\n\n## Requirements\n\nYou need at least Python 3.6 to use this library. Other than that libarc1 only\ndepends on numpy and pyserial. If you\'re installing with `pip` these will be\ntaken care for you.\n\n## Installation\n\nAs libarc1 is still in early stages of development it\'s not available in PyPI\nand you should use it directly from the repository. If you have `pip` ≥ 19.0\nyou can point `pip` directly to the source repository\n\n```bash\npip install git+https://github.com/arc-instruments/libarc1\n```\n\nOtherwise see the [Development](#development) section below on how to install\n`poetry`. Using `poetry build` you will get a wheel file in the `dist`\nfolder that\'s installable with `pip` as usual.\n\n## Usage\n\nIn the simplest form one can write\n\n```python\nfrom libarc1 import ArC1, ArC1Conf\n\n# initialise the ArC1 board. Port is platform specific; shown here for Linux.\n# libarc1 will take care of initialising the board with sane defaults\narc1 = ArC1(\'/dev/ttyACM0\')\n\n# alternatively a configuration can be provided as well\n# conf = ArC1Conf()\n# set read voltage to 0.2 V\n# conf.Vread = 0.2\n# arc1 = ArC1(\'/dev/ttyACM0\', config=conf)\n\n# read a single device at W=2, B=7\nresistance = arc1.read_one(2, 7)\n\n# pulse a device with a 100 us pulse @ 2.5 V and read its state\nresistance = arc1.pulseread_one(2, 7, 2.5, 100e-6)\n\n# select a device (W=5, B=12) by closing a specified crosspoint\narc1.select(5, 12)\n\n# pulse the device without reading it\narc1.pulse_active(2.5, 100e-6)\n\n# read all devices\nfor datum in arc1.read_all():\n    # will print current word-/bitline, resistance and amplitude\n    print(datum)\n\n```\n\nHigher level functionality is provided in the form of *modules* which provide a\nself-contained test routine. In fact the `read_all()` method is also\nimplemented as a higer level module. Modules generally run in a separate thread\n(as they are I/O constrained anyway) and they populate an internal buffer. The\nuser-facing API has been kept simple to abstract all this away from the user.\n\n```python\nfrom libarc1 import ArC1, ArC1Conf\nfrom libarc1.modules.curvetracer import CurveTracer\n\n# let\'s get the CurveTracer\'s default configuration\nconf = CurveTracer.default_config\n# and change the number of cycles to 5\nconf["cycles"] = 5\n\n# will run the module on these crosspoints\ndevs = [(5, 7), (9, 12)]\n\n# Run it!\n# Please note: You don\'t need to instantiate CurveTracer. Just the class\n# is enough as libarc1 will take care of instatiating the module with the\n# appropriate configuration and running it in a separate thread\nfor datum in arc1.run_module(CurveTracer, devs, conf):\n    # will return word-/bitline, voltage, resistance, current and cycle nr.\n    print(x)\n\n```\n\n## Development\n\nIf you want to develop on libarc1 start by cloning the repository. The build\nsystem requires `poetry` which can by installed using `pip`. Then `poetry\ninstall` will fetch the dependencies and install them in an appropriate virtual\nenvironment. See [the documentation](https://python-poetry.org/docs/) for more\ninfo.\n',
    'author': 'Spyros Stathopoulos',
    'author_email': 'devel@arc-instruments.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://www.arc-instruments.co.uk/products/arc-one/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
