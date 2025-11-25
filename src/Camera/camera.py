from math import trunc
from Math.vector import Point3, Vector3, Color3, random_on_hemisphere
from Core.primitives import hit_sphere
from Core.ray import Ray
from Display.PPMWriter import PPMWriter
import random

class Camera:
    def __init__(self, img_width, aspect_ratio, samples_per_pixel, max_ray_bounces) -> None:
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

    def sample_square(self):
        return Vector3(random.random() - 0.5, random.random() - 0.5, 0)
    
    def get_ray(self, i, j):
        offset = self.sample_square()
        pixel_sample = self._pixel00_loc + ((i + offset.x) * self._pixel_delta_u) + ((j + offset.y) * self._pixel_delta_v)
        ray_origin = self._center
        ray_direction = pixel_sample - ray_origin
        return Ray(ray_origin, ray_direction)

    def ray_color(self, ray, max_bounce_count):
        if self._max_ray_bounces <= 0: 
            return Color3(0, 0, 0)

        t = hit_sphere(Vector3(0,0,-1), 0.5, ray)
        if t > 0.001:
            point = ray.at(t)
            normal = (point - Vector3(0, 0, -1)).normalize()
            vec_direction = random_on_hemisphere(normal)
            new_ray = Ray(point, vec_direction)
            return 0.5 * self.ray_color(new_ray, max_bounce_count - 1)
            #N = (ray.at(t) - Vector3(0,0,-1)).normalize()
            #return 0.5 * Color3(N.x + 1, N.y + 1, N.z + 1)

        unit_dir = ray.direction.normalize()
        a = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - a) * Color3(1,1,1) + a * Color3(0.5, 0.7, 1.0)

    def initialize_camera(self):
        self._img_height = int(self._img_width / self._aspect_ratio)
        self._center = Point3(0, 0, 0)
        self._pixel_sample_scale = 1.0 / self._samples_per_pixel

        #focal_length = 1.0
        viewport_height = 2.0
        viewport_width = viewport_height * (self._img_width / self._img_height)

        viewport_u = Vector3(viewport_width, 0, 0)
        viewport_v = Vector3(0, -viewport_height, 0)

        self._pixel_delta_u = viewport_u / self._img_width
        self._pixel_delta_v = viewport_v / self._img_height

        viewport_upper_left = self._center - Vector3(0, 0, 1) - viewport_u/2 - viewport_v/2
        self._pixel00_loc = viewport_upper_left + 0.5 * (self._pixel_delta_u + self._pixel_delta_v)


    def write_img_to_file(self):
        with open("output.ppm", "w") as f:
            writer = PPMWriter(self._img_width, self._img_height, f)
            writer.write_image(self._img_ro_render)


    def render(self):
        #TODO: add hittables abstraction layer t primitives
        self.initialize_camera()
        
        for j in range(self._img_height):
            row = []
            for i in range(self._img_width):
                color = Color3(0, 0, 0)
                for sample in range(self._samples_per_pixel):
                    ray = self.get_ray(i, j)
                    color += self.ray_color(ray, self._max_ray_bounces)
                    print(f"Sampling : {sample}")

                #pixel_center = self._pixel00_loc + (i+0.5)*self._pixel_delta_u + (j+0.5)*self._pixel_delta_v
                #ray_direction = pixel_center - self._center
                #r = Ray(self._center, ray_direction)
                row.append(color * self._pixel_sample_scale)
            self._img_ro_render.append(row)

        self.write_img_to_file()


