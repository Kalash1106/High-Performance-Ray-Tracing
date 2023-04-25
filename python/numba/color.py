import numpy as np
from vector_implementation import vec3

class color():
    #Default color is black
    def __init__(self, r = 0, g = 0, b = 0):
        self.r = r
        self.g = g
        self.b = b

    def __add__(self, other):
        r_new = self.r + other.r
        g_new = self.g + other.g
        b_new = self.b + other.b
        return color(r_new, g_new, b_new)

    def __sub__(self, other):
        r_new = self.r - other.r
        g_new = self.g - other.g
        b_new = self.b - other.b
        return color(r_new, g_new, b_new)

    def __mul__(self, scale : float):
        self.r = self.r * scale
        self.g = self.g * scale
        self.b = self.b * scale

    def __mul__(self, other):
        r_new = self.r * other.r
        g_new = self.g * other.g
        b_new = self.b * other.b
        return color(r_new, g_new, b_new)

class ray():

    def __init__(self, vec_in : vec3, c_in : color):
        super().__init__(c_in.r, c_in.g, c_in.b)
        self.vector = vec_in
        self.color = c_in

    def modify_color(self, c_new):
        self.color = c_new

    def modify_direction(self, new_dirn : vec3):
        self.vector = new_dirn

    def modify_intensity(self, i_in):
        self.intensity = i_in


def clamp(num, min, max):
    if(num >= min and num <= max): 
        return num
    
    elif(num < min):
        return min
    
    elif(num > max):
        return max
    
def write_color(out_file : __file__, pixel_color : color, samples_per_pixel : int, gamma_correction : bool = False):
    r = pixel_color.r
    g = pixel_color.g
    b = pixel_color.b

    if(gamma_correction == True):
        #Divide the color by the number of samples and gamma-correct for gamma=2.0.
        scale = 1.0 / samples_per_pixel
        r = np.sqrt(scale * r)
        g = np.sqrt(scale * g)
        b = np.sqrt(scale * b)

        with open(out_file, 'w') as f:
            f.write("%s %s %s\n" % (256 * clamp(r, 0.0, 0.999),256 * clamp(g, 0.0, 0.999), 256 * clamp(b, 0.0, 0.999) ))

    else:
        with open(out_file, 'w') as f:
            f.write("%s %s %s\n" % r, g, b)

            