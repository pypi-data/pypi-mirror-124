"""
Setup module for install lib
"""
import os
import re
from os import path
from pathlib import Path
from typing import List, Optional

from setuptools import setup

LIB_NAME = 'gen_doc'
HERE = Path(__file__).parent

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


def get_version() -> Optional[str]:
    """
      Method for getting the version of the library from the init file
    :requirements: version must be specified separately
        :good: __version__ = '0.0.1'
        :bad: __version__, __any_variable__ = '0.0.1', 'any_value'
    :return: version lib
    """

    txt = (HERE / LIB_NAME / "__init__.py").read_text("utf-8")
    txt = txt.replace("'", '"')
    try:
        version = re.findall(r'^__version__ = "([^"]+)"\r?$', txt, re.M)[0]
        return version
    except IndexError:
        raise RuntimeError("Unable to determine version.")


def get_packages() -> List[str]:
    """
    Help method
    :return: List[str] path to files and folders library
    """
    ignore = ['__pycache__']

    list_sub_folders_with_paths = [x[0].replace(os.sep, '.')
                                   for x in os.walk(LIB_NAME)
                                   if x[0].split(os.sep)[-1] not in ignore]
    return list_sub_folders_with_paths


setup(name=LIB_NAME,
      version=get_version(),
      description='Module for build documentation',
      author='Denis Shchutkiy',
      long_description=long_description,
      long_description_content_type='text/markdown',
      author_email='denisshchutskyi@gmail.com',
      url='https://github.com/Shchusia/gen_doc',
      packages=get_packages(),
      keywords=['pip', LIB_NAME],
      python_requires='>=3.7',
      entry_points={
          'console_scripts': [
              'gen_doc=gen_doc.commands:main'

          ]},
      )
