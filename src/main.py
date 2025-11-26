from Camera.camera import *
from Core.sphere import *
from Core.plane import *

import time


def main():

    world = HittableList()
    world.add(Sphere(Point3(0,-100.5,-3), 100))
    world.add(Sphere(Point3(0.0,0,-1.0), 0.5))
    # world.add(Plane(Point3(-2, -1, -3), Vector3(4, 0, 0), Vector3(0, 2, 0)))

    camera = Camera(720, (16.0 / 9.0), 30, 50) #you guys can change the last variable for sampling rate, 5 is already high in python
    camera.render(world)

if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Took {time.time() - start}s")
