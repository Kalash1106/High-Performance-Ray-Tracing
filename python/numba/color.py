import numba as nb
import numpy as np
from numba.experimental import jitclass

spec_color = [
    ('r', nb.float32),             
    ('g', nb.float32),  
    ('b', nb.float32),      
]

@jitclass(spec_color)
class color():
    def __init__(self, r, g , b):
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

def warm_color_numba():
    test_1 = color(21, 37, 211)
    test_2 = color(1, 2, 3)
    test_1 = test_1 + test_2
    test_1 = test_1 - test_2
    test_1 * 2.5

#Making sure all the functions run atleast once
warm_color_numba()

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

            