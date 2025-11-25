from .hittable import Hittable, HitRecord
from Math.vector import *
from .ray import Ray

class Plane(Hittable):
    def __init__(self, bot_left : Point3, u : Vector3, v : Vector3):
        super().__init__()
        self.u = u
        self.v = v
        normal = u.cross(v)
        self.normal = normal.normalize()
        self.bot_left = bot_left
        self._d = self.normal.dot(self.bot_left)
        self._w = normal / normal.dot(normal)

    def hit(self, r : Ray,ray_tmin, ray_tmax, hit_record : HitRecord):
        denom = self.normal.dot(r.direction)

        if(abs(denom) < 1e-8): # epsilon
            return False
        
        t = (self._d - self.normal.dot(r.origin)) / denom

        intersection = r.at(t)

        planarHitptVector = intersection - self.bot_left
        alpha = self._w.dot(planarHitptVector.cross(self.v))
        beta = self._w.dot(planarHitptVector.cross(self.u))
        
        hit_record.distance = t
        hit_record.point = intersection
        hit_record.set_face_normal(r, self.normal)

        return True