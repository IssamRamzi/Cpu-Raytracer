from Core.hittable import Hittable, HitRecord
from Core.ray import Ray
from Math.vector import Vector3, Point3
from Utils.intervals import Interval
from Core.material import Material
from math import sqrt


"""
Source : https://raytracing.github.io/books/RayTracingInOneWeekend.html#addingasphere 
(Cx − x)^2+(Cy − y)^2+(Cz − z)^ = (C − P)⋅(C − P) = r2 = any point P that satisfies this equation is on the sphere
To check the intersection between the rays and the sphere we simply modify the equation : (C − P(t)) ⋅ (C − P(t) ) = r²
                                                                                          (C − (origin + t * direction)) ⋅ (C − (origin + t * direction)) = r2 
"""
class Sphere(Hittable):
    def __init__(self, center : Point3, radius : float, material : Material = None):
        super().__init__()
        self.center = center
        self.radius = radius
        self.material = material 

    def hit(self, r, interval : Interval, hit_record): 
        oc = self.center - r.origin
        a = r.direction.length_squared()
        half_b = r.direction.dot(oc)
        c = oc.length_squared() - self.radius**2

        delta = half_b*half_b - a*c
        if delta < 0:
            return False

        sqrtd = sqrt(delta)

        root = (half_b - sqrtd) / a

        if root < interval.min_val: 
            root = (half_b + sqrtd) / a
            if root < interval.min_val:
                return False
            
        if root > interval.max_val: 
            return False
            
        hit_record.distance = root
        hit_record.point = r.at(hit_record.distance)
        outward_normal = (hit_record.point - self.center ) / self.radius
        hit_record.set_face_normal(r, outward_normal)
        hit_record.material = self.material

        return True