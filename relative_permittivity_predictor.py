# -*- coding: utf-8 -*-
"""
Created on Tue Aug 16 18:27:38 2022

@author: Songqi Cao
"""

# Call functions
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.svm import SVR

# Load training data
DE = pd.read_excel('relative_permittivity_training_set.xlsx')
array = DE.values
X = array[:,2:100]
Y = array[:,1]

# Data transformation
scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)
# SVR model construction
SVM = SVR(kernel='rbf',C=10**1.333, epsilon=0.02, gamma=0.01).fit(X,Y)

# Prediction
prediction = pd.read_excel('to_predict_relative_permittivity.xlsx')
a = prediction.values
b = a[:,1:99]
c=scaler.transform(b)
result=SVM.predict(c)
composition=pd.read_excel('to_predict_relative_permittivity.xlsx',sheet_name='Sheet1', usecols="A")
composition=pd.DataFrame(composition)
result=pd.DataFrame(result)
predicted=np.column_stack((composition,result))
predicted=pd.DataFrame(predicted)
predicted.to_excel('predicted_relative_permittivity.xlsx', index=False, header=("Composition","Predicted relative permittivity"))
print('The relative permittivity has been predicted.\nPlease check the file "predicted_relative_permittivity.xlsx".')