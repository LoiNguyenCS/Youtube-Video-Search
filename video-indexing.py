import keras
from keras import layers
import numpy as np
import cv2
import os
import sys



def split_video_into_frames(video_path, max_frames=25):
    video_dir = os.path.dirname(video_path)
    output_folder = os.path.join(video_dir, "Frames")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    video_capture = cv2.VideoCapture(video_path)
    fps = video_capture.get(cv2.CAP_PROP_FPS)
    frame_count = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    step_size = max(1, frame_count // max_frames)
    for frame_number in range(0, frame_count, step_size):
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = video_capture.read()

        if not ret:
            break

        frame_filename = os.path.join(output_folder, f"frame_{frame_number:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
    video_capture.release()

def load_frames_from_folder(folder):
    frames = []
    for filename in os.listdir(folder):
        if filename.endswith(".jpg"):
            img_path = os.path.join(folder, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            img = cv2.resize(img, (28, 28))  # Resize images to match the autoencoder input size
            frames.append(img)
    return np.array(frames)

def encode_frames(encoder, frames):
    frames = frames.astype("float32") / 255.0
    frames = frames.reshape((len(frames), np.prod(frames.shape[1:])))
    encoded_frames = encoder.predict(frames)
    return encoded_frames

def save_encoded_frames(encoded_frames, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for i, encoded_frame in enumerate(encoded_frames):
        np.save(os.path.join(output_folder, f"encoded_frame_{i:04d}.npy"), encoded_frame)

def train_autoencoder(x_train, x_test, encoding_dim=32, epochs=50, batch_size=256):
    # Define the input layer
    input_img = keras.Input(shape=(784,))

    # Encoder layers
    encoded = layers.Dense(encoding_dim, activation="relu")(input_img)

    # Decoder layers
    decoded = layers.Dense(784, activation="sigmoid")(encoded)

    # Create the autoencoder model
    autoencoder = keras.Model(input_img, decoded)

    # Create the encoder model
    encoder = keras.Model(input_img, encoded)

    # Create the decoder model
    encoded_input = keras.Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = keras.Model(encoded_input, decoder_layer(encoded_input))

    # Compile the autoencoder model
    autoencoder.compile(optimizer="adam", loss="binary_crossentropy")

    # Preprocess the data
    x_train = x_train.astype("float32") / 255.0
    x_test = x_test.astype("float32") / 255.0
    x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))

    # Train the autoencoder
    autoencoder.fit(
        x_train,
        x_train,
        epochs=epochs,
        batch_size=batch_size,
        shuffle=True,
        validation_data=(x_test, x_test),
    )
    return autoencoder

def combine_video_embeddings(embeddings):
    # Use simple averaging to combine embeddings
    combined_embedding = np.mean(embeddings, axis=0)
    return combined_embedding

def save_combined_embedding(combined_embedding, output_folder, video_path):
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_filename = f"combined_embedding_{video_name}.npy"
    output_path = os.path.join(output_folder, output_filename)
    np.save(output_path, combined_embedding)

video_path = sys.argv[1]
# split_video_into_frames(video_path)
frame_folder = os.path.join(os.path.dirname(video_path), "Frames")

all_frames = load_frames_from_folder(frame_folder)
split_index = len(all_frames) // 2
train_frames = all_frames[:split_index]
test_frames = all_frames[split_index:]

# autoencoder = train_autoencoder(train_frames, test_frames)
# encoder = keras.Model(autoencoder.input, autoencoder.layers[1].output)
# encoded_all_frames = encode_frames(encoder, all_frames)
# save_encoded_frames(encoded_all_frames, frame_folder)

encoded_frames_folder = frame_folder
encoded_all_frames = []

# Loop through each frame to get encoded frames
for filename in os.listdir(encoded_frames_folder):
    if filename.startswith("encoded_frame") and filename.endswith(".npy"):
        file_path = os.path.join(encoded_frames_folder, filename)

        # Load the encoded frame using NumPy
        encoded_frame = np.load(file_path)
        encoded_all_frames.append(encoded_frame)

# Combine the embeddings
combined_embedding = combine_video_embeddings(encoded_all_frames)

# Save the combined embedding in the same directory as the video_path
save_combined_embedding(combined_embedding, os.path.dirname(video_path), video_path)
