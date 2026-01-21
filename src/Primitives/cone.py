from Core.hittable import Hittable, HitRecord
from Core.ray import Ray
from Math.vector import Vector3, Point3
from Utils.intervals import Interval
from Core.material import Material
from math import sqrt

class Cone(Hittable):
    def __init__(self, center: Point3, radius: float, height: float, material: Material = None):
        super().__init__()
        self.center = center    
        self.radius = radius
        self.height = height
        self.material = material 

    def hit(self, r, interval: Interval, hit_record): 
        oc = r.origin - self.center
        k = self.radius / self.height
        k2 = k * k
        a = r.direction.x**2 + r.direction.z**2 - k2 * r.direction.y**2
        b = 2 * (oc.x * r.direction.x + oc.z * r.direction.z - k2 * oc.y * r.direction.y)
        c = oc.x**2 + oc.z**2 - k2 * oc.y**2

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False
        
        sqrtd = sqrt(discriminant)
        root = (-b - sqrtd) / (2.0 * a)
        if not interval.surrounds(root):
            root = (-b + sqrtd) / (2.0 * a)
            if not interval.surrounds(root):
                return False

        hit_point = r.at(root)
        relative_y = hit_point.y - self.center.y
        
        if relative_y > 0 or relative_y < -self.height:
            return False

        r_dist = sqrt((hit_point.x - self.center.x)**2 + (hit_point.z - self.center.z)**2)
        raw_normal = Vector3(hit_point.x - self.center.x, r_dist * k, hit_point.z - self.center.z)
        hit_record.distance = root
        hit_record.point = hit_point
        refined_normal = raw_normal.unit_vector(raw_normal)         
        hit_record.set_face_normal(r, refined_normal)
        hit_record.material = self.material
        
        return True