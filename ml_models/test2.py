# import torch
# from torch.distributions import Bernoulli

# # Define the probability matrix for the Bernoulli distribution
# # In this example, we have a 3x9 matrix with probabilities (0.8, 0.4, 0.4) for each row.
# # Adjust the probabilities as needed.
# probabilities = torch.tensor([[0.8, 0.4, 0.4],
#                              [0.7, 0.3, 0.6],
#                              [0.5, 0.2, 0.7]])

# # Create a Bernoulli distribution
# bernoulli_distribution = Bernoulli(probs=probabilities)

# # Sample from the Bernoulli distribution to generate binary masks
# sample = bernoulli_distribution.sample()

# # Display the sample
# print("Sampled Binary Mask:")
# print(sample)

# # Create a binary mask based on the sample
# mask = (sample > 0).unsqueeze(1).repeat(1, sample.size(1), 1).unsqueeze(1)

# # Display the resulting binary mask
# print("\nBinary Mask (3D tensor):")
# print(mask)

import cv2

def calculate_fps(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print("Error: Couldn't open the video file.")
        return

    # Get the frames per second
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Release the video capture object
    cap.release()

    return fps

if __name__ == "__main__":
    video_path = "ml_models/dataset/ARID_v1.5/clips_v1.5/Jump/Jump_1_1.mp4"  # Replace with the path to your video file
    fps = calculate_fps(video_path)

    if fps is not None:
        print(f"Frames per second (FPS): {fps}")

