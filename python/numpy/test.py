import copy
import numpy as np
from numpy.typing import NDArray


class TestClass:
    def __init__(self, a: int = 0, b: str = "defstr"):
        self.a = a
        self.b = b


def test(a: NDArray[np.float64]):
    np.multiply(2, a, out=a)


x = np.linspace(0, 5, 9)
print(x)
test(x)
print(x)
