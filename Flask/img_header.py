#header files
import cv2
from collections import Counter
import shutil
import os
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from lime import lime_image
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image




#loading Models
meso4_model = load_model('./model/meso4_model.h5')
meso4_model.load_weights('./model/Meso4_DF')

#to check the image
def check_image(img_path, target_size=(256, 256)):
    img = Image.open(img_path)
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to the range [0, 1]
     #Display the original image
   
    prediction = meso4_model.predict(img_array)
    threshold = 0.5
    predicted_class = 1 if prediction > threshold else 0

    if predicted_class == 1:
        return 1
    else:
        return 0

explainer = lime_image.LimeImageExplainer()
def feature_extraction_image(img_path, target_size=(256, 256)):
    img = Image.open(img_path)
    img = img.resize(target_size)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array /= 255.0  # Normalize pixel values to the range [0, 1]

    

    # Predict the class using your deepfake detection model
    prediction = meso4_model.predict(img_array)

    # Interpret the prediction using LIME
    explanation = explainer.explain_instance(img_array[0], meso4_model.predict, top_labels=1, hide_color=0, num_samples=1000)

    
    temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=True)
    explanation_img = Image.fromarray((temp * 255).astype(np.uint8))

    explanation_filename = os.path.join('static', 'uploads', 'explanation_' + os.path.basename(img_path))
    explanation_img.save(explanation_filename)

    return explanation_filename

def img_with_feature(img_path):
    if(check_image(img_path)==0):
        feature_extraction_image(img_path)
        return "DeepFake"
    else:
        return "Real"

