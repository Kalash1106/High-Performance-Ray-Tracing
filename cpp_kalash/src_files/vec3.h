#pragma once
#include <math.h>
#define eye point(0,0,0)
#define temp_vector vec3(eye, eye)

class point
{
public:    
    float x_coordinate;
    float y_coordinate;
    float z_coordinate;

    point(){}

    point(float x, float y, float z){
        x_coordinate = x;
        y_coordinate = y;
        z_coordinate = z;
    }
};

point scale_point(point a, float scale){
    point c;
    c.x_coordinate = a.x_coordinate * scale;
    c.y_coordinate = a.y_coordinate * scale;
    c.z_coordinate = a.z_coordinate * scale;
    return c;
}

point add_points(point a, point b){
    point c(0,0,0);
    c.x_coordinate = a.x_coordinate + b.x_coordinate;
    c.y_coordinate = a.y_coordinate + b.y_coordinate;
    c.z_coordinate = a.z_coordinate + b.z_coordinate;
    return c;
}

point subtract_points(point a, point b){
    point c(0,0,0);
    c.x_coordinate = a.x_coordinate - b.x_coordinate;
    c.y_coordinate = a.y_coordinate - b.y_coordinate;
    c.z_coordinate = a.z_coordinate - b.z_coordinate;
    return c;
}


point multiply_points(point a, point b){
    point c(0,0,0);
    c.x_coordinate = a.x_coordinate * b.x_coordinate;
    c.y_coordinate = a.y_coordinate * b.y_coordinate;
    c.z_coordinate = a.z_coordinate * b.z_coordinate;
    return c;
}

point divide_points(point a, point b){
    point c(0,0,0);
    c.x_coordinate = a.x_coordinate / b.x_coordinate;
    c.y_coordinate = a.y_coordinate / b.y_coordinate;
    c.z_coordinate = a.z_coordinate / b.z_coordinate;
    return c;
}


class vec3 : public point
{
public:
    point origin;
    float t;
    point direction_vector; 

    vec3(){}   

    //Vector having origin o_in, parameter t_in and direction vector b_in which would be made unit automatically
    vec3(point o_in, float t_in, point b_in){
        origin = o_in;
        t = t_in;
        direction_vector = b_in;

        make_dirn_vec_unit();
    }

    //vector passing through 2 points a and b
    vec3(point a, point b){
        origin = a;
        direction_vector = subtract_points(b,a);
        make_dirn_vec_unit();
        t = 1;
    }

    void make_dirn_vec_unit(){
        float l2_a = sqrt(direction_vector.x_coordinate * direction_vector.x_coordinate +
                          direction_vector.y_coordinate * direction_vector.y_coordinate +
                          direction_vector.z_coordinate * direction_vector.z_coordinate);
    direction_vector.x_coordinate /= l2_a;
    direction_vector.y_coordinate /= l2_a;
    direction_vector.z_coordinate /= l2_a;
    return;

    }
};

point end_point_of_vector(vec3 a){
    point tip;
    tip.x_coordinate = a.origin.x_coordinate + a.t * a.direction_vector.x_coordinate;
    tip.y_coordinate = a.origin.y_coordinate + a.t * a.direction_vector.y_coordinate;
    tip.z_coordinate = a.origin.z_coordinate + a.t * a.direction_vector.z_coordinate;
    return tip;
}


float l2_norm(vec3 a){
    point tip = end_point_of_vector(a);
    float l2 = sqrt(tip.x_coordinate * tip.x_coordinate + 
                    tip.y_coordinate * tip.y_coordinate + 
                    tip.z_coordinate * tip.z_coordinate);
    return l2;
}

float l2_point_norm(point a_in){
    float l2 = sqrt(a_in.x_coordinate * a_in.x_coordinate + 
                    a_in.y_coordinate * a_in.y_coordinate + 
                    a_in.z_coordinate * a_in.z_coordinate);
    return l2;

}

point unit_point_vec(point a){
    point tip_a;
    float l2_a = sqrt(a.x_coordinate * a.x_coordinate +
                 a.y_coordinate * a.y_coordinate +
                 a.z_coordinate * a.z_coordinate);
    tip_a.x_coordinate /= l2_a;
    tip_a.y_coordinate /= l2_a;
    tip_a.z_coordinate /= l2_a;
    return tip_a;
}

point unit_vector(vec3 a){
    point tip_a = end_point_of_vector(a);
    float l2_a = l2_norm(a);
    tip_a.x_coordinate /= l2_a;
    tip_a.y_coordinate /= l2_a;
    tip_a.z_coordinate /= l2_a;
    return tip_a;
}

float dot_product(point a, point b){
    float dot = a.x_coordinate * b.x_coordinate +
                a.y_coordinate * b.y_coordinate +
                a.z_coordinate * b.z_coordinate;
    return dot;
}

//@brief Vector product of two vectors. Make sure to have origin as (0,0,0) and t = 1 
point cross_product(point a, point b){
    point c;
    c.x_coordinate = a.y_coordinate * b.z_coordinate - 
                    a.z_coordinate * b.y_coordinate;

    c.y_coordinate = - (a.x_coordinate * b.z_coordinate) + 
                        a.z_coordinate * b.x_coordinate;

    c.z_coordinate = a.x_coordinate * b.y_coordinate
                                    - a.y_coordinate * b.x_coordinate;

    return c;
}


vec3 vector_addition(vec3 a, vec3 b){
    vec3 c(point(0,0,0), 0, point(0,0,0));
    c.origin = add_points(a.origin, b.origin);
    c.direction_vector = add_points(a.direction_vector, b.direction_vector);
    return c;
}

vec3 vector_subtraction(vec3 a, vec3 b){
    vec3 c(point(0,0,0), 0, point(0,0,0));
    c.origin = subtract_points(a.origin, b.origin);
    c.direction_vector = subtract_points(a.direction_vector, b.direction_vector);
    return c;
}



 