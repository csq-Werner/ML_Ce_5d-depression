# -*- coding: utf-8 -*-
"""
Created on Mon Jun  6 23:46:40 2022

@author: Songqi Cao
"""

'''
Data in the literature are collected in excel 5d_training_set.
The relative permittivity is predicted using the model in https://doi.org/10.1063/5.0012434.
A SVR (supporting vector regression) model was constructed to predicted the 5d-depression.
The input of this predictor should be prepared as an excel file named to_predict_5d_depression.
An example of the input file was provided.
'''

import pandas as pd
from sklearn.svm import SVR
from sklearn import preprocessing
import numpy as np

#Step 1 
DE = pd.read_excel('data/5d_depression_training_set.xlsx')
array = DE.values
X = array[:,2:10]
Y = array[:,1]
DE=pd.read_excel('to_predict_5d_depression.xlsx')
array=DE.values
X_to_predict=array[:,1:9]

#Step 2 Scaling and training
scaler = preprocessing.StandardScaler().fit(X)
X = scaler.transform(X)
X_to_predict=scaler.transform(X_to_predict)




SVR = SVR(kernel='rbf',C=10**6.75, epsilon=0.1, gamma=0.01).fit(X, Y)

#Step 3 Predicting
prediction=SVR.predict(X_to_predict)
composition=array[:,0]
composition=pd.DataFrame(composition)
result=pd.DataFrame(prediction)
predicted=np.column_stack((composition,result))
predicted=pd.DataFrame(predicted)
predicted.to_excel('predicted_5d-depression.xlsx', index=False, header=("Composition","Predicted 5d_depression"))

print('The 5d-depression has been predicted.\nPlease check the file "predicted_5d_depression.xlsx".')
