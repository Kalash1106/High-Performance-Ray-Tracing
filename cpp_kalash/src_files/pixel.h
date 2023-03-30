#pragma once
#include <iostream>
#include "vec3.h"
#include "hit_list.h"
#include "sphere.h"
#define sky_color color(0, 0, 200)
#define black color(0,0,0)
#define white color(256, 256, 256)


class color
{
public:
    float red, blue, green; //rgb values
    color(){}
    color(float red_in, float green_in, float blue_in){
        red = red_in;
        blue = blue_in;
        green = green_in;
    }
};

class pixel: public color
{
public:
    color pixel_color;
    point coordinate;

    //Both the types are supported

    pixel(point co_ord, float red_in, float green_in, float blue_in){
        coordinate = co_ord;
        pixel_color.red = red_in;
        pixel_color.blue = blue_in;
        pixel_color.green = green_in;
    }

    pixel(point co_ord, color c_in){
        coordinate = co_ord;
        pixel_color = c_in;
    }

    pixel(point co_ord){
        coordinate = co_ord;
    }

    pixel(){}
};

class ray: public color
{
public:
    color vec_color;
    vec3 ray_vector;

    ray(vec3 ray_in, float red_in, float green_in, float blue_in){
        ray_vector = ray_in;
        vec_color.red = red_in;
        vec_color.blue = blue_in;
        vec_color.green = green_in;
    }

    ray(vec3 ray_in, color c_in){
        ray_vector = ray_in;
        vec_color = c_in;
    }

    ray(vec3 ray_in){
        ray_vector = ray_in;
    }
    ray(){}
};

inline double clamp(double x, double min, double max) {
    if (x < min) return min;
    if (x > max) return max;
    return x;
}

void write_color(color a, int samples_per_pixel){
        // Divide the color by the number of samples.
    auto scale = 1.0 / samples_per_pixel;
    float r = a.red * scale;
    float g = a.green * scale;
    float b = a.blue * scale;

    // Write the translated [0,255] value of each color component.
     std::cout << static_cast<int>(256 * clamp(r, 0.0, 0.999)) << ' '
        << static_cast<int>(256 * clamp(g, 0.0, 0.999)) << ' '
        << static_cast<int>(256 * clamp(b, 0.0, 0.999)) << '\n';
}
color scale_color(color a, float scale){
    a.red *= scale;
    a.green *= scale;
    a.blue *= scale;

    return a;
}

color ray_color(const ray& r, collection_of_spheres world, hit_info rec, int n_collisions, double t_min = -INFINITY, double t_max = INFINITY) {
    
    std::list<sphere>::iterator it;
    it = world.sphere_collection.begin();

    if (hit(r.ray_vector, t_min, t_max, *it) != NAN) {
        //root calculation
        rec.t = hit(r.ray_vector, t_min, t_max, *it);

        //Intersection point calculation
        rec.intersection_point = add_points(r.ray_vector.origin, scale_point(r.ray_vector.direction_vector, rec.t));

        //Normal vector calculation
        rec.normal_at_intersection = normal_at_point(rec.intersection_point, *it);

        //Generating the random ray
        point target = add_points(add_points(rec.intersection_point, rec.normal_at_intersection.direction_vector),
                                    random(r.ray_vector, rec.intersection_point));

        color s_col = it-> s_col;
        world.sphere_collection.erase(it);
        return scale_color(
            ray_color(ray(vec3(rec.intersection_point, subtract_points(target, rec.intersection_point)), s_col), world, rec, --n_collisions)
            , 0.5);
    }

    else{
        world.sphere_collection.erase(it);
    }

    point unit_direction = unit_point_vec(r.ray_vector.direction_vector);
    auto t = 0.5*(unit_direction.y_coordinate + 1.0);
    return operate_color(scale_color(color(1.0, 1.0, 1.0), 1.0 - t), scale_color(color(0.5, 0.7, 1.0), t));
}


//Here operation = 1 implies addition and 1 subtraction
color operate_color(color a, color b, int operation = 1){
    if(operation == 1){
        a.red = a.red + b.red;
        a.green = a.green + b.green;
        a.blue = a.blue + b.blue;

        return a;
    }
    else{
        a.red = a.red - b.red;
        a.green = a.green - b.green;
        a.blue = a.blue - b.blue;

        return a;

    }
}

