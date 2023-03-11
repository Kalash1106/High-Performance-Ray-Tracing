#include <iostream>
#include "vec3.hpp"

int main() {
    vec3 v(1, 2, 3);

    std::cout << v.x() << v.y() << v.z() << std::endl;

    return 0;
}