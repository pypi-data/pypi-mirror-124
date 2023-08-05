# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['makefilelicense']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.26.0,<3.0.0', 'toml[tomli]>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['license-agpl = '
                     'incolumepy.makefilelicense.licenses:license_agpl',
                     'license-apache = '
                     'incolumepy.makefilelicense.licenses:license_apache',
                     'license-bsl = '
                     'incolumepy.makefilelicense.licenses:license_bsl',
                     'license-gpl = '
                     'incolumepy.makefilelicense.licenses:license_gpl',
                     'license-lgpl = '
                     'incolumepy.makefilelicense.licenses:license_lgpl',
                     'license-mit = '
                     'incolumepy.makefilelicense.licenses:license_mit',
                     'license-mpl = '
                     'incolumepy.makefilelicense.licenses:license_mpl',
                     'unlicense = '
                     'incolumepy.makefilelicense.licenses:unlicense']}

setup_kwargs = {
    'name': 'incolumepy.makefilelicense',
    'version': '0.1.3',
    'description': '',
    'long_description': '# Makefile License Incolume Python\n\n---\nThis software take a License and agregate into the project.\n\n## pip Install\n```bash\npip install incolumepy.makefilelicense\n```\n## poetry Install\n```bash\npoetry add incolumepy.makefilelicense\n```\n## source\n1. Choice the source on https://github.com/incolumepy/incolumepy.makefilelicense/tags;\n2. unzip your package;\n3. cd incolumepy.makefilelicense-x.y.z;\n4.\n\n## Command make\n```bash\nmake setup\nmake [license-agpl license-apache license-bsl license-gpl \\\n      license-lgpl license-mit license-mpl]\n```\n',
    'author': 'Britodfbr',
    'author_email': 'britodfbr@gmail.com',
    'maintainer': 'Britodfbr',
    'maintainer_email': 'britodfbr@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
