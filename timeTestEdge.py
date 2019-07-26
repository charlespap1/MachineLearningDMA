import numpy as np
import joblib as jb
import scipy.io
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from timeit import default_timer as timer
import time
import csv

#loading in trained models

def extractSignals(digitNum):
	filename = 'dig'+str(digitNum)+'.mat'
	mat = scipy.io.loadmat(filename)
	temp = filename[:4]
	keyName = 'data_'+temp+'_aligned'
	digitData = mat[keyName]

	samples = []
	for currSample in range(len(digitData)):
		digitDat = digitData[currSample]
		#extracting the time series signals for a single sample all 50 masks
		digitMasks = []
		for currMask in range(len(digitDat[0])):
			currSeries = []
			for timePt in range(len(digitDat)):
				currSeries.append(digitDat[timePt][currMask][0])
			digitMasks.append(currSeries)
		samples.append(digitMasks)

	return samples

def timeTestSingleSampleMasks(digitD, numMasks):
	digitMasks = digitD[:numMasks]
	timeStart = timer()
	featureExtractionStart = timer()

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
	featureExtractionEnd = timer()

	newInp = np.array(inputTest)
	newInp = newInp.reshape(1,-1)

	modelLoadS = timer()
	loadedKnnModel = jb.load('trained_model_knn' + str(numMasks) + '.sav')
	loadedSvmModel = jb.load('trained_model_svm' + str(numMasks) + '.sav')
	loadedForestModel = jb.load('trained_model_forest' + str(numMasks) + '.sav')
	loadedBayesModel = jb.load('trained_model_bayes' + str(numMasks) + '.sav')
	modelLoadE = timer()

	classStart = timer()
	knnStart = timer()
	knnResult = loadedKnnModel.predict(newInp)
	knnEnd = timer()

	svmStart = timer()
	svmResult = loadedSvmModel.predict(newInp)
	svmEnd = timer()

	forestStart = timer()
	forestResult = loadedForestModel.predict(newInp)
	forestEnd = timer()

	bayesStart = timer()
	bayesResult = loadedBayesModel.predict(newInp)
	bayesEnd = timer()
	classEnd = timer()
	
	timeEnd = timer()

	timesT = []
	classTimeElapsed = classEnd - classStart
	featureTimeElapsed = featureExtractionEnd - featureExtractionStart
	modTimeElapsed = modelLoadE - modelLoadS
	totalTime = timeEnd - timeStart

	timesT.append(featureTimeElapsed)
	timesT.append(modTimeElapsed)
	timesT.append(classTimeElapsed)
	timesT.append(totalTime)

	return timesT

def timeTestSingleDigit(signals,numMasks):
	retVals = []
	featTime = []
	modTime = []
	classTime = []
	totalTime = []
	for sampleNum in range(len(signals)):
		print("Timing Sample #"+str(sampleNum))
		currSample = signals[sampleNum].copy()
		for i in range(50):
			timeTestVals = timeTestSingleSampleMasks(currSample.copy(),numMasks)
			featTime.append(timeTestVals[0])
			modTime.append(timeTestVals[1])
			classTime.append(timeTestVals[2])
			totalTime.append(timeTestVals[3])
	retVals.append(np.mean(featTime))
	retVals.append(np.mean(modTime))
	retVals.append(np.mean(classTime))
	retVals.append(np.mean(totalTime))

	return retVals

allTimes = []
currentDigitNum = 0
print("ExtractingSamples")
currSampleSet = extractSignals(currentDigitNum)

print("TimingWithSamples: 1 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,1)
allTimes.append(currTimeSet)

print("TimingWithSamples: 2 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,2)
allTimes.append(currTimeSet)

print("TimingWithSamples: 5 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,5)
allTimes.append(currTimeSet)

print("TimingWithSamples: 10 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,10)
allTimes.append(currTimeSet)

print("TimingWithSamples: 20 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,20)
allTimes.append(currTimeSet)

print("TimingWithSamples: 50 Masks")
currTimeSet = timeTestSingleDigit(currSampleSet,50)
allTimes.append(currTimeSet)

descrips = []
descrips.append("Feature Extraction")
descrips.append("Model Load")
descrips.append("Classification")
descrips.append("Total Time")

with open('timesTestedEdgeSolo.csv', 'w') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(descrips)
	for sample in allTimes:
		writer.writerow(sample)

csvFile.close()

#extracts a signal with every n'th time measurement then extracts features and predicts
#returns a list of time measurements
def timeTestNF(n,ftype):
	#assumes digitData is a single sample array
	digitMasks = []
	for currMask in range(len(digitDat[0])):
		currSeries = []
		for timePt in range(len(digitDat)):
			if((timePt + 1) % n == 0):
				currSeries.append(digitDat[timePt][currMask][0])
		temp = np.array(currSeries)
		if(ftype == 16):
			temp.astype('float16')
		if(ftype == 32):
			temp.astype('float32')
		digitMasks.append(temp)

	timeStart = time.time()
	featureExtractionStart = time.time()

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
	featureExtractionEnd = time.time()

	newInp = np.array(inputTest)
	newInp = newInp.reshape(1,-1)

	knnStart = time.time()
	knnResult = loadedKnnModel.predict(newInp)
	knnEnd = time.time()

	svmStart = time.time()
	svmResult = loadedSvmModel.predict(newInp)
	svmEnd = time.time()

	forestStart = time.time()
	forestResult = loadedForestModel.predict(newInp)
	forestEnd = time.time()

	bayesStart = time.time()
	bayesResult = loadedBayesModel.predict(newInp)
	bayesEnd = time.time()
	
	timeEnd = time.time()

	timesT = []
	knnTimeElapsed = knnEnd - knnStart
	svmTimeElapsed = svmEnd - svmStart
	forestTimeElapsed = forestEnd - forestStart
	bayesTimeElapsed = bayesEnd - bayesStart
	featureTimeElapsed = featureExtractionEnd - featureExtractionStart
	totalTime = timeEnd - timeStart

	timesT.append(featureTimeElapsed)
	timesT.append(knnTimeElapsed)
	timesT.append(svmTimeElapsed)
	timesT.append(forestTimeElapsed)
	timesT.append(bayesTimeElapsed)
	timesT.append(totalTime)

	return timesT


#CREATES CSV WITH TIME MEASUREMENTS FOR VARYING PARAMETERS FOR N AND F

# measurements = []
# measurements.append(timeTestNF(1,16))
# measurements.append(timeTestNF(1,32))
# measurements.append(timeTestNF(1,64))
# # measurements.append(timeTestNF(2,64))
# # measurements.append(timeTestNF(5,64))
# # measurements.append(timeTestNF(10,64))
# # measurements.append(timeTestNF(20,64))
# # measurements.append(timeTestNF(50,64))
# # measurements.append(timeTestNF(100,64))
# # measurements.append(timeTestNF(500,64))
# # measurements.append(timeTestNF(1000,64))
# descriptions = []
# descriptions.append("featureExtraction")
# descriptions.append("knn")
# descriptions.append("svm")
# descriptions.append("forest")
# descriptions.append("bayes")

# with open('timeTestF.csv', 'w') as csvFile:
# 	writer = csv.writer(csvFile)
# 	writer.writerow(descriptions)
# 	for currRow in measurements:
# 		writer.writerow(currRow)
# csvFile.close()


