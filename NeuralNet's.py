# -*- coding: utf-8 -*-
"""
Created on Tue Sep  8 20:23:25 2020

@author: Fahad Siddiqui
"""
import pandas as pd
from preprocessing import DATAPREPROCESSING
from sklearn.preprocessing import StandardScaler
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

"""
once achive best result push on git
"""

