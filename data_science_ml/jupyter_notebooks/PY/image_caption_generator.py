import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.applications.inception_v3 import InceptionV3
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, LSTM, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import Adam
from PIL import Image

# Load the pre-trained InceptionV3 model
image_model = InceptionV3(weights='imagenet')
new_input = image_model.input
hidden_layer = image_model.layers[-2].output
image_features_extract_model = Model(inputs=new_input, outputs=hidden_layer)

# Load captions and preprocess them
captions = [...]  # List of captions
images = [...]    # List of image filenames corresponding to captions

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(captions)
vocab_size = len(tokenizer.word_index) + 1

captions_sequences = tokenizer.texts_to_sequences(captions)
max_sequence_length = max(len(sequence) for sequence in captions_sequences)
captions_sequences_padded = pad_sequences(captions_sequences, maxlen=max_sequence_length, padding='post')

X_images = []
for image_filename in images:
    image = Image.open(image_filename)
    image = image.resize((299, 299))
    image = np.array(image)
    image = image.reshape(1, 299, 299, 3)
    image = image/255.0
    X_images.append(image)

X_images = np.vstack(X_images)
image_features = image_features_extract_model.predict(X_images)

y_captions = captions_sequences_padded[:, 1:]
y_captions = to_categorical(y_captions, num_classes=vocab_size)

# Define the caption generation model
input_image_features = Input(shape=(image_features.shape[1],))
image_features_dropout = Dropout(0.5)(input_image_features)
image_features_dense = Dense(256, activation='relu')(image_features_dropout)

input_captions = Input(shape=(max_sequence_length - 1,))
embedding_layer = Embedding(input_dim=vocab_size, output_dim=256)(input_captions)
embedding_dropout = Dropout(0.5)(embedding_layer)
lstm_layer = LSTM(256)(embedding_dropout)

decoder_input = keras.layers.add([image_features_dense, lstm_layer])
output = Dense(vocab_size, activation='softmax')(decoder_input)

caption_generator_model = Model(inputs=[input_image_features, input_captions], outputs=output)
caption_generator_model.compile(loss='categorical_crossentropy', optimizer=Adam(lr=0.001))

# Train the model
caption_generator_model.fit([image_features, captions_sequences_padded[:, :-1]], y_captions, batch_size=64, epochs=10)
