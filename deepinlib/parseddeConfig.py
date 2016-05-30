#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt5.QtCore import QSettings

if 2 == sys.version_info.major:
    import ConfigParser as configparser
else:
    import configparser

class ddeconfig(object):
    '''
    获得桌面图标排序，数量少于一列
    '''
    def __init__(self):
        self.defaultpath = os.path.expanduser("~/.config/deepin/dde-desktop.conf")
        self.desktop_icon = configparser.ConfigParser()
        self.section = "DesktopItems"
        self.qsetting_conf = QSettings(self.defaultpath, QSettings.IniFormat)

    def getDesktopIconlist(self):
        self.desktop_icon.read(self.defaultpath)
        list = self.desktop_icon.items(self.section)
        dict = {}
        for i in list:
            name = i[0].split('\\')[-1]
            y = i[1].split()[-1].replace(')', ' ').split()[0]
            dict[int(y)] = name

        dictsort = sorted(dict.iteritems(), key= lambda d:d[0])
        rl = []
        for k, v in dictsort:
            rl.append(v)

        return rl

    def getDesktopIconlist2(self):
        self.qsetting_conf = QSettings(self.defaultpath, QSettings.IniFormat)
        dict = {}
        for i in self.qsetting_conf.allKeys():
            y = self.qsetting_conf.value(i).y()
            name = i.split('/')[-1]
            dict[int(y)] = name

        dictsort = sorted(dict.iteritems(), key = lambda d:d[0])
        rl = []
        for k, v in dictsort:
            rl.append(v)

        return rl

