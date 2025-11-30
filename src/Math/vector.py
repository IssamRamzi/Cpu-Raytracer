import math
import random

# Source : https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # addition vector + another
    def __add__(self, another):
        if isinstance(another, Vector3):
            return Vector3(self.x + another.x, self.y + another.y, self.z + another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x + another, self.y + another, self.z + another)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    # another + vector
    def __radd__(self, another):
        return self.__add__(another)
    
    # soustration
    def __sub__(self, another):
        if isinstance(another, Vector3):
            return Vector3(self.x - another.x, self.y - another.y, self.z - another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x - another, self.y - another, self.z - another)
        
    def __rsub__(self, another):
        if isinstance(another, Vector3):
            return Vector3(another.x - self.x, another.y - self.y, another.z - self.z)
        elif isinstance(another, (int, float)):
            return Vector3(another - self.x, another - self.y, another - self.z)
    
    # multiplication
    def __mul__(self, another):
        if isinstance(another, Vector3):
            return Vector3(self.x * another.x, self.y * another.y, self.z * another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x * another, self.y * another, self.z * another)
        
    def __rmul__(self, another):
        return self.__mul__(another)

    # division
    def __truediv__(self, another):
        if isinstance(another, Vector3):
            return Vector3(self.x / another.x, self.y / another.y, self.z / another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x / another, self.y / another, self.z / another)
        
    # négation
    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    # affichage
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __iadd__(self, another):
        if isinstance(another, Vector3):
            self.x += another.x
            self.y += another.y
            self.z += another.z
        elif isinstance(self, (int, float)):
            self.x += another
            self.y += another
            self.z += another
        return self

    # longueur
    def length(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def length_squared(self):
        return self.x*self.x + self.y*self.y + self.z*self.z
    
    # produit scalaire
    def dot(self, vector):
        return self.x * vector.x + self.y * vector.y + self.z * vector.z
    
    # produit
    def cross(self, vector):
        compx = self.y * vector.z - self.z * vector.y
        compy = self.z * vector.x - self.x * vector.z
        compz = self.x * vector.y - self.y * vector.x
        return Vector3(compx, compy, compz)
    
    def normalize(self):
        return self / self.length()
    
    @staticmethod
    def random_vec(min_val=0.0, max_val=0.0):
        if max_val == 0.0 and min_val == 0.0:
            return Vector3(random.random(), random.random(), random.random())
        else:
            return Vector3(random.uniform(min_val, max_val),
                           random.uniform(min_val, max_val),
                           random.uniform(min_val, max_val))

    @staticmethod
    def random_unit_vec():
        while True:
            p = Vector3.random_vec(-1, 1)
            len_squared = p.length_squared()
            if (1e-160 < len_squared and len_squared <= 1):
                return p / math.sqrt(len_squared)
       
    def near_zero(self):
        s = 1e-8
        return (abs(self.x) < s) and (abs(self.y) < s) and (abs(self.z) < s)


    # https://raytracing.github.io/images/fig-1.15-reflection.jpg
    @staticmethod
    def reflect(v, n):
        return v - 2 * v.dot(n) * n

    @staticmethod
    def unit_vector(v):
        return v / v.length()


def random_on_hemisphere(normal):
    on_unit_sphere = Vector3.random_unit_vec()
    if on_unit_sphere.dot(normal) > 0.0:
        return on_unit_sphere
    else:
        return -on_unit_sphere


    
Point3 = Color3 = Vector3
