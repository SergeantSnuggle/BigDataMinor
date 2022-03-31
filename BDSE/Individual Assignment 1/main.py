import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

"Own made libraries"
import database as db
import scrapping.scrapperSelenium as scrapperSelenium
import scrapping.scrapperSoup as scrapperSoup
import textCleaning as tc


# dfReviews = pd.read_csv("Hotel_Reviews.csv", sep=',')
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

dfNegative = pd.read_csv("negative_hotel_reviews10k.csv")
dfPositive = pd.read_csv("positive_hotel_reviews10k.csv")
dfReviews = pd.concat([dfNegative, dfPositive], ignore_index=True)

dfShuffled = dfReviews.sample(frac=1)
X = dfShuffled["Review"]
y = dfShuffled["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

## VERY HANDY FOR NOT THAT FANCY COMPUTERS, SETTING MAX_FEATURES IN THE COUnTVECTORIZER
vect = CountVectorizer(max_features=1000, binary=False)
## NOTE AGAIN THE USE OF fit_transform FOR THE TRAIN SET
## NOTE AGAIN THE USE OF     transform FOR THE TEST SET

X_train_vect = vect.fit_transform(X_train)
X_test_vect = vect.transform(X_test)

# Number of trees in random forest
n_estimators = np.linspace(100, 3000, int((3000-100)/200) + 1, dtype=int)
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [1, 5, 10, 20, 50, 75, 100, 150, 200]
# Minimum number of samples required to split a node
# min_samples_split = [int(x) for x in np.linspace(start = 2, stop = 10, num = 9)]
min_samples_split = [1, 2, 5, 10, 15, 20, 30]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 3, 4]
# Method of selecting samples for training each tree
bootstrap = [True, False]
# Criterion
criterion=['gini', 'entropy']
random_grid = {'n_estimators': n_estimators,
#                'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf,
               'bootstrap': bootstrap,
               'criterion': criterion}
rf_base = RandomForestClassifier()
rf_random = RandomizedSearchCV(estimator = rf_base,
                               param_distributions = random_grid,
                               n_iter = 30, cv = 5,
                               verbose=2,
                               random_state=42, n_jobs = 4)
rf_random.fit(X_train_vect, y_train)


y_pred = rf_random.predict(X_test_vect)
y_prob = rf_random.predict_proba(X_test_vect)[::, 1]


from sklearn.metrics import accuracy_score, f1_score, confusion_matrix,  roc_auc_score

print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("AUC: \n", roc_auc_score(y_test, y_prob))

"""
Dit even morgen vragen hoe het beter kan. Voor nu doe ik het gewoon zo dat ik die twee dataframes samenvoeg
X_negative = dfNegative["Review"]
X_positive = dfPositive["Review"]
y_negative = dfNegative["label"]
y_positive = dfPositive["label"]
X_negative_train, X_negative_test, y_negative_train, y_negative_test = train_test_split(X_negative, y_negative, test_size=0.20)
X_positive_train, X_positive_test, y_positive_train, y_positive_test = train_test_split(X_positive, y_negative, test_size=0.20)
"""