import numpy as np
import numba
from numpy.typing import NDArray

from ray import ray


@numba.njit
def nbcamera_get_ray_direction(
    origin: NDArray[np.float64],
    lower_left_corner: NDArray[np.float64],
    horizontal: NDArray[np.float64],
    vertical: NDArray[np.float64],
    u: np.float64,
    v: np.float64,
):
    return lower_left_corner + u * horizontal + v * vertical - origin


# generate LLVM IR
nbcamera_get_ray_direction(np.empty((3)), np.empty((3)), np.empty((3)), np.empty((3)), 0.5, 0.5)  # type: ignore


class camera:
    def __init__(self):
        aspect_ratio = np.float64(16.0 / 9.0)
        viewport_height = np.float64(2.0)
        viewport_width = aspect_ratio * viewport_height
        focal_length = np.float64(1.0)

        self.origin: NDArray[np.float64] = np.zeros((3))
        self.horizontal: NDArray[np.float64] = np.array([viewport_width, 0.0, 0.0])
        self.vertical: NDArray[np.float64] = np.array([0.0, viewport_height, 0.0])
        self.lower_left_corner: NDArray[np.float64] = (
            self.origin
            - self.horizontal / 2
            - self.vertical / 2
            - np.array([0, 0, focal_length])
        )

    def get_ray(self, u: np.float64, v: np.float64) -> ray:
        return ray(
            self.origin,
            self.lower_left_corner
            + u * self.horizontal
            + v * self.vertical
            - self.origin,
        )
