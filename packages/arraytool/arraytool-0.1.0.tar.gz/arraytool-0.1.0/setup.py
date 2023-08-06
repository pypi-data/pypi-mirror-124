# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 23:10:03 2021

@author: ycchen
"""

# arraytool生成文件，陈杨城，yondersky@126.com，2021-10-13
# 更新日期：2021-10-22

from distutils.core import setup

setup(
    name = 'arraytool',
    version = '0.1.0',
    description = '基于numpy的Series及DataFrame数据结构',
    author = '陈杨城',
    author_email = 'yondersky@126.com',
    url = 'https://gitee.com/yonder_sky/arraytool',
    py_modules = ['arraytool.core','arraytool.pytool']
)
