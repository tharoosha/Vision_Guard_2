import cv2
import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
import numpy as np


# Open the video file
video_path = 'your_video.mp4'
cap = cv2.VideoCapture(video_path)

# Initialize a list to store frame embeddings
frame_embeddings = []

# Randomly sample 64 frames from the video
frame_indices = np.sort(np.random.choice(range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))), 64, replace=False))

# Define a transformation for frame preprocessing
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((512,512)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

with torch.no_grad():
    for idx in frame_indices:
        cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
        ret, frame = cap.read()
        if not ret:
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        frame = transform(frame)  # Preprocess the frame
        frame = frame.unsqueeze(0)  # Add batch dimension
        frame_embeddings.append(frame)

# Combine the embeddings (e.g., average or concatenate)
video_embedding = torch.cat(frame_embeddings, dim=0).mean(dim=0)


