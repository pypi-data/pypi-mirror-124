# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['manim_fontawesome']

package_data = \
{'': ['*'],
 'manim_fontawesome': ['font-awesome/*',
                       'font-awesome/svgs/brands/*',
                       'font-awesome/svgs/regular/*',
                       'font-awesome/svgs/solid/*']}

install_requires = \
['manim>=0.3']

entry_points = \
{'manim.plugins': ['manim_fontawesome = manim_fontawesome']}

setup_kwargs = {
    'name': 'manim-fontawesome',
    'version': '5.15.4',
    'description': "Font Awesome SVG's for Manim",
    'long_description': None,
    'author': 'Naveen M K',
    'author_email': 'naveen@manim.community',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/naveen521kk/manim-fontawesome',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
