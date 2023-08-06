from distutils.core import  setup
import setuptools
packages = ['openncv']# 唯一的包名，自己取名
setup(name='openncv',
	version='1.2',
	author='yy',
    packages=packages, 
    package_dir={'requests': 'requests'},)
