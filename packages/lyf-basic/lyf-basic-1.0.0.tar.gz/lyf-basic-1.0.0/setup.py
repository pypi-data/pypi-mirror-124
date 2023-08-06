# -*- coding:utf-8 -*-

# !/usr/bin/python
from distutils.core import setup

setup(
    # 库的基本信息
    name="lyf-basic",  # 这里是pip项目发布的名称
    version="1.0.0",  # 版本号，数值大的会优先被pip
    keywords=["init", "lyf"],
    description="lyf-test",
    long_description="test",
    license="MIT Licence",

    # 作者的基本信息
    author="lyf",
    author_email="lyf23william@gmail.com",
    url="https://gitee.com/guoyasoft/guoya-api.git",  # 项目相关文件地址，一般是github

    # 发布的代码
    # data_files =['tool/random_tool.py'], # 发布的文件清单
    packages=['integration-test'],  # 发布的包清单
    platforms="python",

    # 依赖的第三方库列表
    install_requires=[
        'pytest==6.2.5',
        'requests==2.25.1'
    ]
)