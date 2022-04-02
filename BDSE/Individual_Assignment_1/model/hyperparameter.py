from sklearn.svm import SVC
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

dfNegative = pd.read_csv("..\\negative_hotel_reviews10k_cleaned.csv")
dfPositive = pd.read_csv("..\\positive_hotel_reviews10k_cleaned.csv")
dfReviews = pd.concat([dfNegative, dfPositive], ignore_index=True)

dfShuffled = dfReviews.sample(frac=1)
X = dfShuffled["lemReviews"]
y = dfShuffled["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)

## VERY HANDY FOR NOT THAT FANCY COMPUTERS, SETTING MAX_FEATURES IN THE COUnTVECTORIZER
vect = CountVectorizer(max_features=1000)
## NOTE AGAIN THE USE OF fit_transform FOR THE TRAIN SET
## NOTE AGAIN THE USE OF     transform FOR THE TEST SET

X_train_vect = vect.fit_transform(X_train)
X_test_vect = vect.transform(X_test)


kernels = ['linear', 'rbf', 'poly']
cParams = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0]
gamma = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0]

random_grid = {'kernel': kernels,
               'C': cParams,
               'gamma': gamma}

svm_base = SVC()

svm_random = RandomizedSearchCV(estimator=svm_base,
                                param_distributions=random_grid,
                                n_iter=30,
                                cv=5,
                                verbose=2,
                                random_state=42,
                                n_jobs=4)
#svm_random = SVC(probability=True, kernel='linear', gamma=0.1, C=0.01)
svm_random.fit(X_train_vect, y_train)

y_pred = svm_random.predict(X_test_vect)
y_prob = svm_random.predict_proba(X_test_vect)[::, 1]


from sklearn.metrics import accuracy_score, confusion_matrix,  roc_auc_score

print("Accuracy: {:.2f}%".format(accuracy_score(y_test, y_pred) * 100))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("AUC: \n", roc_auc_score(y_test, y_prob))

resultsDf = pd.DataFrame(svm_random.cv_results_)
resultsDf.to_csv =('svmresults.csv')
