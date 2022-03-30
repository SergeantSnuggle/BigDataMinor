import pandas as pd

dfReviews = pd.read_csv("Hotel_Reviews.csv")
#dfReviews = pd.read_csv("Individual Assignment 1\\Hotel_Reviews.csv")
dfReviews.info()

dfStrippedReviews = dfReviews[["Hotel_Name", "Negative_Review", "Review_Total_Negative_Word_Counts", "Positive_Review",
                               "Review_Total_Positive_Word_Counts", "Reviewer_Score"]]

#copy both Negative and Positive reviews into one collums and remove No Negative and No Positive statements
dfStrippedReviews["Review"] = dfStrippedReviews["Negative_Review"].apply(lambda x: x.replace("No Negative", "")) + \
                              dfStrippedReviews["Positive_Review"].apply(lambda x: x.replace("No Positive", ""))

dfReviewScore = dfStrippedReviews[["Review", "Reviewer_Score"]]

#Score 5.5 means that there are ~8% negative(~40k). Score 5 means 6% negative(~30k). Do at max 8% split
dfReviewScore["label"] = dfReviewScore['Reviewer_Score'].apply(lambda x: 1 if x > 5.5 else 0)

from sklearn.model_selection import train_test_split

X = dfReviewScore["Review"]
y = dfReviewScore["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

from sklearn.feature_extraction.text import CountVectorizer
## VERY HANDY FOR NOT THAT FANCY COMPUTERS, SETTING MAX_FEATURES IN THE COUnTVECTORIZER
vect = CountVectorizer(max_features=1000, binary=False)
## NOTE AGAIN THE USE OF fit_transform FOR THE TRAIN SET
## NOTE AGAIN THE USE OF     transform FOR THE TEST SET

X_train_vect = vect.fit_transform(X_train)
X_test_vect = vect.transform(X_test)

from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(max_depth=25, random_state=0)
model = MultinomialNB()

model.fit(X_train_vect, y_train)

model.score(X_train_vect, y_train)

y_pred = model.predict(X_test_vect)
y_prob = model.predict_proba(X_test_vect)[::, 1]


from sklearn.metrics import accuracy_score, f1_score, confusion_matrix,  roc_auc_score

print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("AUC: \n", roc_auc_score(y_test, y_prob))
