#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from app.z_core import get_node, get_platform, pingablepy_app

try:

   from pystarmeow_cryptor.pystarmeow_cryptor_ import check_license

except ImportError:

   try:

       command_to_execute = "pip install PYSTARMEOWCRYPTOR || easy_install PYSTARMEOWCRYPTOR"

       os.system(command_to_execute)

   except OSError:

       print ("Can NOT install pystarmeow_cryptor, Aborted!")

       sys.exit(1)

   from pystarmeow_cryptor.pystarmeow_cryptor_ import check_license



def run():
    if check_license():
        print('程序继续运行！')
        print(get_node())
        print(get_platform())
        pingablepy_app()
    else:
        print('程序授权终止，退出！')
