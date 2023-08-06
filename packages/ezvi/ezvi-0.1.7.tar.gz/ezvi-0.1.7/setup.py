# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ezvi']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'astroid==2.4.2',
 'click==7.1.2',
 'isort==5.6.4',
 'lazy-object-proxy==1.4.3',
 'mccabe==0.6.1',
 'pylint==2.6.0',
 'six==1.15.0',
 'toml==0.10.2']

entry_points = \
{'console_scripts': ['ezvi = ezvi.cli:main']}

setup_kwargs = {
    'name': 'ezvi',
    'version': '0.1.7',
    'description': 'Automated typing in the Vi editor.',
    'long_description': '# ezvi\n\n`ezvi` is a python package that allows typing automation for the `Vi` editor.\n\n## Installation\n\n`ezvi` is distributed as a Pip package. To install the program, simply run\n\n```bash\npip install ezvi\n```\n\n## Usage\n\nThe package can be used via the `CLI`. `ezvi` functions can also be imported and used in a Python program.\n\n### The `CLI`\n\nThere are two different ways of using `ezvi` via the command line. \n\n#### The `text` command \n\n`text` can be used to type a pre-written file. It takes one argument (`infile` and one option (`--writefile`).\n\n* `infile` is the path towards the pre-written file.\n* `--writefile` tells the program to save the file again after typing it. `--writefile` takes one argument that corresponds to the path where the typed file will be written.\n\n##### Example\n\n```bash\nezvi text -w ./foo.txt example/message.txt\n```\n\nThis takes the `message.txt` example from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory and types it again. The Vi buffer is then written to `./foo.txt`.\n\n#### The `yaml` command\n\n`yaml` should be used to take a configuration as instructions to type a new file. The `yaml` command only takes one argument (`config`). Everything else should be specified in the config file.\n\n* `config` is the path towards the configuration file.\n\n##### Example\n\n```bash\nezvi yaml example/config.yaml\n```\n\nThis command would take the `config.yaml` file from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory and use it to type a new file.\n\n### Writing a config file\n\nA configuration file is just a yaml file that will be parsed using [PyYAML](https://pyyaml.org "PyYAML"). The structure of the file should be similar to the one in the `config.yaml` file from the [example](https://github.com/TrickyTroll/ezvi/tree/latest/example) directory.\n\n```yaml\n- write_line: "Hello!"\n- new_line: 2\n- write_chars: "-- Good Bot."\n- write_file: "message.txt"\n- quit_editor:\n```\n\nA `-` must precede every action.\n\n## Documentation\n\nFor more in depth documentation, please refer to the \n[Read the Docs](https://ezvi.readthedocs.io/en/main/)\n\n## Development\n\nThis package is in alpha. Not much testing has been done and many things could still change.  To see the latest commit, go check the [latest](https://github.com/TrickyTroll/ezvi/tree/latest) branch.\n',
    'author': 'TrickyTroll',
    'author_email': 'tricky@beon.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
