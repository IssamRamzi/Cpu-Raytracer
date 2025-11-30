from Core.hittable import *
from abc import abstractmethod

class Material:
    @abstractmethod
    def scatter(self, ray, hit_record, color_attenuation, scattered):
        pass

