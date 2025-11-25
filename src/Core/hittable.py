from .ray import Ray, Vector3
from Math.vector import *

class HitRecord:
    point : Point3
    normal : Vector3
    distance : float
    front_face : bool


    def set_face_normal(self, r : Ray, outward_normal : Vector3):
        self.front_face = r.direction.dot(outward_normal) < 0 
        self.normal = outward_normal if self.front_face else -outward_normal


class Hittable:
    def __init__(self):
        pass

    def hit(self, r : Ray, ray_tmin : float, ray_tmax : float, hit_record : HitRecord) -> bool:
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
    
    def hit(self, r, ray_tmin, ray_tmax, hit_record):
        temp_rec : HitRecord = HitRecord()
        hit_anything = False
        closest_so_far = ray_tmax

        for obj in self.objects:
            if obj.hit(r, ray_tmin, closest_so_far, temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.distance

                hit_record.point = temp_rec.point
                hit_record.normal = temp_rec.normal
                hit_record.distance = temp_rec.distance
                hit_record.front_face = temp_rec.front_face
        
        return hit_anything

