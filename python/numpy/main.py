import sys
import numpy as np
import numba

from ray import ray
from hittable import hittable, hit_record
from hittable_list import hittable_list, world_hit
from sphere import sphere
from color import write_color
from camera import camera
from utils import random_in_unit_sphere, mydot, nbrandom_in_unit_sphere

from numpy.typing import NDArray

# compile LLVM IR
world_hit(np.empty((1, 3)), np.empty((1)), np.empty((3)), np.empty((3)), 0.001, np.inf, np.empty((3)), np.empty((3)), np.empty((1)), np.empty((1), dtype=np.uint8))  # type: ignore


def ray_color(r: ray, world: hittable, depth: int) -> NDArray[np.float64]:
    if depth <= 0:
        return np.zeros((3))

    rec = hit_record()
    # rec, hit_anything = world.hit(r, np.float64(0.001), np.float64(np.inf))
    if world.cpphit(r, np.float64(0.001), np.float64(np.inf), rec):
        target = rec.p + rec.normal + random_in_unit_sphere()  # type: ignore
        return 0.5 * ray_color(ray(rec.p, target - rec.p), world, depth - 1)  # type: ignore

    unit_direction: NDArray[np.float64] = r.direction / np.sqrt(
        np.dot(r.direction, r.direction)
    )
    t = 0.5 * (unit_direction[1] + 1.0)
    return (1 - t) * np.ones((3)) + t * np.array([0.5, 0.7, 1.0])


def jitray_color(r: ray, world, depth: int) -> NDArray[np.float64]:
    if depth <= 0:
        return np.zeros((3))

    rec_p: NDArray[np.float64] = np.empty((3))
    rec_normal: NDArray[np.float64] = np.empty((3))
    rec_t_wrapper: NDArray[np.float64] = np.empty((1))
    rec_front_face_wrapper: NDArray[np.uint8] = np.empty((1), dtype=np.uint8)

    center_array = []
    radius_array = []
    for object in world.objects:
        center_array.append(object.center)
        radius_array.append(object.radius)

    if world_hit(
        np.array(center_array),
        np.array(radius_array),
        r.origin,
        r.direction,
        np.float64(0.001),
        np.float64(np.inf),
        rec_p,
        rec_normal,
        rec_t_wrapper,
        rec_front_face_wrapper,
    ):
        target = rec_p + rec_normal + random_in_unit_sphere()  # type: ignore
        return 0.5 * jitray_color(ray(rec_p, target - rec_p), world, depth - 1)  # type: ignore

    unit_direction: NDArray[np.float64] = r.direction / np.sqrt(
        np.dot(r.direction, r.direction)
    )
    t = 0.5 * (unit_direction[1] + 1.0)
    return (1 - t) * np.ones((3)) + t * np.array([0.5, 0.7, 1.0])

@numba.njit
def fullnbray_color(r_origin: NDArray[np.float64], r_direction: NDArray[np.float64], sp_centers: NDArray[np.float64], sp_radii: NDArray[np.float64], depth: int) -> NDArray[np.float64]:
    if depth <= 0:
        return np.zeros((3))

    rec_p: NDArray[np.float64] = np.empty((3))
    rec_normal: NDArray[np.float64] = np.empty((3))
    rec_t_wrapper: NDArray[np.float64] = np.empty((1))
    rec_front_face_wrapper: NDArray[np.uint8] = np.empty((1), dtype=np.uint8)

    # center_array = []
    # radius_array = []
    # for object in world.objects:
    #     center_array.append(object.center)
    #     radius_array.append(object.radius)

    if world_hit(
        sp_centers,
        sp_radii,
        r_origin,
        r_direction,
        np.float64(0.001),
        np.float64(np.inf),
        rec_p,
        rec_normal,
        rec_t_wrapper,
        rec_front_face_wrapper,
    ):
        target = rec_p + rec_normal + nbrandom_in_unit_sphere()  # type: ignore
        return 0.5 * fullnbray_color(rec_p, target - rec_p, sp_centers, sp_radii, depth - 1)  # type: ignore

    unit_direction: NDArray[np.float64] = r_direction / np.sqrt(
        mydot(r_direction, r_direction)
    )
    t = 0.5 * (unit_direction[1] + 1.0)
    return (1 - t) * np.ones((3)) + t * np.array([0.5, 0.7, 1.0])

# generate LLVM IR
fullnbray_color(np.empty((3)), np.empty((3)), np.empty((1, 3)), np.empty((1)), 1)


def main():
    IMAGE_WIDTH: int = 400
    IMAGE_HEIGHT: int = (IMAGE_WIDTH // 16) * 9
    SAMPLES_PER_PIXEL: int = 5
    MAX_DEPTH: int = 5

    world = hittable_list()
    world.objects.append(
        sphere(np.array([0, -100.5, -1], dtype=np.float64), np.float64(100.0))
    )
    world.objects.append(
        sphere(np.array([0, 0, -1], dtype=np.float64), np.float64(0.5))
    )

    centers = np.array([[0.0, -100.5, -1.0], [0, 0, -1]])
    radii = np.array([100.0, 0.5])
    # world.objects.append(
    #     sphere(np.array([1, 0, -1], dtype=np.float64), np.float64(0.5))
    # )
    # world.objects.append(
    #     sphere(np.array([-1, 0, -1], dtype=np.float64), np.float64(0.5))
    # )

    sp = sphere(np.array([0, 0, -1], dtype=np.float64), np.float64(0.5))

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
                # pixel_color += jitray_color(r, world, MAX_DEPTH)
                pixel_color += fullnbray_color(r.origin, r.direction, centers, radii, MAX_DEPTH)

            write_color(sys.stdout, pixel_color, SAMPLES_PER_PIXEL)


if __name__ == "__main__":
    main()
