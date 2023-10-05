import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Pixel brightness adjust depending on threshold values")
parser.add_argument('video', type=str, help="path to the video file")
args = parser.parse_args()

def adjust_pixel_brightness(frame, brightness_threshold, reduction_factor=0.5):
    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Identify pixels in the Value channel that are above the threshold
    high_brightness_pixels = hsv[:,:,2] > brightness_threshold
    
    # Reduce the brightness of those pixels by the reduction factor
    hsv[high_brightness_pixels, 2] = hsv[high_brightness_pixels, 2] * reduction_factor
    
    # Convert the frame back to BGR
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Open the video file
cap = cv2.VideoCapture(args.video)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_pixel_brightness_adjusted.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

# Set your brightness threshold for individual pixels
pixel_brightness_threshold = 40  # Adjust this value based on your needs

while True:
    ret, frame = cap.read()
    
    # Break the loop if video has ended
    if not ret:
        break
    
    # Adjust brightness of the specific pixels in the frame
    adjusted_frame = adjust_pixel_brightness(frame, pixel_brightness_threshold)
    
    # Write the adjusted frame
    out.write(adjusted_frame)

    # Display the frame (optional)
    # cv2.imshow('Video Playback', adjusted_frame)
    # if cv2.waitKey(25) & 0xFF == ord('q'):
    #     break

# Release the video objects and close all OpenCV windows
cap.release()
out.release()
cv2.destroyAllWindows()
