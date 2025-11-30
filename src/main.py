from Camera.camera import *
from Primitives.primitives import *
from Core.material import *

import time

SAMPLES_PER_PIXEL = 150
CAMERA_WIDTH = 1600

def main():

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

    camera = Camera(CAMERA_WIDTH, (16.0 / 9.0), samples_per_pixel=SAMPLES_PER_PIXEL, max_ray_bounces=50) # you guys can change the last variable for sampling rate, 5 is already high in python
    camera.render(world, output = "Results/Sortie_1600x900_150.ppm")

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Took {time.time() - start}s")