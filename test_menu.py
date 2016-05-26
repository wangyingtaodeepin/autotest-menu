#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyUserInput
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep
import Xlib.display
import os
import sys
import dbus
import shutil
import unittest
from collections import namedtuple
Desktop_obj = namedtuple('Desktop_obj','name')

sys.path.append(".")
# 加入自己的lib
from deepinlib.parseddeConfig import ddeconfig

k = PyKeyboard()
m = PyMouse()

resolution = Xlib.display.Display().screen().root.get_geometry()
screen_width = resolution.width
screen_height = resolution.height
relative_rate = 0.5
lang = os.getenv('LANG')
chinese = False
english = False
session_bus = dbus.SessionBus()
session_obj = session_bus.get_object('com.deepin.dde.daemon.Desktop',
                                     '/com/deepin/dde/daemon/Desktop')
session_iface = dbus.Interface(session_obj, dbus_interface='com.deepin.dde.daemon.Desktop')

desktoppath = ''
if 'zh_CN.UTF-8' == lang:
    chinese = True
    desktoppath = os.path.expanduser('~') + '/' + u'桌面/*'
elif 'en_US.UTF-8' == lang:
    english = True
    desktoppath = os.path.expanduser('~') + '/' + 'Desktop/*'

def keyComWin(key):
    k.press_key(k.windows_l_key)
    k.press_key(key)
    k.release_key(key)
    k.release_key(k.windows_l_key)
    sleep(3)

def mouseClickR(x, y):
    m.click(x, y, 2)
    sleep(1)

def mouseClickRight():
    mouseClickR(screen_width*relative_rate, screen_height*relative_rate)

def mouseClickL(x, y):
    m.click(x, y)
    sleep(2)

def keyTypeStr(str):
    k.type_string(str)
    sleep(1)

def keySingle(key):
    k.press_key(key)
    k.release_key(key)
    sleep(1)

def desktoplist():
    desktopdict = session_iface.GetDesktopItems()
    dl = []
    for (k, v) in desktopdict.items():
        dl.append(v[1])
    return dl

def cleardesktop():
    os.system("rm -rf %s" % desktoppath.encode('utf-8'))

class testdesktopmenu(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cleardesktop()
        cls.ddeconfig = ddeconfig()

    @classmethod
    def tearDownClass(cls):
        cleardesktop()

    def setUp(self):
        cleardesktop()
        self.desktoppath = desktoppath[:-1]

    def tearDown(self):
        cleardesktop()

    def testdesktopmenufolder(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u"新建文件夹"])

        sleep(1)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), sorted([u"新建文件夹", u"新建文件夹 2"]))

    def testdesktopmenuNewtxt(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'文本.txt'])

        sleep(1)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'文本 2.txt', u'文本.txt'])

    def testdesktopmenuNewdoc(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'文档.doc'])

        sleep(1)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'文档 2.doc', u'文档.doc'])

    def testdesktopmenuNewppt(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'演示.ppt'])

        sleep(1)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'演示 2.ppt', u'演示.ppt'])

    def testdesktopmenuNewxls(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'表格.xls'])

        sleep(1)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = desktoplist()
        if True == chinese:
            self.assertListEqual(sorted(filelist), [u'表格 2.xls', u'表格.xls'])

    def testdesktopmenuSortname(self):
        shutil.copy('./data/small.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/big.txt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'small.txt', u'big.txt'])

        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'big.txt', u'small.txt'])

    def testdesktopmenuSortsize(self):
        shutil.copy('./data/small.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/big.txt', self.desktoppath)
        sleep(2)
        filelist= self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'small.txt', u'big.txt'])

        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'big.txt', u'small.txt'])

    def testdesktopmenuSorttype(self):
        shutil.copy('./data/test.xls', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.ppt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'test.xls', u'test.txt', u'test.ppt'])
        
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist()
        self.assertListEqual(filelist, [u'test.ppt', u'test.txt', u'test.xls'])

    def testdesktopmenuSortmodifydate(self):
        shutil.copy('./data/test.xls', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.ppt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist()

    def testdesktopmenuPaste(self):
        shutil.copy('./data/copy.txt', self.desktoppath)
        sleep(2)
        mouseClickR(20, 20)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        sleep(2)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist()
        if True == chinese:
            self.assertListEqual(filelist, [u'copy.txt', u'copy（复件）.txt'])

def suite():
    suite = unittest.TestSuite()
    suite.addTest(testdesktopmenu('testdesktopmenufolder'))
    suite.addTest(testdesktopmenu('testdesktopmenuNewtxt'))
    suite.addTest(testdesktopmenu('testdesktopmenuNewdoc'))
    suite.addTest(testdesktopmenu('testdesktopmenuNewppt'))
    suite.addTest(testdesktopmenu('testdesktopmenuNewxls'))
    suite.addTest(testdesktopmenu('testdesktopmenuSortname'))
    suite.addTest(testdesktopmenu('testdesktopmenuSortsize'))
    suite.addTest(testdesktopmenu('testdesktopmenuSorttype'))
    suite.addTest(testdesktopmenu('testdesktopmenuSortmodifydate'))
    suite.addTest(testdesktopmenu('testdesktopmenuPaste'))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')
