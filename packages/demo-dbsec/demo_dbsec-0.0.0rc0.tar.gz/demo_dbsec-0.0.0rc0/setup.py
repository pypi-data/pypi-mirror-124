from setuptools import setup

name_package = 'demo_dbsec'
version = '0.0.0rc0'
install_requires = ['PyQt5']
description = 'Demo SQL Injection sharing resource'
package_dir = 'src/'
author='GROUP 4 from Class Database Security'
author_email='tquang.sdh20@hcmut.edu.vn'
url= 'https://github.com/tquangsdh20/demo_sql_injection'

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
from io import open
with open("README.md",'r',encoding='utf-8') as fh:
    long_description = fh.read()

keywords = [name_package,]

classifiers = [
    'Intended Audience :: Education',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Developers',
    'Intended Audience :: End Users/Desktop',
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
]

setup(
    name = name_package,
    version = version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=author,
    author_email=author_email,
    url=url,
    classifiers = classifiers,
    package_dir={'': package_dir[0:len(package_dir)-1]},
    install_requires = install_requires,
    include_package_data=True,
    license= 'MIT',
    keywords=keywords,
)
