# coding=utf-8
# @Author:Hunter_talk

from distutils.core import setup
from setuptools import find_packages

with open("README.rst", "r",encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="HunterOakley_package",  # 包名
    version="1.0.0",  # 版本号
    long_description=long_description,  # 简单的描述信息
    author="Hunter_talk",
    author_email="1608477018@qq.com",
    url="https://gitee.com/the-flowers-are-still-blooming",
    install_requires=[],
    license='BSD License',
    packages=find_packages(),
    platforms=["all"],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries'
    ],
)
