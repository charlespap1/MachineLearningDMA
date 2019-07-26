import requests
import jsonpickle
import base64
import time
import threading
import numpy as np
import joblib as jb
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from flask import Flask, request, Response
from timeit import default_timer as timer

app = Flask(__name__)
@app.route('/api/test',methods=['POST'])
#@app.route('/')
#@app.route('/api/test')
def test():
	decodeTime = 0
	decodeS = timer()
	r = request
	data = r.form['digitDat']
	#decoding the string data
	decodTemp = base64.b64decode(data)
	decoded = decodTemp.decode('utf-8')

	decArr = jsonpickle.decode(decoded)
	numMasks = decArr[0]
	decodeE = 0
	
	featTime = 0
	featOrNo = decArr[1]
	features = []
	newDat = []
	if (featOrNo == "extract"):
		formattedDat = decArr[2:]
		formattedData = np.array(formattedDat)
		for currIndex in range(len(formattedData)):
			currArr = formattedData[currIndex]
			splitArr = currArr.split(", ")
			splitArr[0] = splitArr[0][1:]
			splitArr[-1] = splitArr[-1][:-1]
			newArr = np.array(splitArr).astype('float')
			newDat.append(newArr)

		decodeE = timer()
		fStart = timer()

		#performing feature extraction
		digitMasks = newDat
		digitFeatures = []
		peakFeatures = []
		waveFeatures = []
		dispFeatures = []
		autoCFeatures = []
		for tSeries in digitMasks:
		#std deviation
			stan = np.std(tSeries)

		#mean
			avg = np.mean(tSeries)

		#coefficient dispersion
			rat = stan/avg

				#root mean square
			rms = np.sqrt(np.mean(np.square(tSeries)))

				#peak factor - ratio of the peak and root mean square value
			pek = 1/rms

				#wave factor - ratio of rms and mean
			wav = rms/avg

				#correlation coefficient with a time lag of 1
			corr = np.corrcoef(np.array([tSeries[:-1], tSeries[1:]]))
			coeff = corr[0][1]  

			peakFeatures.append(pek)
			waveFeatures.append(wav)
			dispFeatures.append(rat)
			autoCFeatures.append(coeff)

		digitFeatures.append(peakFeatures)
		digitFeatures.append(waveFeatures)
		digitFeatures.append(dispFeatures)
		digitFeatures.append(autoCFeatures)

		inputTest = []
		for i in range(len(digitFeatures[0])):
			inputTest.append(digitFeatures[0][i])
			inputTest.append(digitFeatures[1][i])
			inputTest.append(digitFeatures[2][i])
			inputTest.append(digitFeatures[3][i])
		features = inputTest
		fEnd = timer()
		featTime = fEnd - fStart
	else:
		features = decArr[1:]
		decodeE = timer()


	modelLoadStart = timer()
	loadedKnnModel = jb.load('trained_model_knn' + str(int(numMasks)) + '.sav')
	loadedSvmModel = jb.load('trained_model_svm' + str(int(numMasks)) + '.sav')
	loadedForestModel = jb.load('trained_model_forest' + str(int(numMasks)) + '.sav')
	loadedBayesModel = jb.load('trained_model_bayes' + str(int(numMasks)) + '.sav')
	modelLoadEnd = timer()

	features = np.array(features)
	inpTest = features.reshape(1,-1)

	knnStart = timer()
	knnResult = loadedKnnModel.predict(inpTest)
	knnEnd = timer()

	svmStart = timer()
	svmResult = loadedSvmModel.predict(inpTest)
	svmEnd = timer()

	forestStart = timer()
	forestResult = loadedForestModel.predict(inpTest)
	forestEnd = timer()

	bayesStart = timer()
	bayesResult = loadedBayesModel.predict(inpTest)
	bayesEnd = timer()

	knnTimeElapsed = knnEnd - knnStart
	svmTimeElapsed = svmEnd - svmStart
	forestTimeElapsed = forestEnd - forestStart
	bayesTimeElapsed = bayesEnd - bayesStart
	classTime = knnTimeElapsed + svmTimeElapsed + forestTimeElapsed + bayesTimeElapsed
	modelTime = modelLoadEnd - modelLoadStart
	decodeTime = decodeE - decodeS

	response = {"classification":str(classTime),"decode":str(decodeTime),"feature":str(featTime),"models":str(modelTime)}
	response_pickled = jsonpickle.encode(response)
	return Response(response=response_pickled, status=200, mimetype = 'application/json')
	
app.run(host='0.0.0.0',port=5000,threaded=True)

