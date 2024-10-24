import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import VGG16
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense

# Load the VGG16 model
vgg_model = VGG16(weights='imagenet', include_top=False)
vgg_model.trainable = False

def extract_features(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    
    features = vgg_model.predict(img_array)
    return features.flatten()

# Example dataset (replace with your dataset)
captions = [
    "A dog playing in the park.",
    "A cat sitting on a window.",
    "A person riding a bicycle."
]
images = [
    "path/to/image1.jpg",
    "path/to/image2.jpg",
    "path/to/image3.jpg"
]

# Tokenize the captions
tokenizer = Tokenizer()
tokenizer.fit_on_texts(captions)
vocab_size = len(tokenizer.word_index) + 1

# Convert captions to sequences
sequences = tokenizer.texts_to_sequences(captions)
max_length = max(len(seq) for seq in sequences)
sequences = pad_sequences(sequences, maxlen=max_length)

def create_model(vocab_size, max_length):
    # Feature input
    image_input = Input(shape=(4096,))
    image_embedding = Dense(256, activation='relu')(image_input)

    # Caption input
    caption_input = Input(shape=(max_length,))
    caption_embedding = Embedding(vocab_size, 256)(caption_input)
    caption_lstm = LSTM(256)(caption_embedding)

    # Merge inputs
    merge = tf.keras.layers.add([image_embedding, caption_lstm])
    output = Dense(vocab_size, activation='softmax')(merge)

    model = Model(inputs=[image_input, caption_input], outputs=output)
    model.compile(loss='categorical_crossentropy', optimizer='adam')
    return model

model = create_model(vocab_size, max_length)

# Prepare features for training
features = np.array([extract_features(img) for img in images])

# Train the model (dummy y for demonstration; replace with actual caption targets)
model.fit([features, sequences[:, :-1]], tf.keras.utils.to_categorical(sequences[:, 1:], num_classes=vocab_size), epochs=20)

def generate_caption(model, tokenizer, img_path, max_length):
    feature = extract_features(img_path)
    feature = feature.reshape((1, 4096))
    
    caption = []
    input_seq = [tokenizer.word_index['startseq']]  # Start token
    for _ in range(max_length):
        input_seq = pad_sequences([input_seq], maxlen=max_length)
        yhat = model.predict([feature, input_seq], verbose=0)
        yhat = np.argmax(yhat)
        word = tokenizer.index_word.get(yhat, '')
        
        if word == 'endseq':  # End token
            break
        caption.append(word)
        input_seq.append(yhat)

    return ' '.join(caption)

# Usage example
caption = generate_caption(model, tokenizer, 'path/to/new_image.jpg', max_length)
print("Generated Caption:", caption)
