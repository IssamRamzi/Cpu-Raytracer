from Math.vector import Vector3, Color3, Point3

class Ray:
    def __init__(self, origin : Point3, direction : Vector3):
        self.origin = origin
        self.direction = direction

    # P(t) = origin + t*direction (IMPORTANT, EXAM ?)
    def at(self, t) -> Point3:
        return self.origin + t * self.direction
        