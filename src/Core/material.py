from .hittable import *
from .ray import Ray
from .texture import SolidColor, Texture

class Material:
    def __init__(self):
        pass

    def scatter(self, ray_in, hit_record, scattered) -> bool:
        pass

    def emitted(self, u, v, point):
        return Color3(0, 0, 0)


class Lambertian(Material) :
    def __init__(self, albedo : Color3):
        self.albedo = albedo
        self._texure = SolidColor(albedo)

    # struct : [attenuation, scattered]
    def scatter(self, ray_in, hit_record, struct) -> bool: # TODO : fix pour que le passage de (attenuation, scattered) soit par ref& ou struct ?
        scatter_direction = hit_record.normal + Vector3.random_unit_vec()        

        # catch the degenerate scatter dir
        if scatter_direction.near_zero():
            scatter_direction = hit_record.normal

        struct[1] = Ray(hit_record.point, scatter_direction)
        struct[0] = self._texure.value(hit_record._u, hit_record._v, hit_record.point)
        return True

class Metal(Material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, ray_in, hit_record, struct) -> bool:

        reflected = Vector3.reflect(ray_in.direction, hit_record.normal)
        struct[1] = Ray(hit_record.point, reflected)

        struct[0] = self.albedo
        return True

class DiffuseLight(Material):
    def __init__(self, albedo):
        self._albedo = albedo
        self._texture = SolidColor(albedo)

    def emitted(self, u, v, point):
        return self._texture.value(u, v, point)


