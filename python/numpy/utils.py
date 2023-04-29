import numpy as np
from numpy.typing import NDArray

import numba as nb


def random_in_unit_sphere() -> NDArray[np.float64]:
    while True:
        p: NDArray[np.float64] = np.random.uniform(-1, 1, 3)
        if p.dot(p) >= 1:
            continue
        return p


@nb.njit
def mydot(x: NDArray[np.float64], y: NDArray[np.float64]) -> np.float64:
    return x[0] * y[0] + x[1] * y[1] + x[2] * y[2]


mydot(np.ones((3)), np.ones((3)))
