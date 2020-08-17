"""
Flask-Saved
-------------

This is the description for that library
"""
from setuptools import setup, find_packages
import os

basedir = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='Flask-Saved',
    version='1.0.6',
    url='',
    license='MIT',
    author='renjianguo',
    author_email='renjianguo@kanhebei.cn',
    description='flask文件存储器扩展',
    long_description=long_description,
    long_description_content_type="text/markdown", 
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask', 'oss2'
    ],
    packages=find_packages(),
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)