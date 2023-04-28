from hittable import hittable, hit_record
from ray import ray
import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Optional


class hittable_list(hittable):
    def __init__(self):
        self.objects: List[hittable] = []

    def hit(
        self, r: ray, t_min: np.float64, t_max: np.float64
    ) -> Tuple[Optional[hit_record], bool]:
        # temp_rec: hit_record = hit_record()
        hit_anything = False
        closest_so_far = t_max.copy()

        for object in self.objects:
            temp_rec, hit_anything = object.hit(r, t_min, closest_so_far)
            if hit_anything:
                closest_so_far = temp_rec.t  # type: ignore
                return temp_rec, True
                # hr.t = temp_rec.t
                # hr.p = temp_rec.p
                # hr.normal = temp_rec.normal
                # hr.front_face = temp_rec.front_face

        return None, hit_anything
