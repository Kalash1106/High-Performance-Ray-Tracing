#pragma once
#include "vec3.h"

class pixel
{
public:
    int red, blue, green; //rgb values
    point coordinate;
    

    pixel(point co_ord, int red_in, int blue_in, int green_in){
        coordinate = co_ord;
        red = red_in;
        blue = blue_in;
        green = green_in;
    }
};


pixel add_pixel_color(pixel a, pixel b, pixel c){
    c.red = a.red + b.red;
    c.green = a.green + b.green;
    c.blue = a.blue + b.blue;

    return c;
}

pixel subtract_pixel_color(pixel a, pixel b, pixel c){
    c.red = a.red - b.red;
    c.green = a.green - b.green;
    c.blue = a.blue - b.blue;

    return c;
}

pixel multiply_pixel_color(pixel a, pixel b, pixel c){
    c.red = a.red * b.red;
    c.green = a.green * b.green;
    c.blue = a.blue * b.blue;

    return c;
}

pixel divide_pixel_color(pixel a, pixel b, pixel c){
    c.red = a.red / b.red;
    c.green = a.green / b.green;
    c.blue = a.blue / b.blue;

    return c;
}

