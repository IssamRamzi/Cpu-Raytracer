from Camera.camera import *
from Primitives.primitives import *
from Core.material import *
import sys
from Utils.config_loader import ConfigLoader
from Core.object_factory import MaterialFactory, PrimitiveFactory

import time

SAMPLES_PER_PIXEL = 10
CAMERA_WIDTH = 400

def process(config, output):
    config_loader = ConfigLoader(config)
    camera = config_loader.get_camera()

    materials_config = config_loader.get_materials()
    primitives_config = config_loader.get_primitives()
    material_map = {}
    for mat_data in materials_config:
        mat_id = mat_data["id"]
        material = MaterialFactory.create(mat_data)
        material_map[mat_id] = material

    world = HittableList()
    for prim_data in primitives_config:
        mat_id = prim_data["material"]
        if mat_id not in material_map:
            raise ValueError(f"Material '{mat_id}' not found for primitive {prim_data}")
        material = material_map[mat_id]
        primitive = PrimitiveFactory.create(prim_data, material)
        if primitive is None:
            raise ValueError(f"Primitive creation failed for {prim_data}")
        world.add(primitive)


    camera = Camera(camera["width"], (16.0 / 9.0), samples_per_pixel=camera["samples_per_pixel"], max_ray_bounces=50) # you guys can change the last variable for sampling rate, 5 is already high in python
    camera.render(world, output = output)

if __name__ == "__main__": # for args we'll have : args[1] = config_file_path, and args[2] = output_path.ppm
    args = sys.argv
    assert len(args) == 3, "Not enough arguments : [CONFIG_PATH] [OUTPUT_PATH]" 
    config_file, output = args[1], args[2]
    start = time.time()
    process(config_file, output)
    print(f"Took {time.time() - start}s")