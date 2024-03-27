from pykinect2 import PyKinectV2
#from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime

import cv2
import numpy as np

# Kinect runtime object, we want only color and body frames 
kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Color | PyKinectV2.FrameSourceTypes_Body)
width, height = kinect.color_frame_desc.Width, kinect.color_frame_desc.Height

def draw_body_bone(image, joints, jointPoints, color, joint0, joint1):
    joint0State = joints[joint0].TrackingState
    joint1State = joints[joint1].TrackingState

    # both joints are not tracked
    if (joint0State == PyKinectV2.TrackingState_NotTracked) or (joint1State == PyKinectV2.TrackingState_NotTracked): 
        return

    # both joints are not *really* tracked
    if (joint0State == PyKinectV2.TrackingState_Inferred) and (joint1State == PyKinectV2.TrackingState_Inferred):
        return

    # ok, at least one is good 
    try:
        start = (int(jointPoints[joint0].x), int(jointPoints[joint0].y))
        end = (int(jointPoints[joint1].x), int(jointPoints[joint1].y))
        cv2.line(image, start, end, color, 8)
    except: # need to catch it due to possible invalid positions (with inf)
        pass

def draw_body(image, joints, jointPoints, color):
    # Torso
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_Head, PyKinectV2.JointType_Neck);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_Neck, PyKinectV2.JointType_SpineShoulder);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_SpineMid);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineMid, PyKinectV2.JointType_SpineBase);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineShoulder, PyKinectV2.JointType_ShoulderLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_SpineBase, PyKinectV2.JointType_HipLeft);

    # Right Arm    
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_ShoulderRight, PyKinectV2.JointType_ElbowRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_ElbowRight, PyKinectV2.JointType_WristRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_HandRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_HandRight, PyKinectV2.JointType_HandTipRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_WristRight, PyKinectV2.JointType_ThumbRight);

    # Left Arm
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_ShoulderLeft, PyKinectV2.JointType_ElbowLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_ElbowLeft, PyKinectV2.JointType_WristLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_HandLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_HandLeft, PyKinectV2.JointType_HandTipLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_WristLeft, PyKinectV2.JointType_ThumbLeft);

    # Right Leg
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_HipRight, PyKinectV2.JointType_KneeRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_KneeRight, PyKinectV2.JointType_AnkleRight);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_AnkleRight, PyKinectV2.JointType_FootRight);

    # Left Leg
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_HipLeft, PyKinectV2.JointType_KneeLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_KneeLeft, PyKinectV2.JointType_AnkleLeft);
    draw_body_bone(image, joints, jointPoints, color, PyKinectV2.JointType_AnkleLeft, PyKinectV2.JointType_FootLeft);

# -------- Main Program Loop -----------
image = np.zeros((height,width,3),np.uint8)
frame = None
while True:

    # --- Getting frames and drawing  
    # --- Woohoo! We've got a color frame! Let's fill out back buffer surface with frame's data 
    if kinect.has_new_color_frame():
        frame = kinect.get_last_color_frame()

    # --- Cool! We have a body frame, so can get skeletons
    if kinect.has_new_body_frame(): 
        bodies = kinect.get_last_body_frame()
        # --- draw skeletons to _frame_surface
        if bodies is not None: 
            if frame is not None:
                image = np.array(frame.reshape((height,width,-1))[:,:,:3],np.uint8)
            else:
                image = np.zeros((height,width,3),np.uint8)
            for i in range(0, kinect.max_body_count):
                body = bodies.bodies[i]
                if not body.is_tracked: 
                    continue 
                joints = body.joints 
                # convert joint coordinates to color space 
                joint_points = kinect.body_joints_to_color_space(joints)
                draw_body(image, joints, joint_points, (0,0,255))

    cv2.imshow('body',cv2.resize(image,(image.shape[1]//2,image.shape[0]//2)))
    if cv2.waitKey(10) == 27:
        break
    
# Close our Kinect sensor, close the window and quit.
kinect.close()
cv2.destroyAllWindows()
