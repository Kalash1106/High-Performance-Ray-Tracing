import numpy as np
from vector_implementation import point, vec3
from color import color, ray
from sphere import sphere
from hit_record import hit_record

def ray_color(ray : ray, world, depth : int):
    rec : hit_record

    #The reflection Loop
    while(depth>=0 and world.hit(ray, 0.001, np.Infinity, rec) and ray.intensity > 0.05):
        
        target : point = rec.p + (rec.normal + random_in_unit_sphere())
        ray.modify_direction(vec3(rec.p.x, rec.p.y, rec.p.z, target.x, target.y, target.z))
        cos_a = ray.vector.dot_product(rec.normal)

        #Considering single instance refraction from surface
        ray.modify_color(ray.color * (1 + (cos_a + rec.sphere.transmittivity) * ray.intensity))
        ray.modify_intensity(ray.intensity * sphere.reflectivity)
        depth = depth - 1
        





















