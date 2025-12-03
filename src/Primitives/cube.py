from Core.hittable import Hittable, HitRecord
from Core.ray import Ray
from Math.vector import Vector3, Point3
from Utils.intervals import Interval
from Core.material import Material


class Cube(Hittable):
    def __init__(self, min_corner: Point3, max_corner: Point3, material: Material = None):
        super().__init__()
        self.min = min_corner
        self.max = max_corner
        self.material = material

        print("")

    def hit(self, r: Ray, interval: Interval, hit_record: HitRecord):

        t_min = interval.min_val
        t_max = interval.max_val

        for axis in ("x", "y", "z"):
            origin_axis = getattr(r.origin, axis)
            dir_axis = getattr(r.direction, axis)
            min_axis = getattr(self.min, axis)
            max_axis = getattr(self.max, axis)

            if abs(dir_axis) < 1e-8:
                if origin_axis < min_axis or origin_axis > max_axis:
                    return False
                continue

            invD = 1.0 / dir_axis
            t0 = (min_axis - origin_axis) * invD
            t1 = (max_axis - origin_axis) * invD

            if invD < 0:
                t0, t1 = t1, t0

            if t0 > t_min:
                t_min = t0
            if t1 < t_max:
                t_max = t1

            if t_max <= t_min:
                return False

        hit_record.distance = t_min
        hit_record.point = r.at(t_min)
        hit_record.set_face_normal(r, self._compute_normal(hit_record.point))
        hit_record.material = self.material

        return True

    def _compute_normal(self, p: Point3) -> Vector3:
        eps = 1e-4

        if abs(p.x - self.min.x) < eps:
            return Vector3(-1, 0, 0)
        if abs(p.x - self.max.x) < eps:
            return Vector3(1, 0, 0)
        if abs(p.y - self.min.y) < eps:
            return Vector3(0, -1, 0)
        if abs(p.y - self.max.y) < eps:
            return Vector3(0, 1, 0)
        if abs(p.z - self.min.z) < eps:
            return Vector3(0, 0, -1)
        if abs(p.z - self.max.z) < eps:
            return Vector3(0, 0, 1)

        return Vector3(0, 0, 0)
