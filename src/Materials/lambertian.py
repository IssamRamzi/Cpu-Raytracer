from Core.ray import Ray
from Materials.material import Material
from Math.vector import Vector3

class Lambertian(Material):
    def __init__(self, albedo_color) -> None:
        super().__init__()
        self.albedo_color = albedo_color

    def scatter(self, ray, hit_record, color_attenuation, scattered):
        scatter_direction = hit_record.normal + Vector3.random_unit_vec()
        scattered = Ray(hit_record.point, scatter_direction)
        color_attenuation = self.albedo_color
        return (scattered, color_attenuation, True)


