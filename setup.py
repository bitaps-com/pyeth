#!/usr/bin/python3
# coding: utf-8

from setuptools import setup, find_packages


setup(name='pyeth',
      version='1.1',
      description='Python Ethereum library',
      keywords='ethereum',
      url='https://github.com/bitaps-com/pyeth',
      author='Nadezhda Karpova',
      author_email='nadyka@bitaps.com',
      license='GPL-3.0',
      packages=find_packages(),
      install_requires=['py-ecc==1.4.2','rlp==0.6.0','coincurve','pysha3==1.0.2'],
      include_package_data=True,
      package_data={
          'pyeth': ['bip39_word_list/*.txt'],
      },
      zip_safe=False)