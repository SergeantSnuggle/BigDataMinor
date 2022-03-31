## https://towardsdatascience.com/sentiment-analysis-with-python-part-2-4f71e7bde59a

import numpy as np
import pandas as pd

import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score

import nltk

reviews_train = []
for line in open('full_train.txt', encoding="utf8"):
        reviews_train.append(line.strip())

print(len(reviews_train))
reviews_train [24999]


reviews_test = []
for line in open('full_test.txt', encoding="utf8"):
        reviews_test.append(line.strip())

print(len(reviews_test))
reviews_test [24999]


#Because of special structure of data
#Don't use this at home!!!!!
#Both train and test have  25000 observations
#Both train and test can be split in : First 12500 positive , last 12500 negative
#Don't do this at home

target = [1 if i < 12500 else 0 for i in range(25000)]

import re

REPLACE_NO_SPACE = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\d+)")
REPLACE_WITH_SPACE = re.compile("(<br\s*/><br\s*/>)|(\-)|(\/)")
NO_SPACE = ""
SPACE = " "

def preprocess_reviews(reviews):
    
    reviews = [REPLACE_NO_SPACE.sub(NO_SPACE, line.lower()) for line in reviews]
    reviews = [REPLACE_WITH_SPACE.sub(SPACE, line) for line in reviews]
    
    return reviews

reviews_train_clean = preprocess_reviews(reviews_train)
reviews_test_clean = preprocess_reviews(reviews_test)

baseline_vectorizer = CountVectorizer(binary=False)
#baseline_vectorizer.fit(reviews_train_clean)

X_baseline = baseline_vectorizer.fit_transform(reviews_train_clean)

# Note the difference between fit_transform and transform
X_test_baseline = baseline_vectorizer.transform(reviews_test_clean)

# just Checking
review0_baseline = baseline_vectorizer.transform([reviews_train_clean[0]])
print(review0_baseline)

print ('Shape of Sparse Matrix: ',X_baseline.shape)
print ('Amount of Non-Zero occurences: ', X_baseline.nnz)
print ('sparsity: %s' % (1- 100.0 * X_baseline.nnz /
                             (X_baseline.shape[0] *X_baseline.shape[1])))

final_model = LogisticRegression()
final_model.fit(X_baseline, target)
print ("Baseline Accuracy: %s" % accuracy_score(target, final_model.predict(X_test_baseline)))

print ("Baseline AUC: %s" %  roc_auc_score(target, final_model.predict_proba(X_test_baseline)[::,1]))

#Remove stopwords
from nltk.corpus import stopwords

english_stop_words = stopwords.words('english')
def remove_stop_words(corpus):
    removed_stop_words = []
    for review in corpus:
        removed_stop_words.append(
            ' '.join([word for word in review.split() 
                      if word not in english_stop_words])
        )
    return removed_stop_words

no_stop_words_train = remove_stop_words(reviews_train_clean)
no_stop_words_test = remove_stop_words(reviews_test_clean)

cv = CountVectorizer(binary=True)
X = cv.fit_transform(no_stop_words_train)
X_test = cv.transform(no_stop_words_test)

lr = LogisticRegression()
lr.fit(X, target)
print ("Remove Stopwords Accuracy : %s"  % ( accuracy_score(target, lr.predict(X_test))))
print ("Remove Stopwords AUC: %s" %  roc_auc_score(target, lr.predict_proba(X_test)[::,1]))

# Stemming
# Skip during demo
def get_stemmed_text(corpus):
    from nltk.stem.porter import PorterStemmer
    stemmer = PorterStemmer()
    return [' '.join([stemmer.stem(word) for word in review.split()]) for review in corpus]

#takes 5 minutes
#Skip during demo
stemmed_reviews_train = get_stemmed_text(reviews_train_clean)
stemmed_reviews_test = get_stemmed_text(reviews_test_clean)


import pickle
from joblib import dump, load
#Skip during demo
# with open("stemmed_reviews_train.txt", "wb") as fp: 
#       pickle.dump(stemmed_reviews_train, fp)
# with open("stemmed_reviews_test.txt", "wb") as fp: 
#       pickle.dump(stemmed_reviews_test, fp)
with open("stemmed_reviews_train.txt", "rb") as fp:   # Unpickling
      stemmed_reviews_train_loaded = pickle.load(fp)
with open("stemmed_reviews_test.txt", "rb") as fp:   # Unpickling
      stemmed_reviews_test_loaded = pickle.load(fp)

cv = CountVectorizer(binary=True)

X = cv.fit_transform(stemmed_reviews_train_loaded)
X_test = cv.transform(stemmed_reviews_test_loaded)
   
final_stemmed = LogisticRegression()
final_stemmed.fit(X, target)
print ("Stemmed Accuracy: %s" % accuracy_score(target, final_stemmed.predict(X_test)))

print ("Stemming AUC: %s" %  roc_auc_score(target, final_stemmed.predict_proba(X_test)[::,1]))

dump(final_stemmed, 'final_stemmed.joblib') 

final_stemmed_loaded= load('final_stemmed.joblib')
print ("Final Stemming: %s" % accuracy_score(target, final_stemmed_loaded.predict(X_test)))

#Lemmatization
from nltk import WordNetLemmatizer

def get_lemmatized_text(corpus):
    
    lemmatizer = WordNetLemmatizer()
    return [' '.join([lemmatizer.lemmatize(word) for word in review.split()]) for review in corpus]

#takes 5 minutes
#Skip during demo
lemmatized_reviews_train = get_lemmatized_text(reviews_train_clean)
lemmatized_reviews_test = get_lemmatized_text(reviews_test_clean)

#Skip during demo
# with open("lemmatized_reviews_train.txt", "wb") as fp: 
#       pickle.dump(lemmatized_reviews_train, fp)
# with open("lemmatized_reviews_test.txt", "wb") as fp: 
#       pickle.dump(lemmatized_reviews_test, fp)

cv = CountVectorizer(binary=True)

X = cv.fit_transform(lemmatized_reviews_train)
X_test = cv.transform(lemmatized_reviews_test)

final_lemmatized = LogisticRegression()
final_lemmatized.fit(X, target)
print ("Final Lemmatized Accuracy: %s"  % accuracy_score(target, final_lemmatized.predict(X_test)))

print ("Lemmatized AUC: %s" %  roc_auc_score(target, final_lemmatized.predict_proba(X_test)[::,1]))

# N-grams

ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, 2))
ngram_vectorizer.fit(reviews_train_clean)

X = ngram_vectorizer.transform(reviews_train_clean)
X_test = ngram_vectorizer.transform(reviews_test_clean)

final_ngram = LogisticRegression()
final_ngram.fit(X, target)
print ("Accuracy uni- bi grams: %s"  % accuracy_score(target, final_ngram.predict(X_test)))

print ("WordCount AUC: %s" %  roc_auc_score(target, final_wc.predict_proba(X_test)[::,1]))

# Counting Words Yes /no

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

wc_vectorizer = CountVectorizer(binary=False)

X = wc_vectorizer.fit_transform(reviews_train_clean)
X_test = wc_vectorizer.transform(reviews_test_clean)

final_wc = LogisticRegression()
final_wc.fit(X, target)
print ("WordCount Accuracy: %s"  % accuracy_score(target, final_wc.predict(X_test)))

print ("WordCount AUC: %s" %  roc_auc_score(target, final_wc.predict_proba(X_test)[::,1]))

# TF-IDF
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

tfidf_vectorizer = TfidfVectorizer()

X = tfidf_vectorizer.fit_transform(reviews_train_clean)
X_test = tfidf_vectorizer.transform(reviews_test_clean)

final_tfidf = LogisticRegression()
final_tfidf.fit(X, target)
print ("TF_IDF Accuracy: %s" % accuracy_score(target, final_tfidf.predict(X_test)))

print ("TF_IDF AUC: %s" %  roc_auc_score(target, final_tfidf.predict_proba(X_test)[::,1]))

#SVM

stop_words = ['in', 'of', 'at', 'a', 'the']
ngram_vectorizer = CountVectorizer(binary=True, ngram_range=(1, 3), stop_words=stop_words)

X = ngram_vectorizer.fit_transform(reviews_train_clean)
X_test = ngram_vectorizer.transform(reviews_test_clean)

final = LinearSVC()
final.fit(X, target)
print ("Final Accuracy: %s" % accuracy_score(target, final.predict(X_test)))