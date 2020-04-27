from time import time
from tkinter import ttk

from matplotlib import style
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import solutionTechniuqes

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


style.use('ggplot')


class graphPlotter():

    def __init__(self, frame):
        self.frame = frame
        self.fig = Figure(figsize=(5, 5), dpi=80)
        self.plt = self.fig.add_subplot(1, 1, 1)

        # self.current = 0
        # self.xs = dict()
        # self.ys = dict()
        # self.xs[0] = np.arange(-3, 3, 0.2)
        # self.ys[0] = []
        # for num in self.xs[0]:
        #     self.ys[0].append(solutionTechniuqes.evaluate('pow(x,2)', num))

        # self.ys[0] = solutionTechniuqes.evaluate('pow(x,2)', self.xs[0])
        # self.xs[0] = [0, 1, 2, 3, 4]
        # self.ys[0] = [0, 7, 5, 9, 3]
        # self.xs[1] = [3, 5, 11, 15, 24]
        # self.ys[1] = [1, 4, 10, 6, 11]
        # self.plt.plot(self.xs[self.current], self.ys[self.current])

        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)

        self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
        self.toolbar.update()
        self.canvas.tkcanvas.pack(side=tk.TOP, expand=True)
        self.canvas.get_tk_widget().pack(side=tk.TOP, expand=True)

        self.tooltip_font = "TkDefaultFont"

        self.next_photo = tk.PhotoImage(file='Images/next.png')
        self.next_graph = ttk.Button(self.toolbar, image=self.next_photo)
        self.next_graph.pack(side=tk.RIGHT)
        self.next_graph.configure(command=self.next)
        self.next_graph.configure(width=2.5)
        ToolTip(self.next_graph, self.tooltip_font, 'Next Graph', delay=0.1)

        self.prev_photo = tk.PhotoImage(file='Images/prev.png')
        self.prev_graph = ttk.Button(self.toolbar, image=self.prev_photo)
        self.prev_graph.pack(side=tk.RIGHT)
        # next.configure(command=root_Finder_support.solve)
        self.prev_graph.configure(width=2.5)
        ToolTip(self.prev_graph, self.tooltip_font, 'Previous Graph', delay=0.1)

    def next(self):
        self.fig.clear()
        self.plt = self.fig.add_subplot(1, 1, 1)
        self.current = (self.current + 1) % 2
        self.plt.plot(self.xs[self.current], self.ys[self.current])
        self.canvas.draw()
        self.canvas.figure.set_canvas(self.canvas)



class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """
    def __init__(self, wdgt, tooltip_font, msg=None, msgFunc=None,
                 delay=1, follow=True):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg='black', padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set('No message provided')
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(self, textvariable=self.msgVar, bg='#FFFFDD',
                font=tooltip_font,
                aspect=1000).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind('<Enter>', self.spawn, '+')
        self.wdgt.bind('<Leave>', self.hide, '+')
        self.wdgt.bind('<Motion>', self.move, '+')

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry('+%i+%i' % (event.x_root+20, event.y_root-10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()
