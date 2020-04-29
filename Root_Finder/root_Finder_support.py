#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# Support module generated by PAGE version 5.0.3
#  in conjunction with Tcl version 8.6
#    Apr 15, 2020 05:32:31 PM +0200  platform: Windows NT

import sys
from decimal import Decimal

from numpy import double

import solutionTechniuqes as st
import graphPlotter as gp

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
    global check68
    check68 = tk.BooleanVar()
    global expression
    expression = tk.StringVar()
    global iter
    iter = tk.StringVar()
    global precision
    precision = tk.StringVar()
    global upper
    upper = tk.StringVar()
    global lower
    lower = tk.StringVar()
    global guess1
    guess1 = tk.StringVar()
    global guess2
    guess2 = tk.StringVar()


def init(top, gui, *args, **kwargs):
    global w, top_level, root
    w = gui
    top_level = top
    root = top


def solve(txt, gph):
    txt.delete("1.0", tk.END)
    method = combobox.get()
    try:
        answer = None
        exp = expression.get()
        i = int(iter.get())
        pre = double(precision.get())
        num_digits = abs(Decimal(precision.get()).as_tuple().exponent)
        if method == 'Bisection method' or method == 'Regula-Falsi method':
            low = double(lower.get())
            up = double(upper.get())
            solver = st.solution_techinques(exp)
            if method == 'Bisection method':
                answer = solver.bisection(up, low, pre, i, num_digits)
            else:
                answer = solver.regulafalsi(up, low, pre, i, num_digits)
            print_indirect(txt, answer)
            plot = gp.graphPlotter(gph, 0, answer, solver)
        elif method == 'Fixed point iteration method':
            pass
        else:
            pass
    except:
        txt.insert(tk.END, 'Wrong input format')
    sys.stdout.flush()


def print_indirect(console, answer):
    console.insert(tk.END, 'Calculated root: {}\n\n'.format(answer[0][len(answer[0]) - 1]))
    console.insert(tk.END, 'Iter\t(Upper, Lower) Bounds\t\tAccuracy\n')
    i = 0
    for bound in answer[1]:
        if i == 0:
            console.insert(tk.END, '{}\t({}, {})\t\t\t---\n'.format(i+1, bound[0], bound[1]))
        else:
            console.insert(tk.END, '{}\t({}, {})\t\t\t{}\n'.format(i+1, bound[0], bound[1], answer[2][i-1]))
        i += 1


def check():
    root_Finder
    print('root_Finder_support.check')
    sys.stdout.flush()


def destroy_window():
    # Function which closes the window.
    global top_level
    top_level.destroy()
    top_level = None


if __name__ == '__main__':
    import root_Finder

    root_Finder.vp_start_gui()
