import cv2
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="Gamma correction on video footages")
parser.add_argument('video', type=str, help="path to the video file")
args = parser.parse_args()

def adjust_gamma(image, gamma=1.0):
    # build a lookup table mapping the pixel values [0, 255] to
    # their adjusted gamma values
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
                      for i in np.arange(0, 256)]).astype("uint8")
    
    # apply gamma correction using the lookup table
    return cv2.LUT(image, table)

# Load the video
cap = cv2.VideoCapture(args.video)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output_gamma_corrected.avi', fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

gamma_value = 0.2  # Adjust this value according to your needs. <1 will brighten the video; >1 will darken it.

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        # Apply gamma correction
        gamma_corrected = adjust_gamma(frame, gamma=gamma_value)
        
        # Write the gamma-corrected frame
        out.write(gamma_corrected)

        # Uncomment these lines if you want to see the video playback during processing
        # cv2.imshow('frame', gamma_corrected)
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break
    else:
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()
