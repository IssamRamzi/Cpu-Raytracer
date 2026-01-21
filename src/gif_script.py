import json
import os
import sys
import time
import math

# Imports de votre structure existante
from Camera.camera import *
from Primitives.primitives import *
from Core.material import *
from Utils.config_loader import ConfigLoader
from Core.object_factory import MaterialFactory, PrimitiveFactory
from Core.hittable import HittableList

def process(config, output):
    """Fonction process() existante - identique à votre code"""
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
                    samples_per_pixel=camera_cfg["samples_per_pixel"],
                    max_ray_bounces=camera_cfg['max_ray_bounces'], 
                    vfov=camera_cfg['fov'],
                    vup=Vector3(camera_cfg['up'][0], camera_cfg['up'][1], camera_cfg['up'][2]),
                    lookfrom=Point3(camera_cfg['lookfrom'][0], camera_cfg['lookfrom'][1], camera_cfg['lookfrom'][2]),
                    lookat=Point3(camera_cfg['lookat'][0], camera_cfg['lookat'][1], camera_cfg['lookat'][2]),
                    background=Color3(camera_cfg['background'][0], camera_cfg['background'][1], camera_cfg['background'][2])) 
    
    camera.render(world, output=output)

def create_frame_config(frame_num, total_frames, duration=2.0):
    """
    Crée une configuration pour un frame donné.
    La balle suit une trajectoire parabolique (rebond).
    """
    # Calcul du temps pour ce frame
    t = (frame_num / total_frames) * duration
    
    # Animation de la balle (mouvement vertical avec rebonds)
    bounce_height = 3.0
    ball_y = abs(math.sin(t * math.pi * 2)) * bounce_height + 0.6
    
    # Rotation des lumières
    light_angle = t * math.pi
    light_radius = 3.0
    light1_x = math.cos(light_angle) * light_radius
    light1_z = math.sin(light_angle) * light_radius
    light2_x = math.cos(light_angle + math.pi) * light_radius
    light2_z = math.sin(light_angle + math.pi) * light_radius
    
    config = {
        "camera": {
            "width": 400,
            "samples_per_pixel": 1000,
            "max_ray_bounces": 20,
            "fov": 50,
            "up": [0, 1, 0],
            "lookfrom": [5, 3, 8],
            "lookat": [0, 1.5, 0],
            "background": [0.05, 0.05, 0.15]
        },
        "materials": [
            {
                "id": "Floor",
                "type": "Lambertian",
                "color": [0.3, 0.3, 0.35]
            },
            {
                "id": "BouncingBall",
                "type": "Lambertian",
                "color": [0.9, 0.3, 0.3]
            },
            {
                "id": "BackgroundSphere1",
                "type": "Lambertian",
                "color": [0.2, 0.5, 0.8]
            },
            {
                "id": "BackgroundSphere2",
                "type": "Lambertian",
                "color": [0.8, 0.5, 0.2]
            },
            {
                "id": "BackgroundCube",
                "type": "Lambertian",
                "color": [0.4, 0.8, 0.4]
            },
            {
                "id": "Light1",
                "type": "DiffuseLight",
                "color": [6, 6, 8]
            },
            {
                "id": "Light2",
                "type": "DiffuseLight",
                "color": [8, 6, 4]
            }
        ],
        "primitives": [
            {
                "type": "Plane",
                "bot_left": [-15, 0, -15],
                "x_vector": [30, 0, 0],
                "y_vector": [0, 0, 30],
                "material": "Floor"
            },
            {
                "type": "Sphere",
                "center": [0, ball_y, 0],
                "radius": 0.6,
                "material": "BouncingBall"
            },
            {
                "type": "Sphere",
                "center": [-3, 1.0, -2],
                "radius": 0.8,
                "material": "BackgroundSphere1"
            },
            {
                "type": "Sphere",
                "center": [3, 0.7, -2],
                "radius": 0.7,
                "material": "BackgroundSphere2"
            },
            {
                "type": "Cube",
                "material": "BackgroundCube",
                "min_corner": [-1.5, 0, -4],
                "max_corner": [-0.5, 1.2, -3]
            },
            {
                "type": "Sphere",
                "center": [light1_x, 5.0, light1_z],
                "radius": 0.8,
                "material": "Light1"
            },
            {
                "type": "Sphere",
                "center": [light2_x, 4.5, light2_z],
                "radius": 0.7,
                "material": "Light2"
            }
        ]
    }
    
    return config

def create_animation(output_dir="animation_frames", fps=30, duration=2.0):
    """
    Crée une animation complète en générant plusieurs images PPM.
    
    Args:
        output_dir: Dossier où sauvegarder les frames
        fps: Images par seconde
        duration: Durée de l'animation en secondes
    """
    # Créer le dossier de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    total_frames = int(fps * duration)
    print(f"Génération de {total_frames} frames à {fps} fps pour {duration}s...")
    
    # Générer chaque frame
    for i in range(total_frames):
        print(f"\n{'='*60}")
        print(f"Rendu du frame {i+1}/{total_frames} ({(i+1)/total_frames*100:.1f}%)")
        print(f"{'='*60}")
        
        start_time = time.time()
        
        # Créer la configuration pour ce frame
        config = create_frame_config(i, total_frames, duration)
        
        # Sauvegarder la config dans un fichier JSON temporaire
        config_file = os.path.join(output_dir, f"config_frame_{i:04d}.json")
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        # Nom du fichier de sortie PPM
        ppm_file = os.path.join(output_dir, f"frame_{i:04d}.ppm")
        
        # Rendre le frame en utilisant la fonction process existante
        process(config_file, ppm_file)
        
        # Supprimer le fichier config temporaire
        os.remove(config_file)
        
        elapsed = time.time() - start_time
        print(f"Frame terminé en {elapsed:.2f}s")
        print(f"Temps estimé restant: {elapsed * (total_frames - i - 1) / 60:.1f} minutes")
    
    print(f"\n{'='*60}")
    print(f"✓ Animation terminée!")
    print(f"  - {total_frames} frames générés dans '{output_dir}/'")
    print(f"  - Format: frame_0000.ppm à frame_{total_frames-1:04d}.ppm")
    print(f"\nPour créer un GIF, utilisez ImageMagick:")
    print(f"  convert -delay {int(100/fps)} -loop 0 {output_dir}/frame_*.ppm animation.gif")
    print(f"{'='*60}")

if __name__ == "__main__":
    start_total = time.time()
    
    # Paramètres de l'animation
    OUTPUT_DIR = "animation_frames"
    FPS = 30
    DURATION = 2.0
    
    print("\n" + "="*60)
    print("GÉNÉRATEUR D'ANIMATION - BALLE REBONDISSANTE")
    print("="*60)
    
    create_animation(OUTPUT_DIR, FPS, DURATION)
    
    total_time = time.time() - start_total
    print(f"\nTemps total: {total_time / 60:.1f} minutes ({total_time:.1f}s)\n")