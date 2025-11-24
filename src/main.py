from Math import Vector3
from Display import PPMWriter

import random


width, height = 128, 128
image = [
    [Vector3(random.randint(0,255), random.randint(0,255), random.randint(0,255))
     for _ in range(width)]
    for _ in range(height)
]

with open("output.ppm", "w") as f:
    writer = PPMWriter(width, height, f)
    writer.write_image(image)