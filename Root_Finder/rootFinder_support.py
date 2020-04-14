#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Apr 13, 2020 05:02:18 PM +0200  platform: Windows NT

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

def set_Tk_var():
    global combobox
    combobox = tk.StringVar()
    global tch112
    tch112 = tk.StringVar()

def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top

def cosFormat():
    print('rootFinder_support.cosFormat')
    sys.stdout.flush()

def exitFunc():
    print('rootFinder_support.exitFunc')
    sys.stdout.flush()

def expFormat():
    print('rootFinder_support.expFormat')
    sys.stdout.flush()

def helpFunc():
    print('rootFinder_support.helpFunc')
    sys.stdout.flush()

def loadFunc():
    print('rootFinder_support.loadFunc')
    sys.stdout.flush()

def logFormat():
    print('rootFinder_support.logFormat')
    sys.stdout.flush()

def piFormat():
    print('rootFinder_support.piFormat')
    sys.stdout.flush()

def rootFormat():
    print('rootFinder_support.rootFormat')
    sys.stdout.flush()

def saveFunc():
    print('rootFinder_support.saveFunc')
    sys.stdout.flush()

def sinFormat():
    print('rootFinder_support.sinFormat')
    sys.stdout.flush()

def tanFormat():
    print('rootFinder_support.tanFormat')
    sys.stdout.flush()

def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None

if __name__ == '__main__':
    import rootFinder
    rootFinder.vp_start_gui()



