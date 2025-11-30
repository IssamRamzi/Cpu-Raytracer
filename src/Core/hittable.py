from .ray import Ray, Vector3
from Math.vector import *
from Utils.intervals import Interval
from .material import Material

class HitRecord:
    def __init__(self):
        self.point = None
        self.normal = None
        self.distance = 0.0
        self.front_face = False
        self.material : Material = None
        self._u = None
        self._v = None

    def set_face_normal(self, r : Ray, outward_normal : Vector3):
        self.front_face = r.direction.dot(outward_normal) < 0 
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable:
    def __init__(self):
        pass

    def hit(self, r : Ray, interval : Interval, hit_record : HitRecord) -> bool:
        pass


class HittableList(Hittable):
    def __init__(self, objects = None):
        super().__init__()
        self.objects : list[Hittable] = []
        if objects:
            self.objects = objects
    
    def clear(self):
        self.objects.clear()

    def add(self, object : Hittable):
        self.objects.append(object)
    
    def hit(self, r, interval, hit_record):
        temp_rec : HitRecord = HitRecord()
        hit_anything = False
        closest_so_far = interval.max_val
        for obj in self.objects:
            if obj.hit(r, Interval(interval.min_val, closest_so_far), temp_rec):
                hit_anything = True

                closest_so_far = temp_rec.distance

                hit_record.point = temp_rec.point
                hit_record.normal = temp_rec.normal
                hit_record.distance = temp_rec.distance
                hit_record.front_face = temp_rec.front_face
                hit_record.material = temp_rec.material
                
        return hit_anything

