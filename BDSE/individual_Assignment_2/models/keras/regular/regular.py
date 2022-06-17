import json
import time
from datetime import datetime
import pandas as pd
from joblib import load, dump
from sklearn.model_selection import train_test_split
from tensorflow import keras
from sklearn.metrics import roc_auc_score, roc_curve

from matplotlib import pyplot as plt
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers.core import Dropout, Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from BDSE.individual_Assignment_2.mongodb.retrieveData import retrieve_longest_reviews
from BDSE.individual_Assignment_2.data.cleaning import preprocess_reviews


def build_model():
    reviews = retrieve_longest_reviews()
    X = reviews['review']
    y = reviews['label']

    X = preprocess_reviews(X, 0)

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
    # Create the ANN model
    model = Sequential()
    model.add(Embedding(vocab_size, 50, input_length=max_len))
    model.add(Flatten())
    model.add(Dense(8, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(8, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['acc', keras.metrics.AUC()])
    print(model.summary())

    # Fit the model
    history = model.fit(X_train, y_train, batch_size=128, epochs=15, verbose=1, validation_split=0.2)

    # Final evaluation of the model
    score = model.evaluate(X_test, y_test, verbose=1)

    print(model.metrics_names)
    print("Test Score:", score[0])
    print("Test Accuracy:", score[1])
    print("AUC:", score[2])

    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig('annmodel.png')
    plt.close()

    additional_model_values = {
        'test_score': round(score[0], 3),
        'test_accuracy': round(score[1], 3),
        'auc': round(score[2], 3),
        'date': str(datetime.now().replace(microsecond=0)),
        'duration': round(time.time() - start_time, 2),
        'amount_of_reviews': len(reviews)
    }

    json_additional_model_values = json.dumps(additional_model_values)
    with open(('variables.json'), 'w') as file:
        file.write(json_additional_model_values)
    file.close()
    model.save('kerasANN')
    dump(tokenizer, 'tokenizer.sav')


def live_predict_model_regular(review):
    model = keras.models.load_model('E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/models/keras/regular/kerasANN')
    vect = load('E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/models/keras/regular/tokenizer.sav')

    processed_review = preprocess_reviews([review], 0)
    # make dictionary to get correct result
    instance = vect.texts_to_sequences(processed_review)

    flat_list = []
    for sublist in instance:
        for item in sublist:
            flat_list.append(item)

    flat_list = [flat_list]

    instance = pad_sequences(flat_list, padding='post', maxlen=50)

    resultPrediction = model.predict(instance)

    resultPrediction = resultPrediction.flat[0]
    resultPrediction = round(resultPrediction, 2)
    return resultPrediction


def get_regular_results():
    file = open('E:/Roy Dijkstra/School/BigData/BDSE/individual_Assignment_2/models/keras/regular/variables.json')
    results = file.read()
    json_results = json.loads(results)

    return json_results


if __name__ == "__main__":
    build_model()
    #result = live_predict_model_regular("Disappointed by housekeeping staff knocking on door to clean room before 8 30am on day of checkout ")
    # if result > 0.5:
    #     print('hihi')
    # else:
    #     print("fu")


