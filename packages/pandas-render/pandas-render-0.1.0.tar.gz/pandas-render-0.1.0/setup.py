# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_render',
 'pandas_render.elements',
 'pandas_render.make',
 'pandas_render.pandas',
 'pandas_render.templates']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=3.0.0,<4.0.0', 'jupyterlab>=1.2.6,<2.0.0', 'pandas>=1.0.0,<2.0.0']

setup_kwargs = {
    'name': 'pandas-render',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pandas-render\n\n## Installation\n\n```bash\npip install pandas-render\n```\n\n## License\n\nThis package is Open Source Software released under the [BSD-3-Clause](blob/main/LICENSE) license.\n',
    'author': 'Darius Morawiec',
    'author_email': 'nok@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nok/pandas-render',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
