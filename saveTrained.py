import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
import joblib as jb

def createTrainedModels(numMasks):
	dataFrame = pd.read_csv('dmaFeaturesReal.csv')
	targets = dataFrame['Classification'].values
	inpt = dataFrame.drop(columns = ['Classification'])
	inputs = inpt.iloc[:,0:numMasks*4]
	inputTrain, inputTest, targetTrain, targetTest = train_test_split(inputs, targets, test_size = .2, random_state = 1, stratify = targets)


	modelKnn = KNeighborsClassifier(n_neighbors = 10)
	modelKnn.fit(inputTrain,targetTrain)

	modelSvm = SVC(kernel = 'linear')
	modelSvm.fit(inputTrain,targetTrain)

	modelForest = RandomForestClassifier(n_estimators = 10)
	modelForest.fit(inputTrain,targetTrain)

	modelBayes = GaussianNB()
	modelBayes.fit(inputTrain,targetTrain)

	filNameKnn = 'trained_model_knn' + str(numMasks) + '.sav'
	filNameSvm = 'trained_model_svm' + str(numMasks) + '.sav'
	filNameForest = 'trained_model_forest' + str(numMasks) + '.sav'
	filNameBayes = 'trained_model_bayes' + str(numMasks) + '.sav'

	jb.dump(modelKnn,filNameKnn)
	jb.dump(modelSvm,filNameSvm)
	jb.dump(modelForest,filNameForest)
	jb.dump(modelBayes,filNameBayes)


createTrainedModels(1)
createTrainedModels(2)
createTrainedModels(5)
createTrainedModels(10)
createTrainedModels(20)
createTrainedModels(50)

