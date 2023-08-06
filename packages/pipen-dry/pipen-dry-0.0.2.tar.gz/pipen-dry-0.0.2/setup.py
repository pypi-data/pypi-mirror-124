# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['pipen_dry']
install_requires = \
['pipen>=0.2,<0.3']

entry_points = \
{'pipen': ['dry = pipen_dry:PipenDry'],
 'pipen_sched': ['dry = pipen_dry:PipenDryScheduler']}

setup_kwargs = {
    'name': 'pipen-dry',
    'version': '0.0.2',
    'description': 'Dry runner for pipen pipelines',
    'long_description': None,
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
