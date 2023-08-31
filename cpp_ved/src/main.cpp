#include "vec3.hpp"
#include "utils.hpp"
#include "color.hpp"
#include "hittable_list.hpp"
#include "sphere.hpp"
#include "camera.hpp"

#include <iostream>
#include <cstdlib>


color ray_color(const ray& r, const hittable& world, int depth) {
    if (depth <= 0) return color(0, 0, 0);

    hit_record rec;
    if (world.hit(r, 0.001, infinity, rec)) {
        point3 target = rec.p + rec.normal + random_in_unit_sphere();
        return 0.5 * ray_color(ray(rec.p, target - rec.p), world, depth-1);
    }

    vec3 unit_direction = unit_vector(r.direction());
    auto t = 0.5*(unit_direction.y() + 1.0);
    return (1.0-t)*color(1.0, 1.0, 1.0) + t*color(0.5, 0.7, 1.0);
}

int main(int argc, char *argv[]) {
    int s = 5;
    int d = 5;
    int n = 1;
    
    if (argc < 4) {
        std::cout << "not enough args!" << std::endl;
        std::cout << "usage:" << std::endl;
        std::cout << "  " << argv[0] << " samples depth nspheres" << std::endl;
        exit(EXIT_FAILURE);
    }

    s = atoi(argv[1]);
    d = atoi(argv[2]);
    n = atoi(argv[3]);
    // std::cout << s << d << n;

    if (n > 3) {
        std::cout << "scenes not configured for n > 3" << std::endl;
        exit(EXIT_FAILURE);
    }

    // Image

    const auto aspect_ratio = 16.0 / 9.0;
    const int image_width = 400;
    const int image_height = static_cast<int>(image_width / aspect_ratio);
    const int samples_per_pixel = s;
    const int max_depth = d;

    // World
    hittable_list world;
    world.add(std::make_shared<sphere>(point3(0,-100.5,-1), 100));
    world.add(std::make_shared<sphere>(point3(0,0,-1), 0.5));
    switch (n) {
    case 3:
        world.add(std::make_shared<sphere>(point3(-1,0,-1), 0.5));
    
    case 2:
        world.add(std::make_shared<sphere>(point3(1,0,-1), 0.5));
    }

    // Camera
    camera cam;

    // Render

    std::cout << "P3\n" << image_width << " " << image_height << "\n255\n";

    for (int j = image_height-1; j >= 0; --j) {
        std::cerr << "\rScanlines remaining: " << j << ' ' << std::flush;
        for (int i = 0; i < image_width; ++i) {
            color pixel_color(0, 0, 0);
            for (int s = 0; s < samples_per_pixel; ++s) {
                auto u = (i + random_double()) / (image_width-1);
                auto v = (j + random_double()) / (image_height-1);
                ray r = cam.get_ray(u, v);
                pixel_color += ray_color(r, world, max_depth);
            }
            write_color(std::cout, pixel_color, samples_per_pixel);
        }
    }

    std::cerr << "\nDone.\n";
    return 0;
}