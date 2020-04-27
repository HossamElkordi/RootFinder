from math import *
from scipy.misc import derivative


class solution_techinques:

    def __init__(self):
        self.expression = None

    def f(self, x):
        return self.evaluate(x)

    def d(self, x):
        return derivative(self.f, x)

    def evaluate(self, x):
        return eval(self.expression)

    def set_expression(self, expression):
        self.expression = expression

    def bisection(self, upper, lower, accuracy, max_iter, round_digit):
        fu = self.evaluate(upper)
        fl = self.evaluate(lower)
        if fu * fl > 0:
            return 'No root in this interval'
        i = 0
        old_x = 0.0
        bounds = []
        xes = []
        while True:
            bounds.append((upper, lower))
            x = round((lower + upper) / 2.0, round_digit)
            xes.append(x)
            if fu * self.evaluate(x) < 0:
                lower = x
            else:
                upper = x
                fu = self.evaluate(upper)
            i = i + 1
            if i == 1:
                continue
            if i == max_iter:
                break
            if abs(old_x - x) < accuracy:
                break
            old_x = x
        return [xes, bounds]

    def regulafalsi(self, upper, lower, accuracy, max_iter, round_digit):
        fu = self.evaluate(upper)
        fl = self.evaluate(lower)
        if fu * fl > 0:
            return 'No root in this interval'
        i = 0
        old_x = 0.0
        bounds = []
        xes = []
        while True:
            bounds.append((upper, lower))
            x = round((lower * fu - upper * fl) / (fu - fl), round_digit)
            xes.append(x)
            if fu * self.evaluate(x) < 0:
                lower = x
                fl = self.evaluate(lower)
            else:
                upper = x
                fu = self.evaluate(upper)
            i = i + 1
            if i == 1:
                continue
            if i == max_iter:
                break
            if abs(old_x - x) < accuracy:
                break
            old_x = x
        return [xes, bounds]

    def newtonRaphson(self, init, accuracy, max_iter, round_digit):
        i = 0
        prev_guess = []
        xes = []
        while True:
            prev_guess.append(init)
            x = round(init - (self.evaluate(init) / self.d(init)), round_digit)
            xes.append(x)
            i = i + 1
            if abs(x - init) < accuracy:
                break
            if i == max_iter:
                break
            init = x
        return [xes, prev_guess]


    def secant(self, init, pre_init, accuracy, max_iter, round_digit):
        prev_guesses = []
        xes = []
        while True:
            prev_guesses.append((pre_init, init))
            x = init - ((self.evaluate(init) * (pre_init - init)) / (
                    self.evaluate(pre_init) - self.evaluate(init)))
            x = round(x, round_digit)
            xes.append(x)
            pre_init = init
            init = x
            i = i + 1
            if i == max_iter:
                break
            if abs(init - pre_init) < accuracy:
                break
        return [xes, prev_guesses]
