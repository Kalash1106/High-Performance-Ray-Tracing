import numpy as np
from numpy.typing import NDArray


def random_in_unit_sphere() -> NDArray[np.float64]:
    while True:
        p: NDArray[np.float64] = np.random.uniform(-1, 1, 3)
        if p.dot(p) >= 1:
            continue
        return p
