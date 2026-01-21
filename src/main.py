from Camera.camera import *
from Primitives.primitives import *
from Core.material import *
import sys
from Utils.config_loader import ConfigLoader
from Core.object_factory import MaterialFactory, PrimitiveFactory

import time

SAMPLES_PER_PIXEL = 500
CAMERA_WIDTH = 600

def process(config, output):
    config_loader = ConfigLoader(config)
    camera_cfg = config_loader.get_camera()

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

    camera = Camera(camera_cfg["width"],
                    (16.0 / 9.0),
                    samples_per_pixel=camera_cfg["samples_per_pixel"], # you guys can change this variable for sampling rate, 5 is already high in python
                    max_ray_bounces=camera_cfg['max_ray_bounces'], 
                    vfov=camera_cfg['fov'],
                    vup=Vector3(camera_cfg['up'][0], camera_cfg['up'][1], camera_cfg['up'][2]),
                    lookfrom=Point3(camera_cfg['lookfrom'][0], camera_cfg['lookfrom'][1], camera_cfg['lookfrom'][2]),
                    lookat=Point3(camera_cfg['lookat'][0], camera_cfg['lookat'][1], camera_cfg['lookat'][2]),
                    background=Color3(camera_cfg['background'][0], camera_cfg['background'][1], camera_cfg['background'][2])) 
    camera.render(world, output = output)

if __name__ == "__main__": # for args we'll have : args[1] = config_file_path, and args[2] = output_path.ppm
    args = sys.argv
    assert len(args) == 3, "Not enough arguments : [CONFIG_PATH] [OUTPUT_PATH]" 
    config_file, output = args[1], args[2]
    start = time.time()
    process(config_file, output)
    print(f"Took {time.time() - start}s")
