from Core.material import *
from Primitives.primitives import *


class MaterialFactory:
    @staticmethod
    def create(params):
        mat_type = params["type"]

        if mat_type == "Lambertian":
            return LambertianCreator.create(params)

        elif mat_type == "Metal":
            return MetalCreator.create(params)

        elif mat_type == "DiffuseLight":
            return DiffuseLightCreator.create(params)

        raise ValueError(f"Unknown material type: {mat_type}")


class LambertianCreator:
    @staticmethod
    def create(params):
        c = params["color"]
        return Lambertian(Color3(c[0], c[1], c[2]))


class MetalCreator:
    @staticmethod
    def create(params):
        c = params["color"]
        return Metal(Color3(c[0], c[1], c[2]))

class DiffuseLightCreator:
    @staticmethod
    def create(params):
        c = params["color"]
        return DiffuseLight(Color3(c[0], c[1], c[2]))
    
class PrimitiveFactory:
    @staticmethod
    def create(params, material):
        prim_type = params["type"]

        if prim_type == "Sphere":
            return SphereCreator.create(params, material)
        
        elif prim_type == "Plane":
            return PlaneCreator.create(params, material)
        
        raise ValueError(f"Unknown primitive type: {prim_type}")

class SphereCreator:
    @staticmethod
    def create(params, material):
        center = params["center"]
        radius = params["radius"]
        return Sphere(Point3(center[0], center[1], center[2]), radius, material)


class PlaneCreator:
    @staticmethod
    def create(params, material):
        bot_left = params["bot_left"]
        v = params["y_vector"]
        u = params["x_vector"]
        return Plane(
            Point3(bot_left[0], bot_left[1], bot_left[2]),
            Vector3(v[0], v[1], v[2]),
            Vector3(u[0], u[1], u[2]),
            material
        )
