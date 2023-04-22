from vec3 import point, vec3
from ray import ray
from hit_record import hit_record
import math

class sphere:
    def __init__(self, x: float, y: float, z: float, r: float):
        self.center = point(x, y, z)
        self.radius = r
    
    def hit(r: ray, t_min: float, t_max: float, rec: hit_record) -> bool:
        a: float = 0
        half_b: float = 0
        c: float = 0

        discriminant: float = 0
        if (discriminant < 0):
            return False
        
        sqrtd: float = math.sqrt(discriminant)
        root: float = (-half_b - sqrtd) / a
        if (root < t_min or t_max < root):
            root = (-half_b + sqrtd) / a
            if (root < t_min or t_max < root):
                return False
        
        rec.t = root
        # rec.p = 