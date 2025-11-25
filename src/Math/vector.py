import math

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
    
     # produit
    def normalize(self):
        return self / self.length()
    
Point3 = Color3 = Vector3
