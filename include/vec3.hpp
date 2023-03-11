#pragma once
#include <cmath>
#include <iostream>

class vec3 {
public:
    double e[3];

    vec3() : e{0,0,0} {}
    vec3(double e0, double e1, double e2) : e{e0, e1, e2} {}

    double x() const;
    double y() const;
    double z() const;

    vec3 operator-() const;

    double operator[](int i) const;
    double& operator[](int i);

    vec3& operator+=(const vec3 &v);
    vec3& operator*=(const double t);
    vec3& operator/=(const double t);

    double length() const;
    double length_squared() const;
};

// Type aliases for vec3
using point3 = vec3; // 3D point
using color = vec3;  // RGB color