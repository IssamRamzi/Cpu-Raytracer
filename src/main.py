from Camera.camera import *
import time
def main():
    world = HittableList()
    world.add(Sphere(Point3(0,-100.5,-3), 100))
    world.add(Sphere(Point3(-2.5,0.3,-3.75), 1.75))
    world.add(Sphere(Point3(0.0,0,-1.0), 0.35))
    world.add(Sphere(Point3(2.5,0.3,-3.75), 1.75))

    camera = Camera(400, (16.0 / 9.0))
    camera.render(world)



if __name__ == "__main__":
    start = time.time()
    main()
    print(f"Took {time.time() - start}s")
