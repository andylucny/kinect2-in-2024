from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import cv2
import numpy as np

# Kinect runtime object, we want only color and body frames 
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Depth)
width, height = kinect.depth_frame_desc.Width, kinect.depth_frame_desc.Height

# -------- Main Program Loop -----------
image = np.zeros((height,width,3),np.uint8)
while True:

    # --- Getting frames and drawing  
    # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
    if kinect.has_new_depth_frame():
        frame = kinect.get_last_depth_frame()
        depth = frame.reshape((height,width))
        image = cv2.normalize(depth, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)

    cv2.imshow('body',image)
    if cv2.waitKey(10) == 27:
        break
    
# Close our Kinect sensor, close the window and quit.
kinect.close()
cv2.destroyAllWindows()
