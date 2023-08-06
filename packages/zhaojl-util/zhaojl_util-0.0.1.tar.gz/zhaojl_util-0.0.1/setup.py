# coding: utf-8

from setuptools import setup

setup(
    name='zhaojl_util',
    version='0.0.1',
    author='jialiang',
    author_email='dreamforcode@foxmail.com',
    url='',
    description=u'常用工具包',
    packages=['zhaojl_util'],
    install_requires=['base64', 'fitz', 'os', 'glob', 'shutil'],
    entry_points={
        'console_scripts': [
            'hello = zhaojl_util:.test.main'
        ]
    }
)