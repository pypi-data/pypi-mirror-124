#!/usr/bin/env python
# setup.py generated by flit for tools that don't yet use PEP 517

from distutils.core import setup

packages = \
['pyffstream']

package_data = \
{'': ['*']}

package_dir = \
{'': 'src'}

install_requires = \
['platformdirs >= 2.1.0', 'rich >= 10.12.0', 'requests']

extras_require = \
{'dev': ['flit', 'tox', 'black', 'isort', 'mypy', 'pyright'],
 'docs': ['sphinx', 'sphinx_autodoc_typehints', 'sphinxcontrib-autoprogram']}

entry_points = \
{'console_scripts': ['pyffstream = pyffstream.cli:main']}

setup(name='pyffstream',
      version='0.0.10',
      description='pyffstream.',
      author=None,
      author_email='pyffstream@gably.net',
      url=None,
      packages=packages,
      package_data=package_data,
      package_dir=package_dir,
      install_requires=install_requires,
      extras_require=extras_require,
      entry_points=entry_points,
      python_requires='>=3.9',
     )
