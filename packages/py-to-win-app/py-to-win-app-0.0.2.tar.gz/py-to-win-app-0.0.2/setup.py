# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_to_win_app']

package_data = \
{'': ['*']}

install_requires = \
['gen-exe>=0.2.1,<0.3.0',
 'requests>=2.26.0,<3.0.0',
 'tomli>=1.2.1,<2.0.0',
 'txtoml>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'py-to-win-app',
    'version': '0.0.2',
    'description': 'Make runnable apps from your python scripts!',
    'long_description': '# py-to-win-app\n\n## Make runnable apps from your python scripts!\n\nTODO: description\n\n## Installation\n\nInstall as dev dependency:\n\n    poetry add --dev py-to-win-app\n\nOr using pip:\n\n    pip install py-to-win-app\n\n## Usage\n\n1. Make `requirements.txt` file:\n\n    `pip freeze > requirements.txt`\n\n    Using `poetry`:\n\n    `poetry export -f requirements.txt -o requirements.txt --without-hashes`\n\n1. In root directory of your project create file `build.py` with following content:\n\n    ```python\n    from py_to_win_app import Project\n\n    project = Project(\n        input_dir="my_project",  # directory where your source files are\n        main_file="main.py"\n    )\n\n    project.build(python_version="3.9.7")\n    project.make_dist()\n    ```\n\n1. Run `build.py`:\n\n    `python build.py`\n\n## Documentation\n\n- [API documentation](http://ruslan.rv.ua/py-to-win-app/)\n\n## Examples\n\n1. Clone this repo:\n\n    `git clone https://github.com/ruslan-rv-ua/py2winapp`\n\n1. Execute any of `example-*.py`:\n\n    ```\n    python example-flask-desktop.py\n    ```\n\n    You can find runnable windows application in `build/flask-desktop` directory.\n    Distribution `flask-desktop.zip`\n\n#### More examples:\n\n- [telecode](https://github.com/ruslan-rv-ua/telecode) — desktop wxPython application\n\n## Credits\n\n- inspired by [ClimenteA/pyvan](https://github.com/ClimenteA/pyvan#readme)\n- some examples from [ClimenteA/flaskwebgui](https://github.com/ClimenteA/flaskwebgui)\n',
    'author': 'Ruslan Iskov',
    'author_email': 'ruslan.rv.ua@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ruslan-rv-ua/py-to-win-app',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
