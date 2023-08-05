
from setuptools import setup , find_packages

with open('README.md', 'r') as f:
      long_description = f.read()

setup(name='atomic_loop_pkg_test',
      version='0.2',
      description='this package provides the math functions',
      long_description=long_description,
      long_description_content_type = 'text/markdown',
      py_modules=['functions','greet'],
      requires=[],
      extras_requires = {
            'dev' : [
                  "pytest>=3.7"
            ]
      },
      url='https://github.com/LEO2822/python-package',
      author='Mangesh',
      author_email='mtkashid7@gmail.com',
      package_dir={'' : 'atomic_loop_pkg_test'},
      classifiers=["Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.6",
                   "Programming Language :: Python :: 3.7",
                   "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
                   "Operating System :: OS Independent"])