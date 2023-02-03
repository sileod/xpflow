from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='xpflow',
      version='{{VERSION_PLACEHOLDER}}',
      description='Utilities for representing experiments with classes',
      url='https://github.com/sileod/xpflow',
      author='sileod',
      license='MIT',
      install_requires=['easydict','sorcery'],
      py_modules=['xpflow'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
