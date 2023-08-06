from setuptools import setup, find_packages
import os
pkgs=list(filter(None, [x[0].replace('{}/'.format(os.getcwd()), '').replace('/','.') if '.git' not in x[0] else '' for x in os.walk('{}/'.format(os.getcwd()))]))
setup(
    name='pyziplux',
    version='2021.10.0.12',
    license='MIT',
    author="Ziplux LHS",
    author_email='ziplux.so@ziplux.so',
    packages=find_packages(include=pkgs),
    package_dir={'': 'pyziplux'},
    url='https://github.com/ZipluxLhs/pyziplux',
    keywords='middleware',
    install_requires=[
           'pip',
	  'setuptools',
    	  'wheel',
           'et_xmlfile',
      ],

)