#! /usr/bin/env python
# -*- coding: utf-8 -*-

# from appezztp.z_core import get_node, get_platform, turboeasy_appztp
# from pystarmeow_cryptor_ import check_license


def run():
    if check_license():
        print('The program continues to run!')
        # print(get_node())
        # print(get_platform())
        # turboeasy_appztp()
    else:
        print('The program exit because of the authorization terminated!')
