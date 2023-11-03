import cv2

# # Load the video
# video_path = 'ml_models/dataset/ARID_v1.5/clips_v1.5/Stand/Stand_1_1.mp4'
# cap = cv2.VideoCapture(video_path)

# # Get video properties
# frame_width = int(cap.get(3))  # Width of the frames
# frame_height = int(cap.get(4))  # Height of the frames
# fps = int(cap.get(5))           # Frames per second

# # Close the video capture
# cap.release()

# print(f"Video dimensions: {frame_width}x{frame_height}")
# print(f"Frames per second (fps): {fps}")

from PIL import Image
import numpy as np
from vidoe_transforms import video_transforms


# Open an image
img = Image.open('ml_models/data/ARID_frames/Walk/Walk_1_1/img_00020.jpg')

# # Get image dimensions
# width, height = img.size

# print(f"Image dimensions: {width}x{height}")
cv_read_flag = cv2.IMREAD_COLOR

image_paths = [
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00008.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00009.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00010.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00011.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00012.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00013.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00014.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00015.jpg',
    # 'ml_models/data/ARID_frames/Walk/Walk_5_26/img_00016.jpg',

    "ml_models/data/settings/new_image/output_output_img_00008.jpg",
    "ml_models/data/settings/new_image/output_img_00009.jpg",
    "ml_models/data/settings/new_image/output_img_00010.jpg",
    "ml_models/data/settings/new_image/output_img_00011.jpg",
    "ml_models/data/settings/new_image/output_img_00012.jpg",
    "ml_models/data/settings/new_image/output_img_00013.jpg",
    "ml_models/data/settings/new_image/output_img_00014.jpg",
    "ml_models/data/settings/new_image/output_img_00015.jpg",
    "ml_models/data/settings/new_image/output_img_00016.jpg",

]


def gamma_intensity_correction(img, gamma):

    invGamma = 1.0/gamma
    LU_table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0,256)]).astype("uint8")
    gamma_img = cv2.LUT(img, LU_table)

    return gamma_img

# for image_path in image_paths:

#     cv_img_origin = cv2.imread(image_path, cv_read_flag)

#     # use interpolation for resize the image
#     # interpolation = cv2.INTER_LINEAR
#     gamma = 1.8
#     # cv_img_origin = gamma_intensity_correction(cv_img_origin,gamma)
#     # cv_img = cv2.resize(cv_img_origin, (170, 128), interpolation)
#     cv_img = cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB)

#     # Or, you can save it to a file
#     output_path = 'output_' + image_path.split('/')[-1]  # Output file path
#     cv2.imwrite(output_path, cv_img_origin)


    # Load an image (replace 'your_image_path.jpg' with the actual image path)
img = cv2.imread('output_multiscale_crop_light_00010.png', cv2.IMREAD_COLOR)
img_light = cv2.imread('ml_models/data/ARID_frames/Walk/Walk_5_26/img_00008.jpg', cv2.IMREAD_COLOR)

# Parameters for multi-scale cropping
size = (224, 224)
scale_ratios = [1.0, 0.875, 0.75, 0.66]
fix_crop = True
more_fix_crop = True
max_distort = 1

num_seg = 1
length = 64

clip_mean = [0.485, 0.456, 0.406] 
clip_std = [0.229, 0.224, 0.225] 

tensor = video_transforms.ToTensor()
normalize = video_transforms.Normalize(mean=clip_mean,std=clip_std)

# Perform multi-scale cropping
clip, clip_light = tensor(img, img_light)
print(clip_light.size())
cropped_img_light = normalize(clip_light)
# # print(cropped_img)
# data = Image.fromarray(cropped_img.astype(np.uint8)) 
normalized_array_light = (cropped_img_light * 255).byte().permute(1, 2, 0).cpu().numpy()

# Create a PIL image from the NumPy array
data_light = Image.fromarray(normalized_array_light)

# Save the image
data_light.save("output_normalization_light_000188.png")
