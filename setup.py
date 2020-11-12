#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='speed-tracker',
      version='1.0',
      description='Check and save internet speed',
      author='Kyle Ramey',
      author_email='hello@kyleramey.dev',
      url='https://kyleramey.dev',
      packages=find_packages(),
      install_requires=['speedtest-cli', 'aiohttp', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib', 'python-dotenv']
      )
