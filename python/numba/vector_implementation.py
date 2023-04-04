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

spec_vec3 = [
    ('x_start', nb.float32),             
    ('y_start', nb.float32),  
    ('z_start', nb.float32), 
    ('x_end', nb.float32),             
    ('y_end', nb.float32),  
    ('z_end', nb.float32),
    ('xrel', nb.float32),             
    ('yrel', nb.float32),  
    ('zrel', nb.float32),       
]

#The vector class assumes start point and an end point
@jitclass(spec_vec3)
class vec3():
    def __init__(self, x_start, y_start, z_start, x_end, y_end, z_end):
        self.x_start = x_start
        self.y_start = y_start
        self.z_start = z_start

        self.x_end = x_end
        self.y_end = y_end
        self.z_end = z_end

        self.xrel = x_end - x_start
        self.yrel = y_end - y_start
        self.zrel = z_end - z_start
         

    @property
    def get_l2norm(self):
         return np.sqrt( (self.x_end - self.x_start)**2 
                        +(self.y_end - self.y_start)**2
                        +(self.z_end - self.z_start)**2)
    
    def __add__(self, other):
        x_s = self.x_start + other.x_start
        y_s = self.y_start + other.y_start
        z_s = self.z_start + other.z_start

        x_e = self.x_end + other.x_end
        y_e = self.y_end + other.y_end
        z_e = self.z_end + other.z_end

        return vec3(x_s, y_s, z_s, x_e, y_e, z_e)

    def __sub__(self, other):
        x_s = self.x_start - other.x_start
        y_s = self.y_start - other.y_start
        z_s = self.z_start - other.z_start

        x_e = self.x_end - other.x_end
        y_e = self.y_end - other.y_end
        z_e = self.z_end - other.z_end

        return vec3(x_s, y_s, z_s, x_e, y_e, z_e)

    def __mul__(self, scale : float):
        self.x_start = self.x_start * scale
        self.y_start = self.y_start * scale
        self.z_start = self.z_start * scale

        self.x_end = self.x_end * scale
        self.y_end = self.y_end * scale
        self.z_end = self.z_end * scale
    
    def dot_product(self, other):
         return self.xrel * other.xrel + self.yrel * other.yrel + self.zrel * other.zrel
    
    def cross_product(self, other):
         x = self.yrel * other.zrel - self.zrel * other.yrel
         y = self.xrel * other.zrel - self.zrel * other.xrel
         z = self.xrel * other.yrel - self.yrel * other.xrel
         return vec3(0, 0, 0, x, y, z)
    
    def make_unit(self):
         l2 = self.get_l2norm
         self.x_start = self.x_start / l2
         self.y_start = self.y_start / l2
         self.z_start = self.z_start / l2

         self.x_end = self.x_end / l2
         self.y_end = self.y_end / l2
         self.z_end = self.z_end / l2

         self.xrel = self.x_end - self.x_start
         self.yrel = self.y_end - self.y_start
         self.zrel = self.z_end - self.z_start

#To warm up all the functions once
def warm_vec_numba():
    test_vec = vec3(0,0,0, 1.5, 2.5, 3)
    test_2 = vec3(1,1,1, -2, -5, 1)
    a = test_vec.get_l2norm
    test_vec = test_vec + test_2
    test_vec = test_vec - test_2
    test = test_vec * 0.5
    test_dot = test_vec.dot_product(test_2)
    test_cross = test_vec.cross_product(test_2)
    test = test_vec.make_unit()
     
#Warming up
warm_point_numba()
warm_vec_numba()


     