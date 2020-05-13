from math import *
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
from typing import List, Any

from scipy.misc import derivative


class solution_techinques:

    def __init__(self, expression):
        self.expression = expression
        self.x = Symbol('x')
        self.deriv = parse_expr(self.expression)
        self.deriv = self.deriv.diff(self.x)
        self.deriv = lambdify(self.x, self.deriv)

    def f(self, x):
        return self.evaluate(x)

    def d(self, x):
        return self.deriv(x)

    def evaluate(self, x):
        try:
            return eval(self.expression)
        except OverflowError:
            return float('inf')

    def bisection(self, upper, lower, accuracy, max_iter, round_digit):
        fu = self.evaluate(upper)
        fl = self.evaluate(lower)
        if fu * fl > 0:
            return 'No root in this interval'
        i = 0
        old_x = 0.0
        bounds = []
        xes = []
        acc = []
        while True:
            bounds.append((lower, upper))
            x = round((lower + upper) / 2.0, round_digit)
            xes.append(x)
            mul = fu * self.evaluate(x)
            if mul < 0:
                lower = x
                fl = self.evaluate(lower)
            elif mul > 0:
                upper = x
                fu = self.evaluate(upper)
            else:
                acc.append(round(abs(old_x - x), round_digit))
                break
            i += 1
            if i == 1:
                continue
            a = round(abs(old_x - x), round_digit)
            acc.append(a)
            if a < accuracy:
                break
            if i == max_iter:
                break
            old_x = x
        return [xes, bounds, acc]

    def regulafalsi(self, upper, lower, accuracy, max_iter, round_digit):
        fu = self.evaluate(upper)
        fl = self.evaluate(lower)
        if fu * fl > 0:
            return 'No root in this interval'
        i = 0
        old_x = 0.0
        bounds = []
        xes = []
        acc = []
        while True:
            bounds.append((lower, upper))
            x = round((lower * fu - upper * fl) / (fu - fl), round_digit)
            xes.append(x)
            mul = fu * self.evaluate(x)
            if mul < 0:
                lower = x
                fl = self.evaluate(lower)
            elif mul > 0:
                upper = x
                fu = self.evaluate(upper)
            else:
                acc.append(round(abs(old_x - x), round_digit))
                break
            i += 1
            if i == 1:
                continue
            a = round(abs(old_x - x), round_digit)
            acc.append(a)
            if a < accuracy:
                break
            if i == max_iter:
                break
            old_x = x
        return [xes, bounds, acc]

    def FixedPoint(self, init, accuracy, max_iter, round_digit):
        prev_guesses = []
        xes = []
        acc = []
        i = 0
        while i < max_iter:
            prev_guesses.append(init)
            old = init
            init = round(self.evaluate(init), round_digit)
            if init == inf:
                return 'Overflow in math range'
            xes.append(init)
            i += 1
            a = round(abs(old - init), round_digit)
            acc.append(a)
            if a == inf:
                return 'This method diverges'
            if a < accuracy:
                break
            if i == max_iter:
                break
        return [xes, prev_guesses, acc]

    def newtonRaphson(self, init, accuracy, max_iter, round_digit):
        i = 0
        prev_guess = []
        xes = []
        acc = []
        while True:
            prev_guess.append(init)
            x = round(init - (self.evaluate(init) / self.d(float(init))), round_digit)
            if x == inf:
                return 'Overflow in math range'
            xes.append(x)
            i += 1
            a = round(abs(x - init), round_digit)
            acc.append(a)
            if a == inf:
                return 'This method diverges'
            if a < accuracy:
                break
            if i == max_iter:
                break
            init = x
        return [xes, prev_guess, acc]

    def secant(self, init, pre_init, accuracy, max_iter, round_digit):
        prev_guesses = []
        xes = []
        acc = []
        i = 0
        while True:
            prev_guesses.append((pre_init, init))
            x = init - ((self.evaluate(init) * (pre_init - init)) / (
                    self.evaluate(pre_init) - self.evaluate(init)))
            if x == inf:
                return 'Overflow in math range'
            x = round(x, round_digit)
            xes.append(x)
            pre_init = init
            init = x
            i += 1
            a = round(abs(init - pre_init), round_digit)
            acc.append(a)
            if a == inf:
                return 'This method diverges'
            if a < accuracy:
                break
            if i == max_iter:
                break
        return [xes, prev_guesses, acc]
