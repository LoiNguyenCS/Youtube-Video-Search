import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import os
import csv

# Load a pre-trained ResNet-18 model
resnet18 = models.resnet18(pretrained=True)
# Remove the classification layer (the final fully connected layer)
encoder = nn.Sequential(*list(resnet18.children())[:-1])

# Define a transformation to preprocess the images
data_transform = transforms.Compose([
    transforms.Resize(256), 
    transforms.CenterCrop(224),  
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Relevant folders
frames_folder = 'NPRVideoFrames'
embeddings_folder = 'NPREmbeddings'
os.makedirs(embeddings_folder, exist_ok=True)

# Loop through all subfolders in the frames folder
for subfolder in os.listdir(frames_folder):
    subfolder_path = os.path.join(frames_folder, subfolder)

    if os.path.isdir(subfolder_path):
        # List to store tuples of frame names and feature vectors for frames in the same video
        video_feature_list = []

        for frame in os.listdir(subfolder_path):
            frame_path = os.path.join(subfolder_path, frame)
            image = Image.open(frame_path)
            image = data_transform(image)

            frame_name = frame.replace("  NPR News Now", "")
            frame_name = frame_name.replace(".jpg", "")  
            frame_name = frame_name.replace(" ", "_")  

            # ENCODE THE IMAGE
            # -- The 'feature_vector' contains the encoded representation of the image
            with torch.no_grad():
                feature_vector = encoder(image.unsqueeze(0))

            # -- Flatten the tensor and convert to NumPy array
            flat_vector = feature_vector.view(-1).numpy()

            # -- Append the frame name and feature vector tuple to the list for the current video
            video_feature_list.append((frame_name, flat_vector))

        # EMBEDDING STORAGE IN CSV FILE
        # -- Define the CSV file path
        video_name = frame_name[:-11].replace("_", " ")
        csv_file_path = os.path.join(embeddings_folder, f"{video_name}.csv")

        # -- Write the data to the CSV file: define the column names and fill in the values
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Frame_Name'] + [f'Feature_{i}' for i in range(len(flat_vector))])

            for frame_name, flat_vector in video_feature_list:
                writer.writerow([frame_name] + flat_vector.tolist())
            
            print(video_name)