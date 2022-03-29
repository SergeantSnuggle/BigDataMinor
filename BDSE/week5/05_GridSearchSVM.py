import pandas as pd 

winedf = pd.read_csv('winequality-red.csv', sep=',')
# print winedf.isnull().sum() # check for missing data
print (winedf.head(3))

X=winedf.drop(['quality'],axis=1)
Y=winedf['quality']

print (winedf['quality'].value_counts() )

from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix

X_train, X_test, y_train, y_test = train_test_split(X,Y,test_size=0.2, random_state=30)

model = SVC()

model.fit(X_train, y_train)

predictions=model.predict(X_test)

print("Confusion matrix:\n%s" % confusion_matrix(y_test, predictions))

from sklearn.pipeline import Pipeline
from sklearn.pipeline import make_pipeline
from sklearn.model_selection  import GridSearchCV

sc = StandardScaler()
model = SVC()
pipeline = Pipeline(steps=[('sc', sc),('svc', model)])

parameters =  [{
                    'svc__C': [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0],
                    'svc__kernel': ['linear']
                  },
                 {
                    'svc__C': [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0],
                    'svc__gamma': [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 10.0],
                    'svc__kernel': ['rbf']
                 }]

grid = GridSearchCV(pipeline, param_grid=parameters, cv=5) 

grid.fit(X_train, y_train) # will take some time: a few minutes

print ("score = %3.2f" %(grid.score(X_test,y_test)))
print (grid.best_params_)

resultsdf = pd.DataFrame(grid.cv_results_)