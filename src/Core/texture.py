
class Texture:
    def __init__(self) -> None:
        pass

    def value(u, v, point):
        pass

class SolidColor(Texture):
    def __init__(self, albedo) -> None:
        self._albedo = albedo

    def value(self, u, v, point):
        return self._albedo
