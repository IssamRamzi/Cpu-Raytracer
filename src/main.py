from Camera.camera import *
from Primitives.primitives import *
from Core.material import *
import sys
from Utils.config_loader import ConfigLoader
from Core.object_factory import MaterialFactory

import time

SAMPLES_PER_PIXEL = 10
CAMERA_WIDTH = 400

def process(config, output):
    

    material_ground = Lambertian(Color3(0.8, 0.3, 0.3))
    material_center = Lambertian(Color3(0.1, 0.2, 0.1))
    material_left   = Metal(Color3(0.8, 0.8, 0.8))
    material_right  = Metal(Color3(0.8, 0.6, 0.2))


    world = HittableList()
    world.add(Sphere(Point3(0,-100.5,-3), 100, material_ground))
    world.add(Sphere(Point3(0.0,0,-1.0), 0.5, material_center))
    world.add(Sphere(Point3(1.5,0,-2.0), 0.5, material_left))
    world.add(Sphere(Point3(-1.5,0,-2.0), 0.5, material_right))
    # world.add(Plane(Point3(-2, -.8, -4), Vector3(1.5 * 3, 0, 0), Vector3(0, 1 * 3, 0)))

    camera = Camera(camera["width"], (16.0 / 9.0), samples_per_pixel=camera["samples_per_pixel"], max_ray_bounces=50) # you guys can change the last variable for sampling rate, 5 is already high in python
    camera.render(world, output = output)

if __name__ == "__main__": # for args we'll have : args[1] = config_file_path, and args[2] = output_path.ppm
    args = sys.argv
    assert len(args) == 3, "Not enough arguments : [CONFIG_PATH] [OUTPUT_PATH]" 
    config_file, output = args[1], args[2]
    start = time.time()
    process(config_file, output)
    print(f"Took {time.time() - start}s")