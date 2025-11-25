from Camera.camera import Camera

def main():
    camera = Camera(400, (16.0 / 9.0), 5)
    camera.render()

if __name__ == "__main__":
    main()

