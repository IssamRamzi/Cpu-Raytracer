import math

class Interval:
    def __init__(self, min_val=math.inf, max_val=-math.inf) -> None:
        self.min_val = min_val
        self.max_val = max_val

    def size(self):
        return self.max_val - self.min_val

    def contains(self, val):
        return self.min_val <= val <= self.max_val

    def surrounds(self, val):
        return self.min_val < val < self.max_val

    def clamp(self, val):
        if val < self.min_val:
            return self.min_val
        if val > self.max_val:
            return self.max_val
        return val


Interval.empty = Interval(math.inf, -math.inf)
Interval.universe = Interval(-math.inf, math.inf)
