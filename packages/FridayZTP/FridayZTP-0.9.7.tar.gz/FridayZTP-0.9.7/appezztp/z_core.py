#! /usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from .vtg_ezztp_inertia_register_tbm_ import *

def get_platform():
    return platform.platform()


def get_node():
    return platform.node()


def turboeasy_appztp():
    tbm = Application()
    tbm.create_widgets()


if __name__ == '__main__':
    pass
