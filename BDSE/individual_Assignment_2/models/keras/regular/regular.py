import json
import time
from datetime import datetime
from joblib import load, dump
from sklearn.model_selection import train_test_split
from tensorflow import keras

from matplotlib import pyplot as plt
# Keras
from keras.callbacks import TensorBoard
from keras.preprocessing.text import one_hot
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers.core import Activation, Dropout, Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_longest_reviews
from BDSE.individual_Assignment_2.data.cleaning import clean_text_pandas

reviews = retrieve_longest_reviews()
cleanedReviews = clean_text_pandas(reviews)
X = cleanedReviews['review']
y = cleanedReviews['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

max_words = 5000

tokenizer = Tokenizer(num_words=max_words)
tokenizer.fit_on_texts(X_train)

X_train = tokenizer.texts_to_sequences(X_train)
X_test = tokenizer.texts_to_sequences(X_test)

max_len = 50  # tried 100 , 500 bad results

X_train = pad_sequences(X_train, padding='post', maxlen=max_len)
X_test = pad_sequences(X_test, padding='post', maxlen=max_len)

# Adding 1 because of reserved 0 index
vocab_size = len(tokenizer.word_index) + 1

# create the model  NN  see sample code previous lesson
model = Sequential()
model.add(Embedding(vocab_size, 50, input_length=max_len))
model.add(Flatten())
model.add(Dense(100, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
print(model.summary())

# Fit the model
history=model.fit(X_train, y_train, batch_size=128, epochs=6, verbose=1, validation_split=0.2)

# Final evaluation of the model
score = model.evaluate(X_test, y_test, verbose=1)

print(model.metrics_names)
print("Test Score:", score[0])
print("Test Accuracy:", score[1])