from hittable import hittable, hit_record
from ray import ray
from utils import mydot
import numpy as np

from numpy.typing import NDArray
from typing import Tuple, Optional

import numba

"""
1 == True
0 == False
"""


@numba.njit
def sphere_hit(
    center: NDArray[np.float64],
    radius: np.float64,
    r_origin: NDArray[np.float64],
    r_direction: NDArray[np.float64],
    t_min: np.float64,
    t_max: np.float64,
    hr_p: NDArray[np.float64],
    hr_normal: NDArray[np.float64],
    hr_t_wrapper: NDArray[np.float64],
    hr_front_face_wrapper: NDArray[np.uint8],
) -> bool:
    oc: NDArray[np.float64] = r_origin - center
    # a: np.float64 = np.square(np.linalg.norm(r_direction))
    a: np.float64 = mydot(r_direction, r_direction)
    half_b: np.float64 = mydot(oc, r_direction)
    c: np.float64 = mydot(oc, oc) - (radius * radius)

    discriminant: np.float64 = half_b * half_b - a * c
    if discriminant < 0.0:
        # hr_t_wrapper[0] = np.inf
        return False
    sqrtd: np.float64 = np.sqrt(discriminant)

    root = (-half_b - sqrtd) / a
    if root < t_min or root > t_max:
        root = (-half_b + sqrtd) / a
        if root < t_min or root > t_max:
            # hr_t_wrapper[0] = np.inf
            return False

    # hr = hit_record()
    # hr.t = root
    hr_t_wrapper[0] = root

    # hr.p = r.at(root)
    for i in range(3):
        hr_p[i] = r_origin[i] + r_direction[i] * root

    # outward_normal: NDArray[np.float64] = np.empty((3))
    outward_normal = (hr_p - center) / radius
    front_face: bool = mydot(r_direction, outward_normal) < 0.0  # type: ignore
    hr_front_face_wrapper[0] = 1 if front_face else 0

    # hr.set_face_normal(r, outward_normal)
    for i in range(3):
        hr_normal[i] = outward_normal[i] if front_face else -outward_normal[i]

    return True


class sphere(hittable):
    def __init__(
        self,
        center: NDArray[np.float64] = np.zeros((3)),
        radius: np.float64 = np.float64(0.0),
    ):
        self.center = center
        self.radius = radius

    def hit(
        self, r: ray, t_min: np.float64, t_max: np.float64
    ) -> Tuple[Optional[hit_record], bool]:
        oc: NDArray[np.float64] = r.origin - self.center
        a: np.float64 = np.square(np.linalg.norm(r.direction))
        half_b: np.float64 = np.dot(oc, r.direction)
        c: np.float64 = np.square(np.linalg.norm(oc)) - np.square(self.radius)

        discriminant: np.float64 = np.square(half_b) - a * c
        if discriminant < 0:
            return None, False
        sqrtd: np.float64 = np.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return None, False

        hr = hit_record()
        hr.t = root
        hr.p = r.at(root)
        outward_normal = (hr.p - self.center) / self.radius
        hr.set_face_normal(r, outward_normal)

        return hr, True

    def cpphit(
        self, r: ray, t_min: np.float64, t_max: np.float64, rec: hit_record
    ) -> bool:
        oc: NDArray[np.float64] = r.origin - self.center
        a: np.float64 = np.square(np.linalg.norm(r.direction))
        half_b: np.float64 = np.dot(oc, r.direction)
        c: np.float64 = np.square(np.linalg.norm(oc)) - np.square(self.radius)

        discriminant: np.float64 = np.square(half_b) - a * c
        if discriminant < 0:
            return False
        sqrtd: np.float64 = np.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < t_min or root > t_max:
            root = (-half_b + sqrtd) / a
            if root < t_min or root > t_max:
                return False

        # hr = hit_record()
        # hr.t = root
        rec.t = root

        # hr.p = r.at(root)
        rec.p = r.at(root)
        outward_normal = (rec.p - self.center) / self.radius

        # hr.set_face_normal(r, outward_normal)
        rec.set_face_normal(r, outward_normal)

        return True
