#include "pixel.h"
#include "vec3.h"
#include <iostream>
#include <random>
#define radial_tolerance float(0.05)
#pragma once

class sphere
{
public:
	point center;
	float radius;
	color s_col;


	sphere(){
		s_col = black;
	}
	sphere(point center_in, float radius_in){
		center = center_in;
		radius = radius_in;
		s_col = black;

	}
	sphere(point center_in, float radius_in, color s_color){
		center = center_in;
		radius = radius_in;
		s_col = s_color;

	}


	bool within_sphere(point a){
		float d = (a.x_coordinate - center.x_coordinate) * (a.x_coordinate - center.x_coordinate) +
				  (a.y_coordinate - center.y_coordinate) * (a.y_coordinate - center.y_coordinate) +
				  (a.z_coordinate - center.z_coordinate) * (a.z_coordinate - center.z_coordinate);

		if(d<=radius*radius) return true;
		else return false;

	}
};

class hit_info
{
public:
	float t; //The parameter at which it hits the sphere
	point intersection_point;
	vec3 normal_at_intersection;

	hit_info(){}
	hit_info(float t_in, point p_in, vec3 n){
		t = t_in;
		intersection_point = p_in;
		normal_at_intersection = n;
	}

};

//This function naturally returns the outward normal
vec3 normal_at_point(point a, sphere s){
		point dirn = subtract_points(a, s.center);
		vec3 normal_p(s.center, 1, dirn);

		try {
		    if ((dirn.x_coordinate * dirn.x_coordinate +
		    	dirn.y_coordinate * dirn.y_coordinate +
		    	dirn.z_coordinate * dirn.z_coordinate - s.radius*s.radius) <= radial_tolerance) return normal_p;

		    else {
		    	throw a;
		    }
	    }

		catch(point a) {
		    std::cout << "The given point doesn't lie on the sphere surface";
		}
	}

void write_hit_info(hit_info& rec_in, float res_in, vec3& ray_in, sphere& s_in){
		rec_in.t = res_in;
        rec_in.intersection_point = add_points(ray_in.origin, scale_point(ray_in.direction_vector, res_in));
        rec_in.normal_at_intersection = normal_at_point(rec_in.intersection_point, s_in);
		return;
	}

float hit(const vec3& r, double t_min, double t_max, sphere s) {

    point oc = subtract_points(r.origin, s.center);
    auto a = dot_product(r.direction_vector, r.direction_vector);
    auto half_b = dot_product(oc, r.direction_vector);
    auto c = dot_product(oc, oc) - s.radius*s.radius;

    //std :: cout << a << " " << half_b << " " << c;

    auto discriminant = half_b*half_b - a*c;
    if (discriminant < 0) return false;
    auto sqrtd = sqrt(discriminant);

    // Find the nearest root that lies in the acceptable range.
    auto root = (-half_b - sqrtd) / a;
    if (root < t_min || t_max < root) {
        root = (-half_b + sqrtd) / a;
        if (root < t_min || t_max < root)
            return NAN;
    }

    return root;
}

vec3 spherical_reflection(point intersection_in, vec3 normal_in, vec3 ray_in ){
	//using w = v - 2(a.v)a, where a is the normal, v is the incident ray and w is the reflection
	point reflected_dirn = subtract_points(ray_in.direction_vector,
						scale_point(normal_in.direction_vector, 2 * dot_product(ray_in.direction_vector, normal_in.direction_vector)));

	vec3 ref(intersection_in, 1, reflected_dirn);
	return ref;
}

vec3 random(vec3 ray_in, point p, double min = -1.0, double max = 1.0) {
	std::random_device rd; // obtain a random number from hardware
    std::mt19937 gen(rd()); // seed the generator
	std::uniform_int_distribution<> coordinates(min, max); // define the range
	point rand_dirn(coordinates(gen), coordinates(gen), coordinates(gen) );

	while(l2_point_norm(rand_dirn) <= 1 && dot_product(rand_dirn, ray_in.direction_vector) > 0){
		rand_dirn.x_coordinate = coordinates(gen);
		rand_dirn.y_coordinate = coordinates(gen);
		rand_dirn.z_coordinate = coordinates(gen);
	}

        return vec3(p, 1, rand_dirn);
    }
