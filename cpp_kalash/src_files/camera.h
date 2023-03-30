#pragma once
#include "vec3.h"
#include "pixel.h"

class camera {
    public:
            float aspect_ratio, viewport_height, viewport_width, focal_length, samples_per_pixel;
            double image_width, image_height;
            point origin, screen_center, horizontal, vertical, lower_left_corner;

        camera() {
            //Properties
            aspect_ratio = 16.0 / 9.0;
            viewport_height = 2.0;
            viewport_width = aspect_ratio * viewport_height;
            focal_length = 1.0;
            samples_per_pixel = 100;

            //Image dimesnions
            image_width = 256;
            image_height = 256;

            //coordinates
            origin = point(0, 0, 0);
            screen_center = point(focal_length,0,0);
            horizontal = point(0.0, 0.0, viewport_width);
            vertical = point(0.0, viewport_height, 0.0);
            lower_left_corner = subtract_points(screen_center,
                                scale_point(add_points(horizontal, vertical), 0.5)) ;
        }

        ray get_ray(double u, double v) const {
            vec3 ray_vec(origin, subtract_points(
                          add_points(add_points(scale_point(horizontal, u), scale_point(vertical, v)), 
                          lower_left_corner), origin));
            ray ray_out(ray_vec);
            return ray_out;
        }
};