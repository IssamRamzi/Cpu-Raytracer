from Camera.camera import Camera

def main():
    
    camera = Camera(400, (16.0 / 9.0), 5, 50) #you guys can change the last variable for sampling rate, 5 is already high in python
    camera.render()

if __name__ == "__main__":
    main()

