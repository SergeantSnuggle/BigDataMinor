# https://www.kaggle.com/lilyelizabethjohn/standardization-using-standardscaler
# Can you classify monsters haunting Kaggle?
import numpy as np
import pandas as pd
import sklearn
from sklearn import linear_model, decomposition, datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

train = pd.read_csv("trainMonster.csv")

#Setup predictor and response variables
y=train['type']
index_train=train['id']
train=train.drop(['id','type'],axis=1)
X=pd.get_dummies(train)

from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.3,random_state=0)

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

#Logistic Regression without Standardization
model=LogisticRegression()
model.fit(X_train,y_train)
predictions=model.predict(X_test)
print(accuracy_score(predictions,y_test))



#Standardization
from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train_std=sc.fit_transform(X_train)
X_test_std=sc.transform(X_test)

#Logistic Regression on standardized dataset
model=LogisticRegression()
model.fit(X_train_std,y_train)
predictions_std=model.predict(X_test_std)
print(accuracy_score(predictions_std,y_test))