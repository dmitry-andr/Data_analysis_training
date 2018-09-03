#import modules
import csv
from datetime import datetime

DATES_FORMAT = "%Y-%m-%d"  #2018-08-24

def normalizeDateFormat(dateToNormalize, originalFromatDescriptor):
	objDate = datetime.strptime(dateToNormalize, originalFromatDescriptor)
	normalizedDate = objDate.strftime(DATES_FORMAT)
	return normalizedDate

def reformatPercentageValue(percentageValue):
	formattedValue = percentageValue.replace("%","")
	
	return formattedValue

	
def mergeMapsByKey(mapsArray):
	if(len(mapsArray) == 0): return -1
	if(len(mapsArray) == 1): return -2
	mergedMap = {}
	for key, value in mapsArray[0].items():
		print(key, value)
		mergedData = [value]		
		for mapInList in mapsArray[1:]:
			print(mapInList)
			if(mapInList.get(key)):
				print("Adding data entry : ", mapInList[key])
				mergedData.append(mapInList[key])
		if(len(mergedData) == len(mapsArray)):
			print("Entries for date found in all maps : ", key, mergedData)
			mergedMap[key] = mergedData
	

	return mergedMap

def addDecisionColumnToMergedData(mergedMap):
	if(len(mergedMap) == 0): return -1
	if(len(mergedMap) == 1): return -2
	print("Adding decision column")
	mapWithDecisions = {}
	for key, value in mergedMap.items():
		labelRawValue = value[len(value) - 1]
		print("Label : ", labelRawValue)
		if(float(labelRawValue) < -0.3):
			value.append("-1:No")
		elif (float(labelRawValue) > 0.3):
			value.append("1:Yes")
		else:
			value.append("0:Risk")
		
		mapWithDecisions[key] = value
		
	return mapWithDecisions

def writeDataToCSV(dataMap):
	print("Writing data to file")
	print("Data items to be added to result set : ", len(dataMap))
	data = []
	for key, values in dataMap.items():		
		csvRow = [key]
		for value in values:
			csvRow.append(value)
		data.append(csvRow)
	with open("data/ml_data_generated/resulting_data.csv", 'w', newline='') as f:
		writer = csv.writer(f)
		writer.writerows(data)
				
	return 1;	

	

######### MAIN SCRIPT #########
print("Data preparations utility")


DJ_HIST_DATA_CSV = 'data/dj_historical_data.csv'
djHistoryMap = {}
with open(DJ_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		djHistoryMap[entryDate] = reformatPercentageValue(row[6])



ND_HIST_DATA_CSV = 'data/nd_historical_data.csv'
ndHistoryMap = {}
with open(ND_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		ndHistoryMap[entryDate] = reformatPercentageValue(row[6])

		
		
		
SP_HIST_DATA_CSV = 'data/sp_historical_data.csv'
spHistoryMap = {}
with open(SP_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		spHistoryMap[entryDate] = reformatPercentageValue(row[6])



EURUSD_HIST_DATA_CSV = 'data/eur_usd_historical_data.csv'
eurUsdHistoryMap = {}
with open(EURUSD_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		eurUsdHistoryMap[entryDate] = reformatPercentageValue(row[5])

		
mergedData = mergeMapsByKey([djHistoryMap, ndHistoryMap, spHistoryMap, eurUsdHistoryMap])
mergedDataWithDecisionColumn = addDecisionColumnToMergedData(mergedData)
writeDataToCSV(mergedDataWithDecisionColumn)


