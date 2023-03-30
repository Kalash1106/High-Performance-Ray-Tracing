#include "pixel.h"
#include "vec3.h"
#include <iostream>
#define tolerance float(0.05)
#pragma once

class cube
{
public:
	point center;
	float side;


	cube(){}
	cube(point center_in, float side_in){
		center = center_in;
		side = side_in;
	}

	bool within_cube(point a){
		bool loc = (abs(a.x_coordinate - center.x_coordinate) <= side) && 
                   (abs(a.y_coordinate - center.y_coordinate) <= side) &&
                   (abs(a.z_coordinate - center.z_coordinate) <= side);

        if(loc) return true;
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

int check_sign (float x){
	if(x < 0) return -1;
	if(x == 0) return 0;
	if(x > 0) return 1;
}

vec3 normal_at_point(point a, cube c){
		point dirn_from_cube_center = subtract_points(a, c.center);
		//Check for direction reversal
		if(a.x_coordinate * dirn_from_cube_center.x_coordinate < 0) return vec3(c.center, 1, 
																		point(check_sign(dirn_from_cube_center.x_coordinate),0,0));

		if(a.y_coordinate * dirn_from_cube_center.y_coordinate < 0) return vec3(c.center, 1, 
																		point(0, check_sign(dirn_from_cube_center.x_coordinate),0));

		if(a.z_coordinate * dirn_from_cube_center.z_coordinate < 0) return vec3(c.center, 1, 
																		point(0,0,check_sign(dirn_from_cube_center.z_coordinate)));																

}

void write_hit_info(hit_info& rec_in, float res_in, vec3& ray_in, cube& c_in){
		rec_in.t = res_in;
        rec_in.intersection_point = add_points(ray_in.origin, scale_point(ray_in.direction_vector, res_in));
        rec_in.normal_at_intersection = normal_at_point(rec_in.intersection_point, c_in);
		return;
	}

float hit(const vec3& r, double t_min, double t_max, cube c) {

	/*
	ax + t * bx  should belong in [cx - side, cx + side]
	Performing the same analysis for y and z coordinates we can take the minimum common element in the three sets 
	*/
	point a = r.origin;
	point b = r.direction_vector;

	// x - coordinate
	float tx_min = (c.center.x_coordinate - c.side - a.x_coordinate)/b.x_coordinate;
	float tx_max = (c.center.x_coordinate + c.side - a.x_coordinate)/b.x_coordinate;

	//y-- coordinate
	float ty_min = (c.center.y_coordinate - c.side - a.y_coordinate)/b.y_coordinate;
	float ty_max = (c.center.y_coordinate + c.side - a.y_coordinate)/b.y_coordinate;

	// z - coordinate
	float tz_min = (c.center.z_coordinate - c.side - a.z_coordinate)/b.z_coordinate;
	float tz_max = (c.center.z_coordinate + c.side - a.z_coordinate)/b.z_coordinate;

	return min_sets(tx_min, tx_max, ty_min, ty_max, tz_min, tz_max);
	
}

float min_sets(float x1, float x2, float y1, float y2, float z1, float z2){

	float num_arr[4] = {x1, x2, y1, y2};
	int n = sizeof(num_arr) / sizeof(num_arr[0]);
    std::sort(num_arr, num_arr + n);

	//Checking mutual exclusivity
	if((num_arr[0] == x1 && num_arr[1] == x2) || (num_arr[2] == x1 && num_arr[3] == x2)) return NAN;

	float a_1 = num_arr[1];
	float a_2 = num_arr[2];

	//Modifying arr values
	num_arr[0] = a_1;
	num_arr[1] = a_2;
	num_arr[2] = z1;
	num_arr[3] = z2;

	std::sort(num_arr, num_arr + n);

	//Checking mutual exclusivity
	if((num_arr[0] == a_1 && num_arr[1] == a_2) || (num_arr[2] == a_1 && num_arr[3] == a_2)) return NAN;

	return num_arr[1];
}

vec3 cubical_reflection(point intersection_in, vec3 normal_in, vec3 ray_in){
	point reflected_dirn = ray_in.direction_vector;
	
	//Changing the concerned coordinate
	if(normal_in.x_coordinate == 1) reflected_dirn.x_coordinate *= -1;
	if(normal_in.y_coordinate == 1) reflected_dirn.y_coordinate *= -1;
	if(normal_in.z_coordinate == 1) reflected_dirn.z_coordinate *= -1;
	
	

	vec3 ref(intersection_in, 1, reflected_dirn);
	return ref;
}
