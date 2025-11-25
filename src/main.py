from Math import Vector3, Color3, Point3
from Display import PPMWriter
from Core import *

def ray_color(r : Ray) -> Color3:
    if(hit_sphere(Vector3(0,0,-1), 0.5, r)):
        return Color3(1,0,0)
    unit_dir = r.direction.normalize()
    a = 0.5 * (unit_dir.y + 1.0)
    return (1.0 - a) * Color3(1,1,1) + a * Color3(0.5, 0.7, 1.0)


# Camera and image Setup
# Source : https://raytracing.github.io/images/fig-1.04-pixel-grid.jpg
aspect_ratio = 16.0 / 9.0
image_width = 400
image_height = int(image_width / aspect_ratio)

viewport_height = 2.0
viewport_width = viewport_height * (image_width / image_height)

camera_center = Point3(0, 0, 0)

viewport_u = Vector3(viewport_width, 0, 0)
viewport_v = Vector3(0, -viewport_height, 0)

pixel_delta_u = viewport_u / image_width
pixel_delta_v = viewport_v / image_height

viewport_upper_left = camera_center - Vector3(0,0,1) - viewport_u/2 - viewport_v/2
pixel100_loc = viewport_upper_left + 0.5 * (pixel_delta_u + pixel_delta_v)


image = []

for j in range(image_height):
    row = []
    for i in range(image_width):
        pixel_center = viewport_upper_left + (i+0.5)*pixel_delta_u + (j+0.5)*pixel_delta_v
        ray_direction = pixel_center - camera_center
        r = Ray(camera_center, ray_direction)
        row.append(ray_color(r))
    image.append(row)

# Render
print(f"Début du rendu: {image_width}x{image_height}")
with open("output.ppm", "w") as f:
    writer = PPMWriter(image_width, image_height, f)
    writer.write_image(image)