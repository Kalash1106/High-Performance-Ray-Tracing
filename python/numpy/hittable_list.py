from ray import ray
from hittable import hit_record
from sphere import sphere_hit
from hittable import hittable, hit_record
from ray import ray

import numpy as np
from numpy.typing import NDArray
from typing import List, Tuple, Optional

import numba


@numba.njit
def world_hit(
    center_array: NDArray[np.float64],
    radius_array: NDArray[np.float64],
    r_origin: NDArray[np.float64],
    r_direction: NDArray[np.float64],
    t_min: np.float64,
    t_max: np.float64,
    rec_p: NDArray[np.float64],
    rec_normal: NDArray[np.float64],
    rec_t_wrapper: NDArray[np.float64],
    rec_front_face_wrapper: NDArray[np.uint8],
) -> bool:
    hit_anything = False
    closest_so_far: np.float64 = t_max

    temp_rec_p: NDArray[np.float64] = np.empty((3))
    temp_rec_normal: NDArray[np.float64] = np.empty((3))
    temp_rec_t_wrapper: NDArray[np.float64] = np.empty((1))
    temp_rec_front_face_wrapper: NDArray[np.uint8] = np.empty((1), dtype=np.uint8)

    for i in range(center_array.shape[0]):
        if sphere_hit(
            center_array[i],
            radius_array[i],
            r_origin,
            r_direction,
            t_min,
            t_max,
            temp_rec_p,
            temp_rec_normal,
            temp_rec_t_wrapper,
            temp_rec_front_face_wrapper,
        ):
            closest_so_far = temp_rec_t_wrapper[0]
            hit_anything = True

            rec_t_wrapper[0] = temp_rec_t_wrapper[0]

            for j in range(rec_p.shape[0]):
                rec_p[j] = temp_rec_p[j]

            for j in range(rec_normal.shape[0]):
                rec_normal[j] = temp_rec_normal[j]

            rec_front_face_wrapper[0] = temp_rec_front_face_wrapper[0]

    return hit_anything


class hittable_list(hittable):
    def __init__(self):
        self.objects: List[hittable] = []

    def hit(
        self, r: ray, t_min: np.float64, t_max: np.float64
    ) -> Tuple[Optional[hit_record], bool]:
        # temp_rec: hit_record = hit_record()
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        for object in self.objects:
            temp_rec, hit_anything = object.hit(r, t_min, closest_so_far)
            if hit_anything:
                closest_so_far = temp_rec.t  # type: ignore
                hit_anything = True
                return temp_rec, True
                # hr.t = temp_rec.t
                # hr.p = temp_rec.p
                # hr.normal = temp_rec.normal
                # hr.front_face = temp_rec.front_face

        return temp_rec, hit_anything

    def cpphit(
        self, r: ray, t_min: np.float64, t_max: np.float64, rec: hit_record
    ) -> bool:
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = t_max

        for object in self.objects:
            if object.cpphit(r, t_min, closest_so_far, temp_rec):
                closest_so_far = temp_rec.t  # type: ignore
                hit_anything = True

                rec.t = temp_rec.t
                rec.p = temp_rec.p
                rec.normal = temp_rec.normal
                rec.front_face = temp_rec.front_face

        return hit_anything
