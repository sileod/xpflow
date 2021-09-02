from setuptools import setup

long_description = (this_directory / "README.md").read_text()

setup(name='xpflow',
      version='0.1',
      description='Utilities for representing experiments with classes',
      url='https://github.com/sileod/xpflow',
      author='sileod',
      license='MIT',
      py_modules=['xpflow'],
      install_requires=['easydict'],
      long_description=long_description,
      long_description_content_type='text/markdown'
      zip_safe=False)
