from setuptools import setup

long_description = (this_directory / "README.md").read_text()

setup(name='xpflow',
      version='0.2',
      description='Utilities for representing experiments with classes',
      url='https://github.com/sileod/xpflow',
      author='sileod',
      license='MIT',
      install_requires=['easydict'],
      download_url='https://github.com/sileod/xpflow/archive/refs/tags/v0.tar.gz',
      py_modules=['xpflow'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)
