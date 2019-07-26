import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB

def knnCV(csvName, numMasks, folds, neighbors):
	dataFrame = pd.read_csv(csvName)
	listOfScores = []
	targets = dataFrame['Classification'].values
	for i in range(50 - numMasks + 1):
		inputs = dataFrame.iloc[:,0+(i*4):numMasks*4+(i*4)]

		knn = KNeighborsClassifier(n_neighbors = neighbors)
		cv_scores = cross_val_score(knn,inputs,targets,cv=folds)
		listOfScores.append(np.mean(cv_scores))
		#print(np.mean(cv_scores))
	#averageScore = np.mean(listOfScores)
	#maxScore = np.max(listOfScores)
	#minScore = np.min(listOfScores)
	#retVals = [maxScore,minScore,averageScore]
	#return retVals
	return listOfScores

def svmCV(csvName, numMasks, folds):
	dataFrame = pd.read_csv(csvName)
	listOfScores = []
	targets = dataFrame['Classification'].values
	for i in range(50 - numMasks + 1):
		inputs = dataFrame.iloc[:,0+(i*4):numMasks*4+(i*4)]

		svm = SVC(kernel = 'linear')
		cv_scores = cross_val_score(svm,inputs,targets,cv=folds)
		listOfScores.append(np.mean(cv_scores))
		#print(np.mean(cv_scores))
	#averageScore = np.mean(listOfScores)
	#maxScore = np.max(listOfScores)
	#minScore = np.min(listOfScores)
	#retVals = [maxScore,minScore,averageScore]
	#return retVals
	return listOfScores

def forestCV(csvName, numMasks, folds, trees):
	dataFrame = pd.read_csv(csvName)
	listOfScores = []
	targets = dataFrame['Classification'].values
	for i in range(50 - numMasks + 1):
		inputs = dataFrame.iloc[:,0+(i*4):numMasks*4+(i*4)]

		tre = RandomForestClassifier(n_estimators = trees)
		cv_scores = cross_val_score(tre,inputs,targets,cv=folds)
		listOfScores.append(np.mean(cv_scores))
		#print(np.mean(cv_scores))
	#averageScore = np.mean(listOfScores)
	#maxScore = np.max(listOfScores)
	#minScore = np.min(listOfScores)
	#retVals = [maxScore,minScore,averageScore]
	#return retVals
	return listOfScores

def bayesCV(csvName, numMasks, folds):
	dataFrame = pd.read_csv(csvName)
	listOfScores = []
	targets = dataFrame['Classification'].values
	for i in range(50 - numMasks + 1):
		inputs = dataFrame.iloc[:,0+(i*4):numMasks*4+(i*4)]

		gnb = GaussianNB()
		cv_scores = cross_val_score(gnb,inputs,targets,cv=folds)
		listOfScores.append(np.mean(cv_scores))
		#print(np.mean(cv_scores))
	#averageScore = np.mean(listOfScores)
	#maxScore = np.max(listOfScores)
	#minScore = np.min(listOfScores)
	#retVals = [maxScore,minScore,averageScore]
	#return retVals
	return listOfScores

def plotAvgs(avgVals):
	barWidth = 0.1
	axes = plt.gca()
	axes.set_ylim([0.25,1.0])
	x1 = np.arange(len(avgVals[0]))
	x2 = [x+barWidth for x in x1]
	x3 = [x+barWidth for x in x2]
	x4 = [x+barWidth for x in x3]
	x5 = [x+barWidth for x in x4]
	x6 = [x+barWidth for x in x5]
	x7 = [x+barWidth for x in x6]
	x8 = [x+barWidth for x in x7]

	plt.bar(x1, avgVals[0], width = barWidth, edgecolor='white', label = 'knnR')
	plt.bar(x2, avgVals[1], width = barWidth, edgecolor='white', label = 'knnI')
	plt.bar(x3, avgVals[2], width = barWidth, edgecolor='white', label = 'svmLR')
	plt.bar(x4, avgVals[3], width = barWidth, edgecolor='white', label = 'svmLI')
	plt.bar(x5, avgVals[4], width = barWidth, edgecolor='white', label = 'forR')
	plt.bar(x6, avgVals[5], width = barWidth, edgecolor='white', label = 'forI')
	plt.bar(x7, avgVals[6], width = barWidth, edgecolor='white', label = 'bayR')
	plt.bar(x8, avgVals[7], width = barWidth, edgecolor='white', label = 'bayI')

	plt.xlabel('Number of Masks', fontweight = 'bold')
	plt.xticks([x + barWidth for x in range(len(avgVals[0]))],['1','2','5','10','20','50'])

	plt.legend(loc = 'upper right')
	plt.show()

def generateAvgAccVals(filName1, filName2):
	fName = filName1
	fName2 = filName2

	averageVals = []
	knnRealVals = []
	print("k-NN -- Real")
	knnRealVals.append(knnCV(fName,1,10,10))
	knnRealVals.append(knnCV(fName,2,10,10))
	knnRealVals.append(knnCV(fName,5,10,10))
	knnRealVals.append(knnCV(fName,10,10,10))
	knnRealVals.append(knnCV(fName,20,10,10))
	knnRealVals.append(knnCV(fName,50,10,10))

	averageVals.append([])
	for vals0 in knnRealVals:
		averageVals[0].append(np.mean(vals0))


	knnImagVals = []
	print("k-NN -- Imaginary")
	knnImagVals.append(knnCV(fName2,1,10,10))
	knnImagVals.append(knnCV(fName2,2,10,10))
	knnImagVals.append(knnCV(fName2,5,10,10))
	knnImagVals.append(knnCV(fName2,10,10,10))
	knnImagVals.append(knnCV(fName2,20,10,10))
	knnImagVals.append(knnCV(fName2,50,10,10))

	averageVals.append([])
	for vals1 in knnImagVals:
		averageVals[1].append(np.mean(vals1))

	print("------------------------------------------")

	svmLinRealVals = []
	print("SVM - Linear -- Real")
	svmLinRealVals.append(svmCV(fName,1,10))
	svmLinRealVals.append(svmCV(fName,2,10))
	svmLinRealVals.append(svmCV(fName,5,10))
	svmLinRealVals.append(svmCV(fName,10,10))
	svmLinRealVals.append(svmCV(fName,20,10))
	svmLinRealVals.append(svmCV(fName,50,10))

	averageVals.append([])
	for vals2 in svmLinRealVals:
		averageVals[2].append(np.mean(vals2))

	svmLinImagVals = []
	print("SVM - Linear -- Imaginary")
	svmLinImagVals.append(svmCV(fName2,1,10))
	svmLinImagVals.append(svmCV(fName2,2,10))
	svmLinImagVals.append(svmCV(fName2,5,10))
	svmLinImagVals.append(svmCV(fName2,10,10))
	svmLinImagVals.append(svmCV(fName2,20,10))
	svmLinImagVals.append(svmCV(fName2,50,10))

	averageVals.append([])
	for vals3 in svmLinImagVals:
		averageVals[3].append(np.mean(vals3))

	print("------------------------------------------")

	forestRealVals = []
	print("RandomForest -- Real")
	forestRealVals.append(forestCV(fName,1,10,10))
	forestRealVals.append(forestCV(fName,2,10,10))
	forestRealVals.append(forestCV(fName,5,10,10))
	forestRealVals.append(forestCV(fName,10,10,10))
	forestRealVals.append(forestCV(fName,20,10,10))
	forestRealVals.append(forestCV(fName,50,10,10))

	averageVals.append([])
	for vals4 in forestRealVals:
		averageVals[4].append(np.mean(vals4))

	forestImagVals = []
	print("RandomForest -- Imaginary")
	forestImagVals.append(forestCV(fName2,1,10,10))
	forestImagVals.append(forestCV(fName2,2,10,10))
	forestImagVals.append(forestCV(fName2,5,10,10))
	forestImagVals.append(forestCV(fName2,10,10,10))
	forestImagVals.append(forestCV(fName2,20,10,10))
	forestImagVals.append(forestCV(fName2,50,10,10))

	averageVals.append([])
	for vals5 in forestImagVals:
		averageVals[5].append(np.mean(vals5))

	print("------------------------------------------")

	averageVals.append([])
	print("NaiveBayes -- Real")
	bayesRealVals = []
	bayesRealVals.append(bayesCV(fName,1,10))
	bayesRealVals.append(bayesCV(fName,2,10))
	bayesRealVals.append(bayesCV(fName,5,10))
	bayesRealVals.append(bayesCV(fName,10,10))
	bayesRealVals.append(bayesCV(fName,20,10))
	bayesRealVals.append(bayesCV(fName,50,10))

	averageVals.append([])
	for vals6 in bayesRealVals:
		averageVals[6].append(np.mean(vals6))

	averageVals.append([])
	print("NaiveBayes -- Imaginary")
	bayesImagVals = []
	bayesImagVals.append(bayesCV(fName2,1,10))
	bayesImagVals.append(bayesCV(fName2,2,10))
	bayesImagVals.append(bayesCV(fName2,5,10))
	bayesImagVals.append(bayesCV(fName2,10,10))
	bayesImagVals.append(bayesCV(fName2,20,10))
	bayesImagVals.append(bayesCV(fName2,50,10))

	averageVals.append([])
	for vals7 in bayesImagVals:
		averageVals[7].append(np.mean(vals7))

	return averageVals


averageVals = generateAvgAccVals('dmaFeaturesReal.csv','dmaFeaturesImaginary.csv')
plotAvgs(averageVals)




