import io
from Utils.colors import write_color


class PPMWriter:
    def __init__(self, width : int, height : int, output_stream : io.TextIOBase):
        self.width = width
        self.height = height
        self.output : io.TextIOBase = output_stream
        self._write_header()

    def _write_header(self):
        # P3
        self.output.write("P3\n")
        # width et height
        self.output.write(f"{self.width} {self.height}\n")
        # valeur rgb max
        self.output.write("255\n")

    def write_image(self, image):
        for row in image:
            # pixel : Vector3
            for pixel in row:
                write_color(self.output, pixel)
            self.output.write("\n")


        
