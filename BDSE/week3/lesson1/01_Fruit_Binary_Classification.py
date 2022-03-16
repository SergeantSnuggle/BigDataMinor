import pandas as pd
import numpy as np
from sklearn import metrics
from numpy.core.fromnumeric import transpose

fruits = pd.read_csv("BDSE\\week3\\lesson1\\fruit_data_with_colors.txt", sep="\t")
fruits = pd.read_csv("week3\\lesson1\\fruit_data_with_colors.txt", sep="\t")
fruits.head()


# IsApple Yes/ No 
fruits['is_apple']= fruits['fruit_label'].apply(lambda x: 1 if (x==1) else 0)



1- fruits['is_apple'].sum() / fruits['is_apple'].count()

# 66% is not an apple.
# So a model need to do better dan 66% 

X=fruits.drop(['fruit_label','fruit_name','fruit_subtype', 'is_apple'],  axis=1)

y=fruits['is_apple'].rename('label')


# Step 3: Splitting data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,train_size=0.6, random_state=1)


# Step 4 : Choosing the model, in this case just pick one
from sklearn import svm

model = svm.SVC()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Step 5: Evaluate

# Print a confusionmatrix
print("Confusion matrix:\n%s" % metrics.confusion_matrix(predictions,y_test))

#Or the transpose
print("Confusion matrix:\n%s" % metrics.confusion_matrix(y_test,predictions))


# Print a easy to read confusionmatrix
cm= pd.DataFrame(metrics.confusion_matrix(predictions,y_test)
        , index = ['pred:apple', 'pred:other']
        , columns = ['actual:apple', 'actual:other'])


cm['total_actual']=cm.sum(axis=1)
sum_row = cm.sum(axis=0)
sum_rowdf=pd.DataFrame(sum_row)
sum_rowdf.transpose()

cm_final=pd.concat([cm,sum_rowdf.transpose()])
print(cm_final)

# or transpose

cm_tr= pd.DataFrame(metrics.confusion_matrix(y_test, predictions)
        , index = ['actual:apple', 'actual:other']
        , columns = ['pred:apple', 'pred:other'])

cm_tr['total_pred']=cm_tr.sum(axis=1)
sum_row = cm_tr.sum(axis=0)
sum_rowdf=pd.DataFrame(sum_row)
sum_rowdf.transpose()

cm_tr_final=pd.concat([cm_tr,sum_rowdf.transpose()])
print(cm_tr_final)

print('accuracy: ', (cm_tr_final.iloc[0,0]+cm_tr_final.iloc[1,1])/(cm_tr_final.iloc[2,2]))



from sklearn.metrics import accuracy_score

accuracy_score(y_test, predictions)