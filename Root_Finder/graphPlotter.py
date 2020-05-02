from time import time
from tkinter import ttk

from matplotlib import style
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_pdf import PdfPages

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

style.use('ggplot')


class graphPlotter():

    def __init__(self, frame, method, answer, solver, check, filename):
        self.check = check
        self.frame = frame
        self.fig = Figure(figsize=(5, 5), dpi=80)
        self.plt = self.fig.add_subplot(1, 1, 1)

        self.current = 0
        self.xs = dict()
        self.ys = dict()

        self.solver = solver
        self.method = method

        if self.method == 0:
            '''indirect methods'''
            self.bounds = answer[1]
            self.fx = np.arange(self.bounds[0][0] - 3, self.bounds[0][1] + 3, 0.2)
            self.fy = np.array([self.solver.evaluate(num) for num in self.fx])
            self.plot_indirect()
        else:
            '''direct method'''
            self.guesses = answer[1]
            self.xes = answer[0]
            self.unit_x = None
            self.unit_y = None
            self.plot_direct()

        self.plt.axhline(y=0, color='k', label='X-Axis')
        self.plt.axvline(x=0, color='k', label='Y-Axis')
        self.plt.legend(loc="upper right")

        if self.check:
            pdf = PdfPages(filename)
            pdf.savefig(self.fig)
            i = 0
            if self.method == 0:
                while i != len(self.bounds)-1:
                    self.next()
                    pdf.savefig(self.fig)
                    i += 1
            else:
                while i != len(self.guesses)-1:
                    self.next()
                    pdf.savefig(self.fig)
                    i += 1
            pdf.close()
        else:
            self.canvas = FigureCanvasTkAgg(self.fig, self.frame)

            self.toolbar = NavigationToolbar2Tk(self.canvas, self.frame)
            self.toolbar.update()
            self.canvas.get_tk_widget().pack(side=tk.TOP, expand=True)
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
            self.prev_graph.configure(command=self.prev)
            self.prev_graph.configure(width=2.5)
            ToolTip(self.prev_graph, self.tooltip_font, 'Previous Graph', delay=0.1)

    def next(self):
        self.fig.clear()
        self.plt = self.fig.add_subplot(1, 1, 1)
        if self.method == 0:
            self.current = (self.current + 1) % len(self.bounds)
            self.plot_indirect()
        else:
            self.current = (self.current + 1) % len(self.guesses)
            self.plot_direct()
        self.plt.axhline(y=0, color='k', label='X-Axis')
        self.plt.axvline(x=0, color='k', label='Y-Axis')
        self.plt.legend(loc="upper right")
        if not self.check:
            self.canvas.draw()
            self.canvas.figure.set_canvas(self.canvas)

    def prev(self):
        self.fig.clear()
        self.plt = self.fig.add_subplot(1, 1, 1)
        if self.method == 0:
            if self.current == 0:
                self.current = len(self.bounds) - 1
            else:
                self.current -= 1
            self.plot_indirect()
        else:
            if self.current == 0:
                self.current = len(self.guesses) - 1
            else:
                self.current -= 1
            self.plot_direct()
        # self.plt.plot(self.xs[self.current], self.ys[self.current])
        self.plt.axhline(y=0, color='k', label='X-Axis')
        self.plt.axvline(x=0, color='k', label='Y-Axis')
        self.plt.legend(loc="upper right")
        self.canvas.draw()
        self.canvas.figure.set_canvas(self.canvas)

    def plot_indirect(self):
        self.plt.plot(self.fx, self.fy, color='r', label='f(x)')
        self.plt.axvline(x=self.bounds[self.current][0], color='b', label='lower')
        self.plt.axvline(x=self.bounds[self.current][1], color='g', label='upper')

    def plot_direct(self):
        if self.method == 3:
            max_guess = max(self.guesses[self.current][0], self.guesses[self.current][1])
            min_guess = min(self.guesses[self.current][0], self.guesses[self.current][1])
            self.fx = np.arange(min_guess - 3, max_guess + 3, 0.2)
            self.fy = np.array([self.solver.evaluate(num) for num in self.fx])
        else:
            self.fx = np.arange(self.guesses[self.current] - 3, self.guesses[self.current] + 3, 0.2)
            self.fy = np.array([self.solver.evaluate(num) for num in self.fx])

        if self.method == 1:
            self.unit_x = np.array([self.fx[0], self.fx[len(self.fx) - 1]])
            self.unit_y = np.array([self.fx[0], self.fx[len(self.fx) - 1]])
        elif self.method == 2:
            self.unit_x = self.fx
            self.slope = self.solver.d(self.guesses[self.current])
            self.b = self.solver.f(self.guesses[self.current]) - (self.slope * self.guesses[self.current])
            self.unit_y = np.array([((self.slope * num) + self.b) for num in self.unit_x])
        else:
            self.unit_x = self.fx
            self.slope = (
                        (self.solver.f(self.guesses[self.current][0]) - self.solver.f(self.guesses[self.current][1])) /
                        (self.guesses[self.current][0] - self.guesses[self.current][1]))
            self.b = self.solver.f(self.guesses[self.current][0]) - (self.slope * self.guesses[self.current][0])
            self.unit_y = np.array([((self.slope * num) + self.b) for num in self.unit_x])

        self.plt.plot(self.fx, self.fy, color='r')
        self.plt.plot(self.unit_x, self.unit_y, color='c')
        if self.method == 3:
            self.plt.axvline(x=self.guesses[self.current][0], color='b')
            self.plt.axvline(x=self.guesses[self.current][1], color='y')
        else:
            self.plt.axvline(x=self.guesses[self.current], color='b')
        self.plt.axvline(x=self.xes[self.current], color='g')


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
        self.geometry('+%i+%i' % (event.x_root + 20, event.y_root - 10))
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
