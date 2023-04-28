from hittable import hittable, hit_record
from ray import ray
import numpy as np
from numpy.typing import NDArray
from typing import Tuple, Optional


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
