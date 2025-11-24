import math

# Source : https://raytracing.github.io/books/RayTracingInOneWeekend.html#thevec3class

class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    # addition vector + another
    def __add__(self, another) -> Vector3:
        if isinstance(another, Vector3):
            return Vector3(self.x + another.x, self.y + another.y, self.z + another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x + another, self.y + another, self.z + another)

    # another + vector
    def __radd__(self, another):
        return self.__add__(another)
    
    # soustration
    def __sub__(self, another) -> Vector3:
        if isinstance(another, Vector3):
            return Vector3(self.x - another.x, self.y - another.y, self.z - another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x - another, self.y - another, self.z - another)
        
    def __rsub__(self, another):
        return self.__add__(another)
    
    # multiplication (dot)
    def __mul__(self, another) -> Vector3:
        if isinstance(another, Vector3):
            return Vector3(self.x * another.x, self.y * another.y, self.z * another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x * another, self.y * another, self.z * another)
        
    def __rmul__(self, another):
        return self.__add__(another)

    # division
    def __truediv__(self, another) -> Vector3:
        if isinstance(another, Vector3):
            return Vector3(self.x / another.x, self.y / another.y, self.z / another.z)
        elif isinstance(another, (int, float)):
            return Vector3(self.x / another, self.y / another, self.z / another)

    # affichage
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    # longueur
    def length(self, vector : Vector3 = None):
        if vector:
            return math.sqrt(Vector3(vector.x**2, vector.y**2, vector.z**2))
        else:
            return math.sqrt(Vector3(self.x**2, self.y**2, self.z**2))

    def length_squared(self, vector : Vector3 = None):
        return self.length(vector)**2
    
    # produit scalaire
    def dot(self, vector : Vector3):
        return self * vector
    
    # produit
    def cross(self, vector : Vector3):
        compx = self.y * vector.z - self.z * vector.y
        compy = self.z * vector.x - self.x * vector.z
        compz = self.x * vector.y - self.y * vector.x
        return Vector3(compx, compy, compz)
    
     # produit
    def normalize(self):
        return self / self.length()
    
