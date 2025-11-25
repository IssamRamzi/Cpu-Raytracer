from Math.vector import *
from .ray import Ray
from math import sqrt


#deprecated




def hit_sphere(center : Point3, radius : float, r : Ray) -> bool:
    oc = center - r.origin
    a = r.direction.dot(r.direction)
    b = -2 * r.direction.dot(oc)
    c = oc.dot(oc) - radius**2
    delta = b**2 - 4*a*c
    if delta < 0:
        return -1
    return (-b - sqrt(delta))/2*a
