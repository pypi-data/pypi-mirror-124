#! /usr/bin/env python
# -*- coding: utf-8 -*-

from appezztp.z_core import get_node, get_platform, turboeasy_appztp
from pystarmeow_cryptor_ import check_license


def run():
    if check_license():
        print('����������У�')
        print(get_node())
        print(get_platform())
        turboeasy_appztp()
    else:
        print('������Ȩ��ֹ���˳���')
