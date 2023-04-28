import numpy as np
from numpy.typing import NDArray


class ray:
    def __init__(self, origin: NDArray[np.float64], direction: NDArray[np.float64]):
        self.origin = origin
        self.direction = direction

    def at(self, t: np.float64) -> NDArray[np.float64]:
        return self.origin + t * self.direction
