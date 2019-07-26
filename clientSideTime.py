import numpy as np
import joblib as jb
import scipy.io
import requests
import base64
import jsonpickle
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from timeit import default_timer as timer
import time
import csv

#extracts all of the time series signals for a single digit
#returns a list where each index represents a sample and holds a 50x4096 list
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

#times local feature extraction and then the encoding and sending of data to server for classification
def localFeatureServerClass(digitD,numMasks):
	sTime = timer()
	fSt = timer()
	digitMasks = digitD[:numMasks]
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

	inputTest.insert(0,numMasks)
	tempArr = np.array(inputTest)

	fEn = timer()

	encS = timer()

	tempStr = jsonpickle.encode(tempArr)

	byteArr = tempStr.encode('utf-8')

	encE = timer()

	#change url to wherever you want to use server
	final_url="http://10.197.53.148:5000/api/test"
	#final_url="http://localhost:5000/api/test"
	mystr = base64.b64encode(byteArr)
	payload = {'digitDat':mystr}
	response = requests.post(final_url, data=payload)
	eTime = timer()
	decResp = jsonpickle.decode(response.text)
	encTime = encE - encS
	featTime = fEn - fSt
	totTime = eTime - sTime
	times = []
	decTime = float(decResp['decode'])
	claTime = float(decResp['classification'])
	modTime = float(decResp['models'])
	times.append(totTime)
	times.append(featTime)
	times.append(claTime)
	times.append(modTime)
	times.append(encTime)
	times.append(totTime - (encTime + decTime + featTime + claTime + modTime))
	times.append(decTime)
	return times

#times feature extraction and classification of data on server rather than locally
def serverFeatureClass(digitD,numMasks):
	#converting the first sample's time series into a transferable string
	sTime = timer()
	encS = timer()
	digitD = digitD[:numMasks]
	digitD.insert(0,numMasks)
	digitD.insert(1,"extract")
	tempStr = jsonpickle.encode(digitD,max_depth = 1)
	byteArr = tempStr.encode('utf-8')
	encE = timer()
	#change url to wherever you want to use server
	final_url="http://10.197.53.148:5000/api/test"
	#final_url="http://localhost:5000/api/test"
	mystr = base64.b64encode(byteArr)
	payload = {'digitDat':mystr}
	response = requests.post(final_url, data=payload)
	eTime = timer()
	decResp = jsonpickle.decode(response.text)
	times = []
	totTime = eTime - sTime
	encTime = encE - encS
	decTime = float(decResp['decode'])
	fetTime = float(decResp['feature'])
	claTime = float(decResp['classification'])
	modTime = float(decResp['models'])
	times.append(totTime)
	times.append(fetTime)
	times.append(claTime)
	times.append(modTime)
	times.append(encTime)
	times.append(totTime - (encTime + decTime + fetTime + claTime + modTime))
	times.append(decTime)
	return times

#50 repetitions for each sample timing both local and server side feature extraction
def timeSingleDigit(signals,numMasks):
	currL = []
	locTot = []
	locFet = []
	locCla = []
	locMod = []
	locEnc = []
	locCom = []
	locDec = []
	serTot = []
	serFet = []
	serCla = []
	serMod = []
	serEnc = []
	serCom = []
	serDec = []
	for index in range(len(signals)):
		print("Timing Sample #"+str(index))
		currSample = signals[index].copy()
		for i in range(50):
			locF = localFeatureServerClass(currSample.copy(),numMasks)
			servF = serverFeatureClass(currSample.copy(),numMasks)
			locTot.append(locF[0])
			locFet.append(locF[1])
			locCla.append(locF[2])
			locMod.append(locF[3])
			locEnc.append(locF[4])
			locCom.append(locF[5])
			locDec.append(locF[6])
			serTot.append(servF[0])
			serFet.append(servF[1])
			serCla.append(servF[2])
			serMod.append(servF[3])
			serEnc.append(servF[4])
			serCom.append(servF[5])
			serDec.append(servF[6])
	currL.append(np.mean(locTot))
	currL.append(np.mean(locFet))
	currL.append(np.mean(locCla))
	currL.append(np.mean(locMod))
	currL.append(np.mean(locEnc))
	currL.append(np.mean(locCom))
	currL.append(np.mean(locDec))
	currL.append(np.mean(serTot))
	currL.append(np.mean(serFet))
	currL.append(np.mean(serCla))
	currL.append(np.mean(serMod))
	currL.append(np.mean(serEnc))
	currL.append(np.mean(serCom))
	currL.append(np.mean(serDec))
	return currL

#formats all of the timed samples into an output that can be visualized in a csv and is useful for data visualizations
def generateCsvOutput():
	allTimes = []
	currentDigitNum = 0
	print("ExtractingSamples")
	currSampleSet = extractSignals(currentDigitNum)

	print("TimingWithSamples: 1 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,1)
	allTimes.append(currTimeSet)

	print("TimingWithSamples: 2 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,2)
	allTimes.append(currTimeSet)

	print("TimingWithSamples: 5 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,5)
	allTimes.append(currTimeSet)

	print("TimingWithSamples: 10 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,10)
	allTimes.append(currTimeSet)

	print("TimingWithSamples: 20 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,20)
	allTimes.append(currTimeSet)

	print("TimingWithSamples: 50 Masks")
	currTimeSet = timeSingleDigit(currSampleSet,50)
	allTimes.append(currTimeSet)

	descrips = []
	descrips.append('localF-Tot')
	descrips.append('localF-Feat')
	descrips.append('localF-Class')
	descrips.append('localF-Mod')
	descrips.append('localF-Enc')
	descrips.append('localF-Comm')
	descrips.append('localF-Dec')
	descrips.append('serverF-Tot')
	descrips.append('serverF-Feat')
	descrips.append('serverF-Class')
	descrips.append('serverF-Mod')
	descrips.append('serverF-Enc')
	descrips.append('serverF-Comm')
	descrips.append('serverF-Dec')

	with open('timesTestedCompServer.csv', 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(descrips)
		for sample in allTimes:
			writer.writerow(sample)

	csvFile.close()


generateCsvOutput()
