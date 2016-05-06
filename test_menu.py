#!/usr/bin/env python
# -*- coding: utf-8 -*-

# PyUserInput
from pymouse import PyMouse
from pykeyboard import PyKeyboard
from time import sleep
import Xlib.display
import os
import dbus
import unittest
from collections import namedtuple
Desktop_obj = namedtuple('Desktop_obj','name')

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
    sleep(1)

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

    @classmethod
    def tearDownClass(cls):
        cleardesktop()

    def setUp(self):
        cleardesktop()

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

def suite():
    suite = unittest.TestSuite()
    suite.addTest(testdesktopmenu('testdesktopmenufolder'))
    return suite

if __name__ == "__main__":
    unittest.main(defaultTest = 'suite')
