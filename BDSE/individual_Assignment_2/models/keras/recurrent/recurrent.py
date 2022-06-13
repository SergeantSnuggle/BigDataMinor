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


def build_model():
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

    start_time = time.time()
    # create the model
    model = Sequential()
    model.add(Embedding(vocab_size, 32, input_length=max_len))
    model.add(LSTM(128))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc'])
    print(model.summary())

    history = model.fit(X_train, y_train, batch_size=128, epochs=10, verbose=1, validation_split=0.2)

    score = model.evaluate(X_test, y_test, verbose=1)

    print("Test Score:", score[0])
    print("Test Accuracy:", score[1])

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('model.png')
    plt.close()

    additional_model_values = {
        'test_score': round(score[0], 3),
        'test_accuracy': round(score[1], 3),
        'date': str(datetime.now().replace(microsecond=0)),
        'duration': round(time.time() - start_time, 2),
        'amount_of_reviews': len(reviews)
    }

    json_additional_model_values = json.dumps(additional_model_values)
    with open(('variables.json'), 'w') as file:
        file.write(json_additional_model_values)
    file.close()
    model.save('kerasRNN')
    dump(tokenizer, '../tokenizer.sav')



if __name__ == "__main__":
    build_model()
