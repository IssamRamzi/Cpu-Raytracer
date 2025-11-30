import math
from Math.vector import Point3, Vector3, Color3, random_on_hemisphere
from Core.hittable import *
from Core.ray import Ray
from Display.PPMWriter import PPMWriter
from Utils.intervals import Interval, zeroExToInf
import random
import concurrent.futures
import functools
import multiprocessing

class Camera:
    def __init__(self, img_width, aspect_ratio, samples_per_pixel, max_ray_bounces, vfov, vup, lookfrom, lookat) -> None:
        self._img_width = img_width
        self._aspect_ratio = aspect_ratio
        self._img_height = 0
        self._center = None
        self._pixel00_loc = None
        self._pixel_delta_u = None
        self._pixel_delta_v = None
        self._img_ro_render = []
        self._samples_per_pixel = samples_per_pixel
        self._pixel_sample_scale = None
        self._max_ray_bounces = max_ray_bounces
        self._vfov = vfov
        self._camera_u_right = None
        self._camera_v_up = None
        self._camera_w_opposite = None
        self._vup = vup
        self._lookfrom = lookfrom
        self._lookat = lookat

    def sample_square(self):
        return Vector3(random.random() - 0.5, random.random() - 0.5, 0)

    def get_ray(self, i, j):
        offset = self.sample_square()
        pixel_sample = self._pixel00_loc + ((i + offset.x) * self._pixel_delta_u) + ((j + offset.y) * self._pixel_delta_v)
        ray_origin = self._center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def ray_color(self, ray : Ray, world, max_bounce_count):
        if max_bounce_count <= 0: 
            return Color3(0, 0, 0)

        rec = HitRecord()
        # if world.hit(ray, zeroExToInf, rec):
        #     # vec_direction = random_on_hemisphere(rec.normal)
        #     vec_direction = rec.normal + Vector3.random_unit_vec()
        #     new_ray = Ray(rec.point, vec_direction)

        #     return 0.5 * self.ray_color(new_ray, world, max_bounce_count - 1)

        if world.hit(ray, zeroExToInf, rec):
            # vec_direction = random_on_hemisphere(rec.normal)
            struct = [None, None]
            if rec.material.scatter(ray, rec, struct):
                attenuation = struct[0]
                scattered = struct[1]
                return attenuation * self.ray_color(scattered, world, max_bounce_count - 1)
            return Color3(0,0,0)



        unit_dir = ray.direction.normalize()
        a = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - a) * Color3(1,1,1) + a * Color3(0.5, 0.7, 1.0)

    def process_scanlines(self, j, world):
        row_colors = []
        for i in range(self._img_width):
            pixel_color = Color3(0, 0, 0)
            for sample in range(self._samples_per_pixel):
                ray = self.get_ray(i, j)
                pixel_color += self.ray_color(ray, world, self._max_ray_bounces)
            final_color = pixel_color * self._pixel_sample_scale
            row_colors.append(final_color)
        return row_colors

    def initialize_camera(self):
        self._img_height = int(self._img_width / self._aspect_ratio)
        self._center = self._lookfrom
        self._pixel_sample_scale = 1.0 / self._samples_per_pixel
        theta = math.radians(self._vfov)
        h = math.tan(theta/2)

        focal_length = (self._lookfrom - self._lookat).length()
        self._camera_w_opposite = Vector3.unit_vector(self._lookfrom - self._lookat)
        self._camera_u_right = Vector3.unit_vector(Vector3.cross(self._vup, self._camera_w_opposite))
        self._camera_v_up = Vector3.cross(self._camera_w_opposite, self._camera_u_right)
        viewport_height = 2 * h * focal_length
        viewport_width = viewport_height * (self._img_width / self._img_height)

        viewport_u = viewport_width * self._camera_u_right
        viewport_v = viewport_height * -self._camera_v_up 

        self._pixel_delta_u = viewport_u / self._img_width
        self._pixel_delta_v = viewport_v / self._img_height

        viewport_upper_left = self._center - (focal_length * self._camera_w_opposite) - viewport_u/2 - viewport_v/2
        self._pixel00_loc = viewport_upper_left + 0.5 * (self._pixel_delta_u + self._pixel_delta_v)


    def write_img_to_file(self, output):
        with open(output, "w") as f:
            writer = PPMWriter(self._img_width, self._img_height, f)
            writer.write_image(self._img_ro_render)


    def render(self, world, output = "output.ppm"):
        #TODO: add hittables abstraction layer t primitives
        self.initialize_camera()
        num_cores = multiprocessing.cpu_count()
        print("Total Cpu Cores : " + str(num_cores))
        with concurrent.futures.ProcessPoolExecutor(max_workers= num_cores) as executor:
            func = functools.partial(self.process_scanlines, world=world)
            results = executor.map(func, range(self._img_height))
            self._img_ro_render = list(results)
        self.write_img_to_file(output)


