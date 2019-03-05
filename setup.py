"""Basic seup for entry points."""
from setuptools import setup

setup(name='trim',
      version='0.1',
      description='Sync and trim video.',
      author='Dave Greenwood',
      py_modules=['times', 'trim'],
      zip_safe=False,
      entry_points={'console_scripts': [
          'trim=trim:main',
      ]}
      )
