import tensorflow as tf
import os
import time
import numpy as np
import math
import pathlib
import keras
import json
import shutil
from PIL import Image, ImageOps
from lime import lime_image
from skimage import io
from skimage.segmentation import mark_boundaries
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
# import geojson_writer

# Set a timer to measure the time it takes to run the script
start_time = time.time()

# Variables 
zoom_level = 15
location_name = 'test-pictures'
class_names = ['Cars', 'No cars']
output_analysis_images = True # This slows down the process a lot. Use only on small datasets 

# Load in the model for tensorflow from the model folder
model = tf.keras.models.load_model('models/cars_v1.h5', compile=False)
model_name = 'v1'

# Print the model summary
model.summary()

# Prepare the lime image explainer
explainer = lime_image.LimeImageExplainer()

# Data folder
data_dir = pathlib.Path(f"{location_name}")

# Set the batch size
images = list(data_dir.glob('*.png'))
image_count = len(images)
print(f"Going to analyze {image_count} images")

# Set up results dictionary
results = []

# Delete previous image results 
if os.path.exists('output-images/cars'):
    shutil.rmtree('output-images/cars')
os.makedirs('output-images/cars')

# Empty no-tennis image folder
if os.path.exists('output-images/no-cars'):
    shutil.rmtree('output-images/no-cars')
os.makedirs('output-images/no-cars')

for i in range(len(images)):
    # print(images[i])
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(images[i]).convert('RGB')
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)

    #turn the image into a numpy array
    image_array = np.asarray(image)
    # Normalize the image
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    # Load the image into the array
    data[0] = normalized_image_array

    # run the inference
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    image_name_raw = images[i]
    image_name_raw = str(image_name_raw)
    image_name = image_name_raw.replace(f"{location_name}/", "")
    image_name = image_name.replace(f"{zoom_level}/", "")
    image_name = image_name.replace("img/", "")
    image_name = image_name.replace(".png", "")

    print(f"Analyzing image {i} of {image_count} - {image_name_raw} - {image_name} - {class_name} - {confidence_score}")

    # Get part of string before slash
        
    result = {
        "index": i,
        "image_id": image_name,
        "image_name": image_name_raw,
        "classification_nr": index,
        "classification": class_name,
        "security": confidence_score,
    }

    results.append(result)

    if(class_name == 'Cars'):
        shutil.copyfile(image_name_raw, f"output-images/cars/{image_name}.png")
    
    if(class_name == 'No cars'):
        shutil.copyfile(image_name_raw, f"output-images/no-cars/{image_name}.png")

    # Do a lime image analysis if parameter is set to true
    if(output_analysis_images):
        explanation = explainer.explain_instance(normalized_image_array, model.predict, top_labels=5, hide_color=0, num_samples=1000)
        print(explanation)

        temp, mask = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=True)

        temp_1, mask_1 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=True, num_features=5, hide_rest=True)
        temp_2, mask_2 = explanation.get_image_and_mask(explanation.top_labels[0], positive_only=False, num_features=10, hide_rest=False)
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15,15))
        ax1.imshow(mark_boundaries(temp_1, mask_1))
        ax2.imshow(mark_boundaries(temp_2, mask_2))
        ax1.axis('off')
        ax2.axis('off')

        # If lime dir in trench folder is not there, make it
        if not os.path.exists(f"output-images/cars/lime"):
            os.makedirs(f"output-images/cars/lime")

        # If lime dir in no trench folder is not there, make it
        if not os.path.exists(f"output-images/no-cars/lime"):
            os.makedirs(f"output-images/no-cars/lime")

        # If the image is a trench, copy it to the trench folder
        if(class_name == 'Cars'):
            plt.savefig(f"output-images/cars/lime/{image_name}.png")
        
        if(class_name == 'No cars'):
            plt.savefig(f"output-images/no-cars/lime/{image_name}.png")

# Write results to file
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)

with open(f"{model_name}.json", 'w') as outfile:
    json.dump(results, outfile, cls=NpEncoder)

# Write results to geojson
# geojson_writer.write_geojson(location_name)

# Print time it took to run the script
print("--- %s seconds ---" % (time.time() - start_time))
