#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  PyUserInput
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep
from Xlib.display import Display
from Xlib import X
import gtk
import wnck
import os
import sys
import dbus
import psutil
import shutil
import unittest
from collections import namedtuple
Desktop_obj = namedtuple('Desktop_obj','name')

sys.path.append(".")
# 加入自己的lib
from deepinlib.parseddeConfig import ddeconfig

k = PyKeyboard()
m = PyMouse()

resolution = Display().screen().root.get_geometry()
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
else:
    english = True
    desktoppath = os.path.expanduser('~') + '/' + 'Desktop/*'

print("Language type is %s" % os.getenv("LANG"))
print("desktoppath is %s" % desktoppath)

def keyComWin(key):
    k.press_key(k.windows_l_key)
    k.press_key(key)
    k.release_key(key)
    k.release_key(k.windows_l_key)
    sleep(3)

def mouseClickR(x, y):
    m.click(x, y, 2)
    sleep(2)

def mouseClickRight():
    mouseClickR(screen_width*relative_rate, screen_height*relative_rate)

def mouseClickL(x, y):
    m.click(x, y)
    sleep(2)

def mouseCLickLeft():
    mouseClickL(screen_width*relative_rate, screen_height*relative_rate)

def keyTypeStr(str):
    k.type_string(str)
    sleep(2)

def keySingle(key):
    k.press_key(key)
    k.release_key(key)
    sleep(2)

def desktoplist():
    desktopdict = session_iface.GetDesktopItems()
    dl = []
    for (k, v) in desktopdict.items():
        dl.append(v[1])
    return dl

def cleardesktop():
    os.system("rm -rf %s" % desktoppath.encode('utf-8'))

class Waitter(object):
    def __init__(self, display):
        self.display = display
        self.root = self.display.screen().root
        self.root.change_attributes(event_mask = X.SubstructureNotifyMask)

    def loop(self, w_name):
        while True:
            sleep(5)
            screen = wnck.screen_get_default()
            while gtk.events_pending():
                gtk.main_iteration()

            for window in screen.get_windows():
                print(window.get_name())
                if w_name == window.get_name():
                    return True

    def isTaskExist(self, name):
        return isTaskExist(name)

def isTaskExist(name):
    for pid in psutil.pids():
        p = psutil.Process(pid)
        if p.name() == name:
            return True
    return False

def clickNewfolder():
    mouseClickRight()
    keySingle(k.down_key)
    keySingle(k.enter_key)

def clickNewExcel():
    if True == english:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

    if True == chinese:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

def clickNewPowerPoint():
    if True == english:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

    if True == chinese:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

def clickNewText():
    if True == english:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

    if True == chinese:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

def clickNewWord():
    if True == english:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

    if True == chinese:
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)

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
        clickNewfolder()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u"新建文件夹"])

        if True == english:
            self.assertListEqual(filelist, ["New folder"])

        sleep(1)
        clickNewfolder()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u"新建文件夹", u"新建文件夹 2"])

        if True == english:
            self.assertListEqual(filelist, ["New folder", "New folder 2"])

    def testdesktopmenuNewtxt(self):
        clickNewText()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'文本.txt'])

        if True == english:
            self.assertListEqual(filelist, ['Text.txt'])

        sleep(1)
        clickNewText()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'文本.txt', u'文本 2.txt'])

        if True == english:
            self.assertListEqual(filelist, ['Text.txt', 'Text 2.txt'])

    def testdesktopmenuNewdoc(self):
        clickNewWord()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'文档.doc'])

        if True == english:
            self.assertListEqual(filelist, ['Word.doc'])

        sleep(1)
        clickNewWord()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'文档.doc', u'文档 2.doc'])

        if True == english:
            self.assertListEqual(filelist, ['Word.doc', 'Word 2.doc'])

    def testdesktopmenuNewppt(self):
        clickNewPowerPoint()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'演示.ppt'])

        if True == english:
            self.assertListEqual(filelist, ['PowerPoint.ppt'])

        sleep(1)
        clickNewPowerPoint()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'演示.ppt', u'演示 2.ppt'])

        if True == english:
            self.assertListEqual(filelist, ['PowerPoint.ppt', 'PowerPoint 2.ppt'])

    def testdesktopmenuNewxls(self):
        clickNewExcel()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'表格.xls'])

        if True == english:
            self.assertListEqual(filelist, ['Excel.xls'])

        sleep(1)
        clickNewExcel()
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'表格.xls', u'表格 2.xls'])

        if True == english:
            self.assertListEqual(filelist, ['Excel.xls', 'Excel 2.xls'])

    def testdesktopmenuSortname(self):
        shutil.copy('./data/small.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/big.txt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'small.txt', u'big.txt'])

        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist2()
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
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'big.txt', u'small.txt'])

    def testdesktopmenuSorttype(self):
        shutil.copy('./data/test.xls', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.ppt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'test.xls', u'test.txt', u'test.ppt'])
        
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'test.ppt', u'test.txt', u'test.xls'])

    def testdesktopmenuSortmodifydate(self):
        shutil.copy('./data/test.xls', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.txt', self.desktoppath)
        sleep(2)
        shutil.copy('./data/test.ppt', self.desktoppath)
        sleep(2)
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'test.xls', u'test.txt', u'test.ppt'])

        shutil.copy('./data/test.txt', self.desktoppath)
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        filelist = self.ddeconfig.getDesktopIconlist2()
        self.assertListEqual(filelist, [u'test.xls', u'test.ppt', u'test.txt'])

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
        filelist = self.ddeconfig.getDesktopIconlist2()
        if True == chinese:
            self.assertListEqual(filelist, [u'copy.txt', u'copy（复件）.txt'])

    def testdesktopmenuDisplaysetting(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        rt = Waitter(Display()).isTaskExist("dde-control-center")
        self.assertTrue(rt)
        mouseCLickLeft()

    def testdesktopmenuCornernavi(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        rt = Waitter(Display()).isTaskExist("dde-zone")
        self.assertTrue(rt)
        mouseCLickLeft()

    def testdesktopmenuPersonnality(self):
        mouseClickRight()
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.left_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.down_key)
        keySingle(k.enter_key)
        rt = Waitter(Display()).isTaskExist("dde-control-center")
        self.assertTrue(rt)
        mouseCLickLeft()


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
    suite.addTest(testdesktopmenu('testdesktopmenuDisplaysetting'))
    suite.addTest(testdesktopmenu('testdesktopmenuCornernavi'))
    suite.addTest(testdesktopmenu('testdesktopmenuPersonnality'))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')
