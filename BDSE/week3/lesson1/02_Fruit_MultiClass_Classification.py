import pandas as pd
import numpy as np

fruits = pd.read_csv('fruit_data_with_colors.txt', sep ="\t")
fruits.head()

print(fruits.shape)

# check the balance in the dataset
print(fruits.groupby('fruit_name').size())

import plotly.express as px
fig = px.histogram(fruits, x='fruit_name')
fig.show()


# Step 3: Splitting data
from sklearn.model_selection import train_test_split
X=fruits.drop('fruit_label',  axis=1)
y=fruits['fruit_label'].rename('label')



X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8, random_state=1)


# Step 4 : Chooing the model, in this case just pick one
from sklearn import svm

model = svm.SVC()
model.fit(X_train, y_train)

# OEPS error , drop some more columns
X=fruits.drop(['fruit_label','fruit_name','fruit_subtype'],  axis=1)

X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.8, random_state=1)

model = svm.SVC()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Step 5: Evaluate
from sklearn import metrics
from sklearn.preprocessing import OneHotEncoder

print("Classification Report %s:\n%s\n"
      % (model, metrics.classification_report(y_test, predictions)))

# Print a confusionmatrix
print("Confusion matrix:\n%s" % metrics.confusion_matrix(predictions,y_test,))


# Print a easy to read confusionmatrix
cm= pd.DataFrame(metrics.confusion_matrix(predictions,y_test)
        , index = ['pred:apple', 'pred:mandarin','pred:orange', 'pred:lemon']
        , columns = ['actual:apple', 'actual:mandarin','actual:orange', 'actual:lemon'])
print(cm)

cm['total_actual']=cm.sum(axis=1)
print(cm)

sum_row = cm.sum(axis=0)
print(sum_row)

sum_rowdf=pd.DataFrame(sum_row)
sum_rowdf.transpose()

cm_final=pd.concat([cm,sum_rowdf.transpose()])
print(cm_final)