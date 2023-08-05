#! /usr/bin/env python
# -*- coding: utf-8 -*-

from appezztp.z_core import get_node, get_platform, turboeasy_appztp
from pystarmeow_cryptor_ import check_license


def run():
    if check_license():
        print('程序继续运行！')
        print(get_node())
        print(get_platform())
        turboeasy_appztp()
    else:
        print('程序授权终止，退出！')
