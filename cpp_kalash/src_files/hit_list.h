#ifndef HITTABLE_LIST_H
#define HITTABLE_LIST_H

#include "vec3.h"
#include "sphere.h"
#include <list>

class collection_of_spheres{
    public:
        std::list <sphere> sphere_collection;
        collection_of_spheres(){}

        void add_sphere(sphere s_in){
            sphere_collection.push_back(s_in);
            return;
        }
        bool hittable_list(const vec3& r, double t_min, double t_max, hit_info& rec);

};


bool collection_of_spheres::hittable_list(const vec3& r, double t_min, double t_max, hit_info& rec){
    hit_info temp_rec;
    bool hit_anything = false;
    auto closest_so_far = t_max;

    for (auto const sph_i : sphere_collection) {
        if (hit(r, -INFINITY, INFINITY, sph_i) != NAN) {
            hit_anything = true;
            closest_so_far = temp_rec.t;
            rec = temp_rec;
        }
    }

    return hit_anything;
}

#endif
