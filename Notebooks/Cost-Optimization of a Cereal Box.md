# `ROUGH DRAFT`


# Cost-Optimization of a Cereal Box

### 1. You will be designing a **new** shape for a cereal box. Your new design **may not** be a rectangular prism!

Being hip kids who know what's cool, it didn't take long to realize that an isosceles trapezoidal prism is what's cool. So that's what we're working with.

### 2. You will be designing a new shape for a cereal box to hold 4 cups of cereal. The original cereal box's dimensions are ***6 inches by 1 inch by 10 inches***. The volume of this box is a little bigger than 4 cups... you want to be able to close the box! Material costs are $0.10 for every 25 square inches of cardstock. You will need to find the surface area (in square inches) and volume (in cubic inches) of the original package. You will also need to find the current cost of materials for one cereal box.

First, let's define a rectangular prism:


```python
class RectangularPrism:
    
    def __init__(self, l, w, h):  # What it needs to know to start itself
        self.l = l
        self.w = w
        self.h = h

    # Each of the following functions defines a property of the prism based on l, w, & h
    def base(self):
        B = self.l * self.w
        return B

    def basePerimeter(self):
        P = 2 * (self.l + self.w)
        return P

    def lateralArea(self):
        LA = self.basePerimeter() * self.h
        return LA

    def surfaceArea(self):
        SA = (2 * self.base()) + self.lateralArea()
        return SA
    
    def volume(self):
        V = self.l * self.w * self.h
        return V

```

Now let's define the cost function:


```python
def cost(area):
    return round(0.1 * (area / 25), 2)  # We're working with money, we only want two decimal points

```

<hr>

Now we can look at some properties of that boring old cereal box:


```python
box = RectangularPrism(6, 1, 10)
print("Surface Area:", box.surfaceArea())
print("Cost:        ", cost(box.surfaceArea()))
print("Volume:      ", box.volume())
```

    Surface Area: 152
    Cost:         0.61
    Volume:       60
    

*These numbers might be wierd because of [loss of significance](https://en.wikipedia.org/wiki/Loss_of_significance)*

### 3. You will need to create a new design for the cereal box that costs less to make but still holds the same amount of cereal. Also, your design must attract and keep shopper's attention. Create a **net** for your cereal box and label it with exact measurements in inches.



Let's define an isosceles trapezoidal prism:


```python
import math  # For the sqrt function


class IsoscelesTrapezoidalPrism:
    
    def __init__(self, b1, b2, h, d):
        self.b1 = b1  # base 1
        self.b2 = b2  # base 2
        self.h = h    # height
        self.d = d    # depth

    def base(self):
        B = 0.5 * self.h * (self.b1 + self.b2)
        return B
    
    def diagonal(self):
        D = math.sqrt(self.h**2 + (0.5 * (self.b1 - self.b2))**2)  # Pythagoran theorem
        return D

    def perimeter(self):
        P = self.b1 + self.b2 + (2 * self.diagonal())
        return P
    
    def lateralArea(self):
        LA = self.perimeter() * self.h
        return LA

    def surfaceArea(self):
        SA = (2 * self.base()) + self.lateralArea()
        return SA

    def volume(self):
        V = self.base() * self.d
        return V

```


```python
box = IsoscelesTrapezoidalPrism(5, 11, 3, 3)
print(box.surfaceArea())
print(cost(box.surfaceArea()))
print(box.volume())
```

    121.4558441227157
    0.49
    72.0
    

Now we need to figure out the best dimensions to use. This can be done with `scipy.optimize.minimize`.


```python
import numpy as np
from scipy.optimize import minimize
```

Before we can optimize, we need to define what it is that we want to minimize. In this case, it should be the cost.


```python
def foo(x):  # x will be a list of values, describing the dimensions of a trapezoidal prism
    box = IsoscelesTrapezoidalPrism(x[0], x[1], x[2], x[3])
    return cost(box.surfaceArea()) / box.volume()

```

Now we need to define any constraints. The box must have the same volume as the old one, which was shown to be 60in<sup>2</sup>.  Also, all the measurements must be positive.


```python
def constraint1(x):
    return 60.  # That was easier than I thought


def constraint2(x):
    for el in x:
        if el <= 0:
            return False
    return True

```


```python
x0 = np.array([5, 11, 3, 3])  # Four zeros as the placeholders for the dimensions
res = minimize(foo, x0, method="nelder-mead",
               options={"xtol": 1e-8, "disp": True},
               constraints={"type": "eq", "fun": constraint1})
print(res.x)
```

    C:\Anaconda3\lib\site-packages\scipy\optimize\_minimize.py:394: RuntimeWarning: Method nelder-mead cannot handle constraints nor bounds.
      RuntimeWarning)
    

    Warning: Maximum number of function evaluations has been exceeded.
    [  1.49477007e+50   8.19133853e+49  -4.65348987e+50   6.40412415e+50]
    
