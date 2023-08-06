# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zbase32']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'python-zbase32',
    'version': '0.1.1',
    'description': 'A human-oriented base-32 encoding.',
    'long_description': '# zbase32\n\nA human-oriented base-32 encoding.\n\n## 🛠 Installing\n\n## poetry\n\n```\npoetry add python-zbase32\n```\n\n## pip\n\n```\npip install python-zbase32\n```\n\n## 🎓 Usage\n\n```pycon\n>>> import zbase32\n>>> zbase32.encode(b"asdasd")\n\'cf3seamuco\'\n>>> zbase32.decode("cf3seamu")\nb"asdas"\n```\n\n## 🔧  Development\n\n| Command           | Description                           |\n| ----------------- | ------------------------------------- |\n| `make bootstrap`  | install project dependencies          |\n| `make ci`         | run continuous integration tasks      |\n| `make console`    | open a repl console                   |\n| `make format`     | format all source files               |\n| `make setup`      | setup the project after a `git clone` |\n| `make test`       | run the applications test suite       |\n| `make update`     | update the project after a `git pull` |\n\n## ⚖️ Licence\n\nThis project is licensed under the [MIT licence](http://dan.mit-license.org/).\n\nAll documentation and images are licenced under the \n[Creative Commons Attribution-ShareAlike 4.0 International License][cc_by_sa].\n\n[cc_by_sa]: https://creativecommons.org/licenses/by-sa/4.0/\n\n## 📝 Meta\n\nThis project uses [Semantic Versioning](http://semver.org/).',
    'author': 'Daniel Knell',
    'author_email': 'contact@danielknell.co.uk',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/artisanofcode/python-zbase32',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
