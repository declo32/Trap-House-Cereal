"""All equations based on a symmetrical trapezoid"""

import math
import numpy as np
from scipy.optimize import minimize


def base(b1, b2, h):
    B = 0.5 * h * (b1 + b2)
    return B


def perimeter(b1, b2, h):
    diagonal = math.sqrt(h**2 + (0.5 * (b1 - b2))**2)
    P = b1 + b2 + (2 * diagonal)
    return P


def volume(B, h):
    V = B * h
    return V


def lateralArea(P, h):
    LA = P * h
    return LA


def surfaceArea(B, LA):
    SA = (2 * B) + LA
    return SA

def cost(SA):
    cost = 0.1 * SA
    return cost

if __name__ == '__main__':
    x0 = np.array([4, 10, 3, 1])  # b1, b2, height, other height
    def foo(x):
        return cost(surfaceArea(base(x[0], x[1], x[2]), lateralArea(perimeter(x[0], x[1], x[2]), x[2])))
    res = minimize(
        foo,
        x0, method="nelder-mead", options={"xtol": 1e-8, "disp": True}
    )
