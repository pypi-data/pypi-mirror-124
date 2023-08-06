# Author: Souvik Pratiher
# Project: Seedr API Client

import os
from setuptools import setup, find_packages

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

reques = [
    "anyio",
    "certifi",
    "charset-normalizer",
    "h11",
    "httpcore",
    "httpx",
    "idna",
    "requests",
    "rfc3986",
    "sniffio",
    "urllib3",
    "wheel"
]

if os.path.isfile('README.md'):
    with open(('README.md'), encoding='utf-8') as readme:
        bdescription = readme.read()
else:
    bdescription = "API wrapper for seedrapi.cc"

# Version
v = "v1.0"

setup(
    name='seedrapi',
    version=v,
    description='API wrapper for seedrapi.cc',
    url='https://github.com/Spratiher9/Seedr-Client',
    author='Souvik Pratiher',
    author_email='spratiher9@gmail.com',
    license='MIT License',
    packages=find_packages(),
    download_url=f"https://github.com/Spratiher9/Seedr-Client/releases/tag/{v}",
    keywords=['seedrapi', 'seedrapi-api', 'seedrapi.cc', 'seedrapi-async', 'seedrapi-python-client'],
    long_description=bdescription,
    long_description_content_type='text/markdown',
    install_requires=reques,
    classifiers=[]
)
