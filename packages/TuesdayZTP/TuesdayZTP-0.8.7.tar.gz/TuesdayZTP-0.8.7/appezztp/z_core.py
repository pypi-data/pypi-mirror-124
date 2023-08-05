#! /usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from vtg_ezztp_inertia_register_tbm_ import *

def get_platform():
    '''获取操作系统名称及版本号'''
    return platform.platform()


def get_node():
    '''计算机的网络名称'''
    return platform.node()


def turboeasy_appztp():
    tbm = Application()
    tbm.create_widgets()


if __name__ == '__main__':
    pass
