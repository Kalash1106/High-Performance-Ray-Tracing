import numpy as np
import numba as nb
from numba.experimental import jitclass

#Speculations for numba class
spec_point = [
    ('x', nb.float32),             
    ('y', nb.float32),  
    ('z', nb.float32),      
]

@jitclass(spec_point)
class point():
    def __init__(self, x, y , z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def get_mod(self):
        return self.x**2 + self.y **2 + self.z ** 2

    def __add__(self, other):
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return point(x, y, z)

    def __sub__(self, other):
        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return point(x, y, z)

    def __mul__(self, scale : float):
            x = self.x * scale
            y = self.y * scale
            z = self.z * scale
            return point(x, y, z)
    
    def dot_point(self, other):
         return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross_point(self, other):
         x = self.y * other.z - self.z * other.y
         y = self.x * other.z - self.z * other.x
         z = self.x * other.y - self.y * other.x
         return point(x, y, z)
    

#To warm up all the functions once
def warm_point_numba():
    test_point = point(1,2,3)
    test_2 = point(1,2,3)
    a = test_point.get_mod
    test_point = test_point + test_2
    test_point = test_point - test_2
    test_point = test_point * 2.5
    test_point_dot = test_point.dot_point(test_2)
    test_point = test_point.cross_point(test_2)

# spec_vec3 = [
#         ('a', nb.experimental.jitclass.point),
#         ('t', nb.float32),
#         ('b', nb.experimental.jitclass.point),     
# ]
@jitclass()
class vec3(point):
     
     def __init__(self, a, t, b):
          self.o = a #Origin
          self.t = t #Parameter t
          self.b = b #* 1/np.sqrt(b.get_mod) # Unit Direction vector


     