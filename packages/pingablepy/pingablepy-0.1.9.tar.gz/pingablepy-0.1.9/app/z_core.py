# !/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
from time import sleep
import sys, traceback
from app.wgbridge.liyuan.restinterface.wholotus.pingable_console_ import *
import pathlib
import re
from vtg_alarms_weakauth_ import *

def server_list_object_pickup(name):
    HERE = pathlib.Path(__file__).parent.parent
    buf = ( HERE / "__init__.py" ).read_text()
    slo1 = buf.find(name) + len(f"{name} = ")
    slo2 = buf[slo1:].find("]") + 1
    slo_ = buf[slo1:slo1 + slo2]
    p1 = re.compile("'(.*?)'", re.S)
    return (re.findall(p1, slo_))


def get_platform():
    return platform.platform()


def get_node():
    return platform.node()


def pingablepy_app():
    try:
        while True:
            server_list_object = server_list_object_pickup('__server_list_object__')
            print(server_list_object)
            errlistobj = pingable_console_(server_list_object)
            if [] != errlistobj:
                ala = VTG_alarms()
                alarmprint_content_critical_(ala, errlistobj)
                print(" - Alarmprinted")
            # sleep(60 * 60)
            sleep(1 * 1)
    except:
        print(traceback.format_exc())


