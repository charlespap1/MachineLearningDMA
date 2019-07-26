import pandas as pd
import numpy as np
import scipy.io
#import matplotlib.pyplot as plt
import csv



def createFeatureDict(filename, nth, rOrI):
	selection = 0
	if(rOrI == "real"):
		selection = 0
	else:
		selection = 1

	mat = scipy.io.loadmat(filename)
	temp = filename[:4]
	keyName = 'data_'+temp+'_aligned'
	digitData = mat[keyName]

	currTimeSeries = []

	#creates a dictionary to store all samples from 0-39
	dictDigit0 = {}

	#extracts each time series and adds to a dictionary of lists where keys are sample #. 
	#there is a single list value w/ ea. key that holds timeSeries lists ordered by mask# based on index
	for currSample in range(len(digitData)):
		for currMask in range(len(digitData[currSample][0])):
			currTimeSeries = []
			for timePt in range(len(digitData[currSample])):

				if((timePt + 1) % nth == 0):
					#changing the last index bracket between 0 and 1 selects real vs imaginary
					currTimeSeries.append(digitData[currSample][timePt][currMask][selection])
			if(dictDigit0.get(currSample) == None):
				currDictList = []
				currDictList.append(currTimeSeries)
				dictDigit0[currSample] = currDictList
			else:
				currDictList = dictDigit0.get(currSample)
				currDictList.append(currTimeSeries)
				dictDigit0[currSample] = currDictList


	#dictionary storing features where ea key is sample num.
	#then there is an array of 4 arrays ea holding 50 features
	featureDict = {}

	#calculates 4 features for each timeseries and adds them to featureDict
	for sampleNum in range(len(digitData)):
		currSampleSet = dictDigit0.get(sampleNum)
		peakFeatures = []
		waveFeatures = []
		dispersionFeatures = []
		autoCorrelationFeatures = []
		for currSeries in currSampleSet:

			#std deviation
			stan = np.std(currSeries)

			#mean
			avg = np.mean(currSeries)

			#coefficient dispersion
			rat = stan/avg

			#root mean square
			rms = np.sqrt(np.mean(np.square(currSeries)))

			#peak factor - ratio of the peak and root mean square value
			pek = 1/rms

			#wave factor - ratio of rms and mean
			wav = rms/avg

			#correlation coefficient with a time lag of 1
			corr = np.corrcoef(np.array([currSeries[:-1], currSeries[1:]]))
			coeff = corr[0][1]

			peakFeatures.append(pek)
			waveFeatures.append(wav)
			dispersionFeatures.append(rat)
			autoCorrelationFeatures.append(coeff)

		currDictList = []
		currDictList.append(peakFeatures)
		currDictList.append(waveFeatures)
		currDictList.append(dispersionFeatures)
		currDictList.append(autoCorrelationFeatures)
		featureDict[sampleNum] = currDictList

	return featureDict

def extractFeatures(everyNth,rOrI):
	n = everyNth
	#creates dictionaries of features for each digit
	listOfDicts = []
	print("Creating Dictionary: 0")
	listOfDicts.append(createFeatureDict('dig0.mat',n,rOrI))
	print("Creating Dictionary: 1")
	listOfDicts.append(createFeatureDict('dig1.mat',n,rOrI))
	print("Creating Dictionary: 2")
	listOfDicts.append(createFeatureDict('dig2.mat',n,rOrI))
	print("Creating Dictionary: 3")
	listOfDicts.append(createFeatureDict('dig3.mat',n,rOrI))
	print("Creating Dictionary: 4")
	listOfDicts.append(createFeatureDict('dig4.mat',n,rOrI))
	print("Creating Dictionary: 5")
	listOfDicts.append(createFeatureDict('dig5.mat',n,rOrI))
	print("Creating Dictionary: 6")
	listOfDicts.append(createFeatureDict('dig6.mat',n,rOrI))
	print("Creating Dictionary: 7")
	listOfDicts.append(createFeatureDict('dig7.mat',n,rOrI))
	print("Creating Dictionary: 8")
	listOfDicts.append(createFeatureDict('dig8.mat',n,rOrI))
	print("Creating Dictionary: 9")
	listOfDicts.append(createFeatureDict('dig9.mat',n,rOrI))

	return listOfDicts

def generateCsvOutput(outputFilename,everyNth,rOrI):
	listOfDicts = extractFeatures(everyNth,rOrI)
	#creates string descriptions for features to put as header in CSV file
	print("Creating Feature Descriptions")
	featureDescriptions = []
	for i in range(50):
		featureDescriptions.append('PeakM'+str(i))
		featureDescriptions.append('WaveM'+str(i))
		featureDescriptions.append('DispersionM'+str(i))
		featureDescriptions.append('AcfM'+str(i))

	featureDescriptions.append('Classification')

	print("Creating CSV File")
	#adding all features of ea sample to a list in correct order to be written to csv
	with open(outputFilename, 'w') as csvFile:
		writer = csv.writer(csvFile)
		writer.writerow(featureDescriptions)
		classification = 0
		for currDict in listOfDicts:
			print("Adding Rows: "+str(classification))
			for sample in range(len(currDict.keys())):
				currRow = []
				for index in range(len(currDict.get(sample)[0])):
					currRow.append(currDict.get(sample)[0][index])
					currRow.append(currDict.get(sample)[1][index])
					currRow.append(currDict.get(sample)[2][index])
					currRow.append(currDict.get(sample)[3][index])
				currRow.append(classification)
				writer.writerow(currRow)
			classification += 1

	csvFile.close()


generateCsvOutput('dmaFeaturesReal.csv',1,"real")

