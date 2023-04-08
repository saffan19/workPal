import cv2
import mediapipe as mp
import numpy as np
import winsound
import sys

##############################



mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

# For static images:
IMAGE_FILES = []
# IMAGE_FILES=[]
BG_COLOR = (192, 192, 192) # gray



with mp_pose.Pose(
    static_image_mode=True,
    model_complexity=2,
    enable_segmentation=True,
    min_detection_confidence=0.5) as pose:
  for idx, file in enumerate(IMAGE_FILES):
    image = cv2.imread(file)
    image_height, image_width, _ = image.shape
    # Convert the BGR image to RGB before processing.
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    if not results.pose_landmarks:
      continue
    # print(
    #     f'Nose coordinates: ('
    #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x * image_width}, '
    #     f'{results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y * image_height})'
    # )

   
    # Draw segmentation on the image.
    # To improve segmentation around boundaries, consider applying a joint
    # bilateral filter to "results.segmentation_mask" with "image".
    #print(results.pose_landmarks)

######################################################


    #print(results.pose_landmarks.landmark[8].x)
    
    #calculating angle b/w right ear right shoulder and right hip

    #right ear
    x1=results.pose_landmarks.landmark[8].x
    y1=results.pose_landmarks.landmark[8].y

    #right shoulder
    x2=results.pose_landmarks.landmark[12].x
    y2=results.pose_landmarks.landmark[12].y    

    #right hib
    x3=results.pose_landmarks.landmark[24].x
    y3=results.pose_landmarks.landmark[24].y
    
    m1=(y2-y1)/(x2-x1)
   # m2=(y2-y3)/(x3-x2)

   # m=m1+m2

    print(results.pose_landmarks.landmark[8].z)
    print(results.pose_landmarks.landmark[7].z)


######################################################

    # Draw pose landmarks on the image.
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    cv2.imwrite('/tmp/annotated_image' + str(idx) + '.png', image)

###################################################
# THIS CONDITION IS TO CHECK IF THE VIEW POSE IS ENABLED
    if len(sys.argv)>1:
      cv2.imshow('MediaPipe Pose', image)
      # Plot pose world landmarks.
      mp_drawing.plot_landmarks(
        results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)
####################################################
    


goodPos=0
badPos=0


# For webcam input:
cap = cv2.VideoCapture(0)
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.

    if len(sys.argv)>1:
      cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    
    ############################
    #right ear
    x1=results.pose_landmarks.landmark[8].x
    y1=results.pose_landmarks.landmark[8].y

    #right shoulder
    x2=results.pose_landmarks.landmark[12].x
    y2=results.pose_landmarks.landmark[12].y    

    #right hib
    x3=results.pose_landmarks.landmark[24].x
    y3=results.pose_landmarks.landmark[24].y
    
    m1=abs((y2-y1)/(x2-x1))

#left:
    xx1=results.pose_landmarks.landmark[7].x
    yy1=results.pose_landmarks.landmark[7].y


    xx2=results.pose_landmarks.landmark[11].x
    yy2=results.pose_landmarks.landmark[11].y    


    xx3=results.pose_landmarks.landmark[23].x
    yy3=results.pose_landmarks.landmark[23].y
    
    m2=abs((yy2-yy1)/(xx2-xx1))    
   # m2=(y2-y3)/(x3-x2)

  #  m=m1+m2


    if(m1<=1.9 or m2<=1.9 or m1>=3.2 or m2>=3.2):
      # frequency=2000
      # duration=125
      # winsound.Beep(frequency, duration)
      badPos=badPos+1
      goodPos=0
      if badPos>=10:
        frequency=2000
        duration=125
        winsound.Beep(frequency, duration)        
    else:
      goodPos=goodPos+1
      if goodPos>=10:
        badPos=0


    #############################


    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()