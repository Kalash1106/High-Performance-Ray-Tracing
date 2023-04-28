import numpy as np
from numpy.typing import NDArray
from typing import TextIO


def write_color(
    fd: TextIO, pixel_color: NDArray[np.float64], samples_per_pixel: int
) -> None:
    output: NDArray[np.uint8] = np.uint8(
        256 * np.clip(np.sqrt(1.0 / samples_per_pixel * pixel_color), 0, 0.999)
    )  # type: ignore
    fd.write(f"{output[0]} {output[1]} {output[2]}\n")
