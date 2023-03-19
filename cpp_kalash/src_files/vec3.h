#pragma once
class point
{
public:    
    float x_coordinate;
    float y_coordinate;
    float z_coordinate;

    point(float x = 0, float y = 0, float z = 0){
        x_coordinate = x;
        y_coordinate = y;
        z_coordinate = z;
    }
};

point add_points(point a, point b, point c){
    c.x_coordinate = a.x_coordinate + b.x_coordinate;
    c.y_coordinate = a.y_coordinate + b.y_coordinate;
    c.z_coordinate = a.z_coordinate + b.z_coordinate;
    return c;
}

point subtract_points(point a, point b, point c){
    c.x_coordinate = a.x_coordinate - b.x_coordinate;
    c.y_coordinate = a.y_coordinate - b.y_coordinate;
    c.z_coordinate = a.z_coordinate - b.z_coordinate;
    return c;
}


point multiply_points(point a, point b, point c){
    c.x_coordinate = a.x_coordinate * b.x_coordinate;
    c.y_coordinate = a.y_coordinate * b.y_coordinate;
    c.z_coordinate = a.z_coordinate * b.z_coordinate;
    return c;
}

point divide_points(point a, point b, point c){
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

    vec3(point o_in, float t_in, point b_in){
        origin = o_in;
        t = t_in;
        direction_vector = b_in;
    }
};

point end_point_of_vector(vec3 a){
    point tip;
    tip.x_coordinate = a.origin.x_coordinate + a.t * a.direction_vector.x_coordinate;
    tip.y_coordinate = a.origin.y_coordinate + a.t * a.direction_vector.y_coordinate;
    tip.z_coordinate = a.origin.z_coordinate + a.t * a.direction_vector.z_coordinate;
    return tip;
}

vec3 dot_product(vec3 a, vec3 b, vec3 c){
    c.direction_vector.x_coordinate = a.direction_vector.x_coordinate * b.direction_vector.x_coordinate;
    c.direction_vector.y_coordinate = a.direction_vector.y_coordinate * b.direction_vector.y_coordinate;
    c.direction_vector.z_coordinate = a.direction_vector.z_coordinate * b.direction_vector.z_coordinate;
    return c;
}

vec3 cross_product(vec3 a, vec3 b, vec3 c){
    c.direction_vector.x_coordinate = a.direction_vector.y_coordinate * b.direction_vector.z_coordinate
                                    - a.direction_vector.z_coordinate * b.direction_vector.y_coordinate;

    c.direction_vector.y_coordinate = - (a.direction_vector.x_coordinate * b.direction_vector.z_coordinate)
                                    + a.direction_vector.z_coordinate * b.direction_vector.x_coordinate;

    c.direction_vector.z_coordinate = a.direction_vector.x_coordinate * b.direction_vector.y_coordinate
                                    - a.direction_vector.y_coordinate * b.direction_vector.x_coordinate;

    return c;
}


vec3 vector_addition(vec3 a, vec3 b, vec3 c){
    c.origin = add_points(a.origin, b.origin, c.origin);
    c.direction_vector = add_points(a.direction_vector, b.direction_vector, c.direction_vector);
    return c;
}

vec3 vector_subtraction(vec3 a, vec3 b, vec3 c){
    c.origin = subtract_points(a.origin, b.origin, c.origin);
    c.direction_vector = subtract_points(a.direction_vector, b.direction_vector, c.direction_vector);
    return c;
}



 