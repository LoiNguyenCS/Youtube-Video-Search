import keras
from keras import layers
import numpy as np

def train_autoencoder(x_train, x_test, encoding_dim=32, epochs=50, batch_size=256):
    # Define the input layer
    input_img = keras.Input(shape=(784,))

    # Encoder layers
    encoded = layers.Dense(encoding_dim, activation='relu')(input_img)

    # Decoder layers
    decoded = layers.Dense(784, activation='sigmoid')(encoded)

    # Create the autoencoder model
    autoencoder = keras.Model(input_img, decoded)

    # Create the encoder model
    encoder = keras.Model(input_img, encoded)

    # Create the decoder model
    encoded_input = keras.Input(shape=(encoding_dim,))
    decoder_layer = autoencoder.layers[-1]
    decoder = keras.Model(encoded_input, decoder_layer(encoded_input))

    # Compile the autoencoder model
    autoencoder.compile(optimizer='adam', loss='binary_crossentropy')

    # Preprocess the data
    x_train = x_train.astype('float32') / 255.
    x_test = x_test.astype('float32') / 255.
    x_train = x_train.reshape((len(x_train), np.prod(x_train.shape[1:])))
    x_test = x_test.reshape((len(x_test), np.prod(x_test.shape[1:])))
    
    # Train the autoencoder
    autoencoder.fit(x_train, x_train,
                    epochs=epochs,
                    batch_size=batch_size,
                    shuffle=True,
                    validation_data=(x_test, x_test))


