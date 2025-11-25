from Math.vector import *
from .ray import Ray
from math import sqrt

"""
Source : https://raytracing.github.io/books/RayTracingInOneWeekend.html#addingasphere 
(Cx − x)^2+(Cy − y)^2+(Cz − z)^ = (C − P)⋅(C − P) = r2 = any point P that satisfies this equation is on the sphere
To check the intersection between the rays and the sphere we simply modify the equation : (C − P(t)) ⋅ (C − P(t) ) = r²
                                                                                          (C − (origin + t * direction)) ⋅ (C − (origin + t * direction)) = r2 
"""

def hit_sphere(center : Point3, radius : float, r : Ray) -> bool:
    oc = center - r.origin
    a = r.direction.dot(r.direction)
    b = -2 * r.direction.dot(oc)
    c = oc.dot(oc) - radius**2
    delta = b**2 - 4*a*c
    if delta < 0:
        return -1
    return (-b - sqrt(delta))/2*a
