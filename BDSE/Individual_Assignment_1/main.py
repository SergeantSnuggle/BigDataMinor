import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix,  roc_auc_score
import numpy as np

"Own made libraries"
import database as db
import scrapping.scrapperSelenium as scrapperSelenium
import scrapping.scrapperSoup as scrapperSoup
import textCleaning as tc

#
# dfStrippedReviews = tc.kaggle_strip_reviews(dfReviews)
#
# dfLabelReviews = tc.kaggle_label_data(dfStrippedReviews)

# X = dfLabelReviews["Review"]
# y = dfLabelReviews["label"]
#
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
#
# stemmedTrain = tc.stem_text(X_train)
# stemmedTest = tc.stem_text(X_test)
#db.insert_df_into_db(dfLabelReviews, "label_kaggle_reviews", "replace")

# db.insert_df_into_db(dfReviews, "rawhoteldata", "replace")
#
# db1 = db.retrieve_table_into_df("rawhoteldata")
# link = "https://www.tripadvisor.com/Hotel_Review-g14129477-d10426242-Reviews-HOSHINOYA_Tokyo-Otemachi_Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html"
# scrappedReviews = scrapperSelenium.selenium_scrapper_tripadvisor(link, 20)
# db.insert_df_into_db(scrappedReviews, "scrappedrawhoteldata")
#
# df2 =db.retrieve_table_into_df("scrappedrawhoteldata")

# dfNegative = pd.read_csv("negative_hotel_reviews10k_cleaned.csv")
# dfPositive = pd.read_csv("positive_hotel_reviews10k_cleaned.csv")
# dfReviews = pd.concat([dfNegative, dfPositive], ignore_index=True)
#
# dfShuffled = dfReviews.sample(frac=1)
# X = dfShuffled["lemReviews"]
# y = dfShuffled["label"]
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
#
# ## VERY HANDY FOR NOT THAT FANCY COMPUTERS, SETTING MAX_FEATURES IN THE COUnTVECTORIZER
# vect = TfidfVectorizer(ngram_range=(1,2))
# ## NOTE AGAIN THE USE OF fit_transform FOR THE TRAIN SET
# ## NOTE AGAIN THE USE OF     transform FOR THE TEST SET
#
# X_train_vect = vect.fit_transform(X_train)
# X_test_vect = vect.transform(X_test)
#
# # Number of trees in random forest
# n_estimators = np.linspace(100, 3000, int((3000-100)/200) + 1, dtype=int)
# # Number of features to consider at every split
# max_features = ['auto', 'sqrt']
# # Maximum number of levels in tree
# max_depth = [1, 5, 10, 20, 50, 75, 100, 150, 200]
# # Minimum number of samples required to split a node
# # min_samples_split = [int(x) for x in np.linspace(start = 2, stop = 10, num = 9)]
# min_samples_split = [1, 2, 5, 10, 15, 20, 30]
# # Minimum number of samples required at each leaf node
# min_samples_leaf = [1, 2, 3, 4]
# # Method of selecting samples for training each tree
# bootstrap = [True, False]
# # Criterion
# criterion=['gini', 'entropy']
# random_grid = {'n_estimators': n_estimators,
# #                'max_features': max_features,
#                'max_depth': max_depth,
#                'min_samples_split': min_samples_split,
#                'min_samples_leaf': min_samples_leaf,
#                'bootstrap': bootstrap,
#                'criterion': criterion}
# rf_base = RandomForestClassifier()
# rf_random = RandomizedSearchCV(estimator = rf_base,
#                                param_distributions = random_grid,
#                                n_iter = 30, cv = 5,
#                                verbose=2,
#                                random_state=42, n_jobs = 4)
# rf_random.fit(X_train_vect, y_train)
#
#
# y_pred = rf_random.predict(X_test_vect)
# y_prob = rf_random.predict_proba(X_test_vect)[::, 1]
#
#
# from sklearn.metrics import accuracy_score, f1_score, confusion_matrix,  roc_auc_score
#
# print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
# print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
# print("AUC: \n", roc_auc_score(y_test, y_prob))
#
# resultsDf = pd.DataFrame(rf_random.cv_results_)
# resultsDf.to_csv =('randomTreeResultsCleaned.csv')

dfReviewsDb = db.retrieve_table_into_df('cleanedhoteldata')

X = dfReviewsDb["lemReviews"]
y = dfReviewsDb["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=69)

vect = CountVectorizer(max_features=1000)

X_train_vect = vect.fit_transform(X_train)
X_test_vect = vect.transform(X_test)

randomForest = RandomForestClassifier(n_estimators=721, min_samples_split=2, min_samples_leaf=4, max_depth=75, criterion="gini", bootstrap=True, n_jobs=-1)
randomForest.fit(X_train_vect, y_train)

y_pred = randomForest.predict(X_test_vect)
y_prob = randomForest.predict_proba(X_test_vect)[::, 1]

print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("AUC: \n", roc_auc_score(y_test, y_prob))

import pickle
filename = 'finalized_model_best_params2.sav'
pickle.dump(randomForest, open(filename, 'wb'))

