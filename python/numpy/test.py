import copy
import numpy as np
from numpy.typing import NDArray


class TestClass:
    def __init__(self, a: int = 0, b: str = "defstr"):
        self.a = a
        self.b = b

    def __repr__(self) -> str:
        return f"({self.a}, {self.b})"


def test1(a: NDArray[np.float64]):
    np.multiply(2, a, out=a)
    a = 2 * a


def test2(k: TestClass):
    # t = TestClass(42, "hello")
    # k = t
    k.a = 42
    k.b = "hello"


def test3(k: NDArray[np.float64]):
    k[0] = 42


def test4(k):
    k[0] = 3


def test5(k):
    t = TestClass(42, "hello")
    k[0] = t


x = np.linspace(0, 5, 9)
y = TestClass()
z: int = 0
u = np.array([0])
v = [TestClass()]
print(v)
test5(v)
print(v)
