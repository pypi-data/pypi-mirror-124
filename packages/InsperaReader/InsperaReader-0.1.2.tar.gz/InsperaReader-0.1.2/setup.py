import os
from setuptools import setup, find_packages
from pathlib import Path
desc = (Path(__file__).parent / "README.md").read_text()

setup(
    name = 'InsperaReader',
    packages = find_packages(),
    include_package_data=True,
    version = '0.1.2',
    description = 'JSON parsing of Inspera Assessment files',
    long_description=desc,
    long_description_content_type='text/markdown',
    author = 'Tollef Jørgensen',
    author_email = 'tollefj@gmail.com',
    license = 'MIT License: http://opensource.org/licenses/MIT',
    url = 'https://github.com/ph10m/inspera-reader',
    download_url = 'https://github.com/ph10m/inspera-reader',
    install_requires = [],
    keywords = ['JSON', 'Inspera', 'parser', 'dataset'],
    classifiers = [
        'Intended Audience :: Science/Research',
         'License :: OSI Approved :: MIT License',
         'Natural Language :: English',
         'Programming Language :: Python :: 3.5',
         'Topic :: Scientific/Engineering :: Information Analysis'
     ]
)
