import cv2
import numpy as np
import tensorflow as tf

# Load the MoveNet Lightning model
model_path = './Models/lite-model_movenet_singlepose_lightning_3.tflite'
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set up the camera
cap = cv2.VideoCapture(0)
while True:
    # Read a frame from the camera
    ret, frame = cap.read()
    if not ret:
        break
    
    # Preprocess the input frame
    resized_frame = cv2.resize(frame, (256, 256))
    input_data = np.expand_dims(resized_frame, axis=0)
    input_data = (input_data - 127.5) / 127.5  # Normalize the input
    
    # Run inference on the input
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    
    # Postprocess the output
    keypoints = output_data.squeeze()
    keypoints[:, 0] *= frame.shape[1] / 256
    keypoints[:, 1] *= frame.shape[0] / 256
    
    # Draw the keypoints on the frame
    for keypoint in keypoints:
        x, y = int(keypoint[0]), int(keypoint[1])
        cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
    
    # Display the resulting frame
    cv2.imshow('MoveNet Lightning', frame)
    if cv2.waitKey(1) == ord('q'):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()
