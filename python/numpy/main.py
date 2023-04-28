import sys
import numpy as np

from ray import ray
from hittable import hittable, hit_record
from hittable_list import hittable_list
from sphere import sphere
from color import write_color
from camera import camera
from utils import random_in_unit_sphere

from numpy.typing import NDArray


def ray_color(r: ray, world: hittable, depth: int) -> NDArray[np.float64]:
    if depth <= 0:
        return np.zeros((3))

    rec = hit_record()
    rec, hit_anything = world.hit(r, np.float64(0.001), np.float64(np.inf))
    if hit_anything:
        target = rec.p + rec.normal + random_in_unit_sphere()  # type: ignore
        return 0.5 * ray_color(ray(rec.p, target - rec.p), world, depth - 1)  # type: ignore

    unit_direction: NDArray[np.float64] = r.direction / np.sqrt(
        np.dot(r.direction, r.direction)
    )
    t = 0.5 * (unit_direction[1] + 1.0)
    return (1 - t) * np.ones((3)) + t * np.array([0.5, 0.7, 1.0])


# def iray_color(r: ray, world: hittable, depth: int) -> NDArray[np.float64]:
#     c0: NDArray[np.float64] = np.zeros((3))
#     for _ in range(depth):
#         rec = hit_record()
#         rec, hit_anything = world.hit(r, np.float64(0.001), np.float64(np.inf))

#         c0 *= 0.5 * temp
#         temp = c0


def main():
    IMAGE_WIDTH: int = 400
    IMAGE_HEIGHT: int = (IMAGE_WIDTH // 16) * 9
    SAMPLES_PER_PIXEL: int = 5
    MAX_DEPTH: int = 5

    world = hittable_list()
    world.objects.append(
        sphere(np.array([0, 0, -1], dtype=np.float64), np.float64(0.5))
    )
    world.objects.append(
        sphere(np.array([0, -100.5, -1], dtype=np.float64), np.float64(100.0))
    )

    cam = camera()

    print("P3")
    print(f"{IMAGE_WIDTH} {IMAGE_HEIGHT}")
    print("255")

    for j in range(IMAGE_HEIGHT - 1, -1, -1):
        # print(f"Scanlines remaining {j}", file=sys.stderr, flush=True, end="\r")
        for i in range(IMAGE_WIDTH):
            pixel_color: NDArray[np.float64] = np.zeros((3))
            for s in range(SAMPLES_PER_PIXEL):
                u = np.float64((i + np.random.uniform(0.0, 1.0)) / (IMAGE_WIDTH - 1))
                v = np.float64((j + np.random.uniform(0.0, 1.0)) / (IMAGE_HEIGHT - 1))
                r: ray = cam.get_ray(u, v)
                pixel_color += ray_color(r, world, MAX_DEPTH)

            write_color(sys.stdout, pixel_color, SAMPLES_PER_PIXEL)


if __name__ == "__main__":
    main()
