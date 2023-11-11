import numpy as np
import pandas as pd
import csv
import os
from sklearn.metrics.pairwise import normalize, cosine_similarity

folder_path = 'NPREmbeddings'
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]


# Load each CSV file and concatenate the DataFrames
df = pd.DataFrame()
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df_vid = pd.read_csv(file_path)

    # Add a 'Video_Name' column to identify each video
    video_name = os.path.splitext(csv_file)[0] 
    df_vid['Video_Name'] = video_name
    df = pd.concat([df, df_vid], ignore_index=True)

# Normalize embeddings
# Separate 'Frame_Name' column for later use
frame_names = df['Frame_Name']
df = df.drop(columns=['Frame_Name', 'Video_Name'])
df = pd.DataFrame(normalize(df, axis=1), columns=df.columns)

# Concatenate 'Frame_Name' column back to the DataFrame
df['Frame_Name'] = frame_names

def semantic_search(query_vector, dataframe, top_n=10):
    """
    Perform semantic search using cosine similarity.
    
    Parameters:
    - query_vector: The vector of the query.
    - dataframe: The DataFrame containing all vectors.
    - top_n: Number of similar vectors to retrieve.
    
    Returns:
    - top_n_indices: Indices of the top N similar vectors.
    """
    # Calculate cosine similarity
    cosine_similarities = cosine_similarity([query_vector], dataframe.iloc[:, :-1].values)[0]

    # Get the indices of top N similar vectors
    top_n_indices = cosine_similarities.argsort()[-top_n:][::-1]

    return top_n_indices

def generate_query_vector(csv_file, target_frame_name):
    with open(csv_file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)

        # Find the index of the frame_name in the header
        frame_name_index = header.index('Frame_Name')

        for row in reader:
            frame_name = row[0]
            if frame_name == target_frame_name:
                frame_data = list(map(float, row[1:]))  # Convert frame_data to float
                return frame_data

    return None

# Example usage:
# Assuming you have a query_vector (e.g., the vector of the user's query)
# and df is the DataFrame containing all video embeddings
# Specify the CSV file path and frame name
csv_file_path = 'NPREmbeddings/2000 Bodies Recovered After Dam Bursts In Derna Libya.csv'
frame_name = '2000_Bodies_Recovered_After_Dam_Bursts_In_Derna_Libya_frame_0000'
query_vector = generate_query_vector(csv_file_path, frame_name)

if query_vector is not None:
    top_similar_indices = semantic_search(query_vector, df)
    top_similar_videos = df.iloc[top_similar_indices]
    print(top_similar_videos)
else:
    print(f"Frame name '{frame_name}' not found in the CSV file.")
