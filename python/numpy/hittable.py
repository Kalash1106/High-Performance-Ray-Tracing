from abc import ABC, abstractmethod
import numpy as np
from numpy.typing import NDArray
from ray import ray
from typing import Tuple, Optional


class hit_record:
    def __init__(self, p=np.zeros((3)), normal=np.zeros((3)), t=np.float64(0.0)):
        self.p = p
        self.normal: NDArray[np.float64] = normal
        self.t = t
        self.front_face: bool = False

    def set_face_normal(self, r: ray, outward_normal: NDArray[np.float64]) -> None:
        self.front_face = np.dot(r.direction, outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = -outward_normal


class hittable(ABC):
    @abstractmethod
    def hit(
        self,
        r: ray,
        t_min: np.float64,
        t_max: np.float64,
    ) -> Tuple[Optional[hit_record], bool]:
        pass
