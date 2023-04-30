import numpy as np
from numpy import *
import coordinates
from mayavi import mlab
from argparse import ArgumentParser
import time
import subprocess

#When animation should be saved to a movie
def SaveupdateAnimation(sx, sy, sz, r, locus_record):

    for i in range(len(locus_record)-1):
        #The ray
        x = locus_record[0:i+1,0]
        y = locus_record[0:i+1,1]
        z = locus_record[0:i+1,2]
        mlab.plot3d(x, y, z, color=(i/(len(locus_record)),
                                    1 - i/(len(locus_record)),
                                    i/(len(locus_record))), tube_radius= np.min(r)/10)


        #The background spheres
        [phi, theta] = np.mgrid[0:2 * np.pi:12j, 0:np.pi:12j]
        x_r = np.cos(phi) * np.sin(theta)
        y_r = np.sin(phi) * np.sin(theta)
        z_r = np.cos(theta)
        for k in range(len(sx)):
            c = r[k]/np.max(r) - 0.01
            mlab.mesh(r[k] * x_r + sx[k], 
                      r[k] * y_r + sy[k],
                      r[k] * z_r + sz[k],
                      color = (c,1 -c, 0.5 *c))
        
        mlab.orientation_axes()
        mlab.view(azimuth = i*180/110) #Adjusting the camera
        mlab.process_ui_events()
        mlab.savefig('anim_{idx}.png'.format(idx = i))

#Saves as 1080p movie
def save_as_movie(filename):
     # Define the command to execute
    command = [
        'ffmpeg',
        '-framerate', '10',
        '-i', 'anim_%d.png',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-s', '1920x1080',
        filename]
    subprocess.run(command, shell=True)



if __name__ == '__main__':
    parser = ArgumentParser(description='Argument parser for the ray_tracing program')
    parser.add_argument('-n', choices = [1,2,3,4,5,6], type = int, default = 4, help='Number of spheres between 1 & 6 inclusive')
    parser.add_argument('-x', type=float, default = 0, help='x-coordinate of the ray on screen')
    parser.add_argument('-y', type=float, default = 0, help='y-coordinate of the ray on screen')
    parser.add_argument('-t', type=float, default = 10, help='Time of animation')
    parser.add_argument(
        '-o',
        dest='filename', default='movie.mp4')
    
    args_dictionary = vars(parser.parse_args())
    s_cx, s_cy, s_cz, s_r, locus = coordinates.get_coordinates(args_dictionary['n'], args_dictionary['x'], 
                                                               args_dictionary['y'], args_dictionary['t']*2.5)

    SaveupdateAnimation(s_cx, s_cy, s_cz, s_r, locus)
    save_as_movie(args_dictionary['filename'])