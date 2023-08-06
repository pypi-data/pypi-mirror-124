# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['trackbranch']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['trackbranch = trackbranch.main:main']}

setup_kwargs = {
    'name': 'trackbranch',
    'version': '0.1.3',
    'description': 'Maintain branch collection profiles for Git repositories',
    'long_description': '# trackbranch\n\n`trackbranch` is a tool for developers that can be used to store\ncollections of branches in the form of profiles. This can be useful\nfor situations where you have multiple branches to group into the\nsame action.\n\n### Installation\n\nUsers can install the `trackbranch` package via PyPi:\n\n    $ pip install trackbranch\n\nOr, clone the repository, build it and install it with pip:\n\n    $ poetry lock\n    $ poetry update\n    $ poetry build\n    $ pip install dist/*.whl\n\n### Getting Started\n\nSee `trackbranch --help` for details on command line arguments\nand program usage.\n\n### Usage\n\nCreate a branch profile `my-profile` consisting of `branch1` and `branch2`:\n\n    # Add branch1 and branch2 to my-profile.\n    $ trackbranch -p my-profile add branch1 branch2\n    added \'branch1\' to \'my-profile\'\n    added \'branch2\' to \'my-profile\'\n\nThis will automatically create a `.trackbranch.json` file if one\ncannot be found in the current directory or upwards.\n\nList all profiles:\n\n    $ trackbranch ls\n    my-profile: [\'branch1\', \'branch2\']\n\nList specific branches by providing `-p|--profile`:\n\n    # List branches in the my-profile collection.\n    $ trackbranch -p my-profile ls\n    branch1 branch2\n\nFor each branch in `my-profile`, execute the command `-c`. Each `{br}` string\nformat piece is replaced by the branch name.\n\n    # Execute -c for each branch found in my-profile.\n    $ trackbranch -p my-profile exec -c \'bash -c "git checkout {br}; git rebase -i base"\'\n\nRemove `branch1` from `my-profile`.\n\n    # Remove branch1 from my-profile; branch2 remains.\n    $ trackbranch -p my-profile rm branch1\n    removed \'branch1\' from \'my-profile\'\n\nCompletely clear out `my-profile`.\n\n    # Clear my-profile.\n    $ trackbranch -p my-profile clear\n    profile \'my-profile\' has been removed\n\n### License\n\nThis project operates under The MIT [License](./LICENSE).\n\n### Authors\n\n| Name         | Email          |\n|--------------|----------------|\n| Kevin Morris | kevr@0cost.org |\n',
    'author': 'Kevin Morris',
    'author_email': 'kevr@0cost.org',
    'maintainer': 'Kevin Morris',
    'maintainer_email': 'kevr@0cost.org',
    'url': 'https://github.com/kevr/trackbranch',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
