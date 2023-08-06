from setuptools import setup

# read the contents of README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'python-banqup-uc-api',         
  packages=['banqup_uc', 'banqup_uc.models', 'banqup_uc.constants', 'banqup_uc.cache', 'banqup_uc.endpoints'],
  version = '0.1.1',
  license='GPL-3.0-or-later',
  description = 'Wrapper for the BanqUP (UnifiedPost) Universal Connector API - v3',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Alexander Schillemans',
  author_email = 'alexander.schillemans@lhs.global',
  url = 'https://github.com/alexanderlhsglobal/python-banqup-uc-api',
  download_url = 'https://github.com/alexanderlhsglobal/python-banqup-uc-api/archive/refs/tags/0.1.1.tar.gz',
  keywords = ['bill-to-box', 'universal connector' 'api', 'banqup', 'unifiedpost', 'bill to box'],
  install_requires=[
          'requests',
          'oauthlib',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    'Programming Language :: Python :: 3.6',
  ],
)