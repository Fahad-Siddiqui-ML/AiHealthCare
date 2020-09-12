# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 20:07:43 2020

@author: Fahad Siddiqui
"""


"""
Code under development phase
"""

import pandas as pd
from preprocessing import DATAPREPROCESSING
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.decomposition import PCA

obj = DATAPREPROCESSING("Train_Beneficiarydata-1542865627584.csv", "Train_Inpatientdata-1542865627584.csv"
                ,"Train_Outpatientdata-1542865627584.csv", "Train-1542865627584.csv")


Dataset = obj.Processing()
Dataset.head()


values = {'AdmitDays': round(Dataset['AdmitDays'].mean(), 0), 
          'DeductibleAmtPaid': round(Dataset['DeductibleAmtPaid'].mean(), 0)}
Dataset = Dataset.fillna(value=values)
Dataset.PotentialFraud.replace(['Yes','No'],['1','0'],inplace=True)
Dataset.PotentialFraud=Dataset.PotentialFraud.astype('int64')
Dataset.Gender=Dataset.Gender.astype('category')
Dataset.Race=Dataset.Race.astype('category')
Dataset = pd.get_dummies(Dataset,columns=['Gender','Race'],drop_first=True)

X = Dataset.iloc[:, 2:29].values
y = Dataset.iloc[:, 1].values


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)


sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)
#%%
# Section for PCA
pca = PCA(n_components = None)
X_train = pca.fit_transform(X_train)
X_test = pca.transform(X_test)
explained_veriance = pca.explained_variance_ratio_

#%%
classifier = RandomForestClassifier()
#%%

#hyper parameter tunning
#hyper parameter tunning
paremeters = {'n_estimators':[10, 100, 1000],
              'criterion' : ['gini', 'entropy']
              }

grid_search = GridSearchCV(estimator=classifier, 
                           param_grid=paremeters,
                           scoring = "accuracy", 
                           cv = 1000,
                           verbose = 10,
                           n_jobs = -1)

grid_search = grid_search.fit(X_train, y_train)
best_acc = grid_search.best_score_
best_para = grid_search.best_params_
#%%
# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix, classification_report
CM = confusion_matrix(y_test, y_pred)
print("ACC: {0}".format((CM[0][0]+CM[1][1])/len(X_test)))








