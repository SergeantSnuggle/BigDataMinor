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
import model.buildmodel as bm

lr = bm.build_lr()

import pickle
filename = 'model/saved/Linear_best_params.sav'
pickle.dump(lr, open(filename, 'wb'))
# import model.hyperparameter as hyp
#
# results = hyp.hyper_lr()
#
# db.insert_df_into_db(results, 'tempresultaten', 'replace')


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

#
# import pickle
# filename = 'model/finalized_random_model_best_params2.sav'
# pickle.dump(randomForest, open(filename, 'wb'))

