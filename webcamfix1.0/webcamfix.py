import cv2
import pyvirtualcam
from pyvirtualcam import PixelFormat

# Read webcam
webcam = cv2.VideoCapture(0)

# Set width to 1280 and height to 720
webcam.set(3, 1280)
webcam.set(4, 720)

# Read mask
mask = cv2.imread('mask.jpg', cv2.IMREAD_GRAYSCALE)
if mask.all() == None:
    print('File couldn`t be opened')
    exit()

# Start virtual cam with 1280x720 30fps and colse camera after block
with pyvirtualcam.Camera(1280, 720, 30, fmt=PixelFormat.BGR) as cam:

    # Display what virtual camera sofware is being used
    print('Virtual camera device: ' + cam.device)

    if webcam.isOpened():
        sucess, frame = webcam.read()

        while sucess:
            sucess, frame = webcam.read()

            # Inpainting frame where mask limits using TELEA technique
            frame = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)

            # Displaying video and closing the window if ESC is pressed
            key = cv2.waitKey(4)
            if key == 27: # ESC
                break

            # Send frame to virtual cam and sleep until next frame
            cam.send(frame)
            cam.sleep_until_next_frame()