import os
import shutil

def save_frames(video_name: str, input_path: str, output_path: str):
    # Construct the path to the video's frames
    video_path = os.path.join(input_path, video_name)
    
    # Get the list of frame files
    frames = sorted(os.listdir(video_path))
    
    # Calculate the total number of frames
    total_frames = len(frames)
    
    # Calculate the sequence number
    sequence_no = total_frames // 30
    
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Iterate through the frames and save specific frames
    for i in range(0, total_frames, sequence_no):
        frame_file = frames[i]
        input_frame_path = os.path.join(video_path, frame_file)
        output_frame_path = os.path.join(output_path, f"{video_name}_frame_{i}.jpg")
        shutil.copy(input_frame_path, output_frame_path)
        print(f"Saved: {output_frame_path}")

# Example usage
input_path = 'ml_models/data/ARID_frames'
output_path = 'output_frames'
video_name = 'example_video'
save_frames(video_name, input_path, output_path)
