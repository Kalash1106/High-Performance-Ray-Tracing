import numpy as np
import numba as nb
from numba.experimental import jitclass


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
    

class vec3(point):
    def __init__(self, x_start, y_start, z_start, x_end, y_end, z_end):
        self.x_start = x_start
        self.y_start = y_start
        self.z_start = z_start

        self.x_end = x_end
        self.y_end = y_end
        self.z_end = z_end

        l2_div = 1/self.get_l2norm
        #Make rel unit
        self.xrel = (x_end - x_start) * l2_div
        self.yrel = y_end - y_start * l2_div
        self.zrel = z_end - z_start * l2_div
         

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

    def at(self, t: float):
         p_x = self.x_start + self.xrel * t
         p_y = self.y_start + self.yrel * t
         p_z = self.z_start + self.zrel * t
         return point(p_x, p_y, p_z)
         
    
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

     