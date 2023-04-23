from vector_implementation import vec3, point

class hit_record:
    def __init__(self):
        self.t: float = 0
        self.front_face: float = False
        self.normal: vec3 = vec3(0, 0, 0, 0, 0, 0)
        self.p: point = point(0, 0, 0)
    
    def set_face_normal(self, r: vec3, outward_normal: vec3):
        self.front_face = r.dot_product(outward_normal) < 0
        if self.front_face:
            self.normal = outward_normal
        else:
            self.normal = outward_normal * -1;

