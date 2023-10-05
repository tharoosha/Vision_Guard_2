# import os
# import csv

# # Root directory
# root_dir = 'ARID_v1.5/clips_v1.5_avi'

# # CSV output file
# output_file = 'dataset.csv'

# # Find the class directories inside the root directory
# class_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

# # Create or overwrite the CSV file
# with open(output_file, 'w', newline='') as csvfile:
#     fieldnames = ['VideoID', 'Video', 'ClassID']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()  # Writes the header
    
#     for class_id, class_dir in enumerate(class_dirs):
#         video_files = [f for f in os.listdir(os.path.join(root_dir, class_dir)) if os.path.isfile(os.path.join(root_dir, class_dir, f))]
        
#         for video_file in video_files:
#             video_id = video_file.split('.')[0]  # Removing file extension
#             writer.writerow({'VideoID': video_id, 'Video': os.path.join(class_dir, video_file), 'ClassID': class_id})

# print(f"CSV file created at {output_file}")
