import cv2
from collections import Counter
import shutil
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

arra=[]

#loading Models
meso4_model = load_model('./model/meso4_model.h5')

def check_image(img_path, target_size=(256, 256)):
    img = Image.open(img_path)
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to the range [0, 1]

#     plt.imshow(img)
#     plt.title('Input Image')
#     plt.show()
    
    prediction = meso4_model.predict(img_array)

    threshold = 0.5
    predicted_class = 1 if prediction > threshold else 0

    if predicted_class == 1:
        return "Real"
    else:
        return "DeepFake"


def check(video_path):


    output_folder = 'framemanage'
    os.makedirs(output_folder, exist_ok=True)


    cap = cv2.VideoCapture(video_path)

# Check if the video opened successfully
    if not cap.isOpened():
        print("Error opening video file.")
        exit()

# Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Read and save all frames
    for frame_number in range(total_frames):
    # Set the video capture object to the current frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

    # Read the frame from the current frame number
        ret, frame = cap.read()

    # Check if the frame was read successfully
        if not ret:
            print(f"Error reading frame {frame_number}.")
            break

    # Save the frame with a specific name
        output_filename = os.path.join(output_folder, f"frame_{frame_number}.jpg")
        cv2.imwrite(output_filename, frame)

# Release the video capture object
    cap.release()

def video_with_feature(video_path):
    check(video_path)
    for i in range (70,110,3):
        arra.append(check_image(f"framemanage/frame_{i}.jpg"))#original
    label_counts = Counter(arra)
    most_common_label = label_counts.most_common(1)[0][0]
    shutil.rmtree(r'./framemanage')
    return most_common_label