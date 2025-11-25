from .intervals import *

def write_color(output_stream, pixel_color):
    r = pixel_color.x
    g = pixel_color.y
    b = pixel_color.z
    intensity = Interval(0.000, 0.999)
    ir = int(256 * intensity.clamp(r))
    ig = int(256 * intensity.clamp(g))
    ib = int(256 * intensity.clamp(b))
    output_stream.write(f"{ir} {ig} {ib} ")

