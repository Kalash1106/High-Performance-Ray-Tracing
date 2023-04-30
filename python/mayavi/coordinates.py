import numpy as np

'''
Here (cx, cy, cz) is the center of a sphere i and r_array contains the corresponding radius
r_origin and r_direction are for the rays respectively.
i is the index for sphere in the world.
'''
def calc_t(cx_array, 
           cy_array,
           cz_array,
           r_array, 
           r_origin,
           r_direction):
    t_min = np.inf
    i_min = -1
    for i in range(len(cx_array)):

        a  = r_direction[0]**2 + r_direction[1]**2 + r_direction[2]**2

        half_b = (r_origin[0] - cx_array[i])*r_direction[0] + (r_origin[1] - cy_array[i])*r_direction[1] + (r_origin[2] - cz_array[i])*r_direction[2]
        
        c = (r_origin[0] - cx_array[i])**2 + (r_origin[1] - cy_array[i])**2 + (r_origin[2] - cz_array[i])**2 - r_array[i]**2

        discriminant = half_b * half_b - a * c
        if(discriminant>0):
            sqrtd = np.sqrt(discriminant)
            root = (-half_b - sqrtd) / a
            if (root > 0):
                if(t_min > root): 
                    t_min = root
                    i_min = i
            else:
                root = (-half_b + sqrtd) / a
                if (root > 0):
                    if(t_min > root): 
                        t_min = root
                        i_min = i

    return t_min, i_min

#Shot along the normal
def modify_dirn(cx, cy, cz, t, r_origin, r_direction):
    p_x = r_origin[0] + r_direction[0]*t - cx
    p_y = r_origin[1] + r_direction[1]*t - cy
    p_z = r_origin[2] + r_direction[2]*t - cz

    #New assignment for point
    r_origin[0] = r_origin[0] + t*r_direction[0]
    r_origin[1] = r_origin[1] + t*r_direction[1]
    r_origin[2] = r_origin[2] + t*r_direction[2]

    #New assignment for direction
    l2 = np.linalg.norm([p_x, p_y, p_z])
    r_direction[0] = p_x/l2
    r_direction[1] = p_y/l2
    r_direction[2] = p_z/l2

def insert_trajectory_points(locus_rec, velocity, dt, hit_points_rec, ray_dirn_rec, t_rec):
    #Each independent portion of the ray
    for i in range(len(hit_points_rec)):
        local_start = hit_points_rec[i]
        t_local = 0
        #For smoothness
        locus_rec.append(local_start) #Contains points for that portion

        while(True):
            t_local = t_local + velocity*dt
            if(t_local > t_rec[i]):
                break
            locus_rec.append(local_start + ray_dirn_rec[i]*t_local)

                
def get_coordinates(n_spheres = 2, x_coordinate = 0, y_coordinate = 0, time = 12.5):
    #Setting up my world
    cx_arr = np.random.uniform(-20, 20, size=(n_spheres))
    cy_arr = np.random.uniform(-20, 20, size=(n_spheres))
    cz_arr = np.random.uniform(1, 40, size=(n_spheres))
    r = np.random.uniform(1, 10, size=(n_spheres))

    # cx_arr = np.array([0, 1])
    # cy_arr = np.array([0, 0])
    # cz_arr = np.array([2, -2])
    # r = np.array([1,1])

    #Ray Params
    r_orig = np.array([0,0,0])
    temp_d = np.array([x_coordinate, y_coordinate, 1]) #The point on projection screen from where ray would pass
    r_dirn = temp_d/np.linalg.norm(temp_d)
    total_distance = 0

    #Global lists
    locus_rec = []
    hit_points_rec = [r_orig.copy()]
    ray_dirn_rec = [r_dirn.copy()]
    t_rec = []
    depth = 25
    infinite_travel = 50

    while(depth>=0):
        t, i =calc_t(cx_arr, cy_arr, cz_arr, r, r_orig, r_dirn)
        if(t == np.inf): 
            total_distance = total_distance + infinite_travel
            t_rec.append(infinite_travel)
            break
        t_rec.append(t)
        total_distance = total_distance + t
        modify_dirn(cx_arr[i], cy_arr[i], cz_arr[i], t, r_orig, r_dirn)
        hit_points_rec.append(r_orig.copy())
        ray_dirn_rec.append(r_dirn.copy())
        depth = depth - 1

    if(depth < 0): 
        t_rec.append(1)
        total_distance = total_distance + 1

    insert_trajectory_points(locus_rec, total_distance/time, 0.25, hit_points_rec, ray_dirn_rec, t_rec)
    locus_rec = np.array(locus_rec)
    return cx_arr, cy_arr, cz_arr, r, locus_rec