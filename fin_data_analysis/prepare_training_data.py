#import modules
import csv
from datetime import datetime

DATES_FORMAT = "%Y-%m-%d"  #2018-08-24
DATA_FILE_TIME_PERIOD_SUFFIX = "_jan_aug_2018"#"_jan_2017_aug_2018"
LOW_DECISION_VAL = 0.0098
TOP_DECISION_VAL = 0.0099

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
		if(float(labelRawValue) < LOW_DECISION_VAL):
			value.append("-1:No")
			print("'-1:No' - Label : ", labelRawValue)
		elif (float(labelRawValue) > TOP_DECISION_VAL):
			value.append("1:Yes")
			print("'1:Yes' - Label : ", labelRawValue)
		else:
			value.append("0:Risk")
			print("'0:Risk' - Label : ", labelRawValue)
		
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
#Historical data downloaded from https://www.investing.com
print("Data preparations utility")


DJ_HIST_DATA_CSV = 'data/dji_historical_data' + DATA_FILE_TIME_PERIOD_SUFFIX + '.csv'
djHistoryMap = {}
with open(DJ_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		djHistoryMap[entryDate] = reformatPercentageValue(row[6])



ND_HIST_DATA_CSV = 'data/nd_IXIC_historical_data' + DATA_FILE_TIME_PERIOD_SUFFIX + '.csv'
ndHistoryMap = {}
with open(ND_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		ndHistoryMap[entryDate] = reformatPercentageValue(row[6])

		
		
		
SP_HIST_DATA_CSV = 'data/sp_SPX_historical_data' + DATA_FILE_TIME_PERIOD_SUFFIX + '.csv'
spHistoryMap = {}
with open(SP_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		spHistoryMap[entryDate] = reformatPercentageValue(row[6])

		
		
GLD_FUTURES_HIST_DATA_CSV = 'data/gld_futures_historical_data' + DATA_FILE_TIME_PERIOD_SUFFIX + '.csv'
gldFutHistoryMap = {}
with open(GLD_FUTURES_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		gldFutHistoryMap[entryDate] = reformatPercentageValue(row[6])#Pay attention to index !!! different in different hist data sets



EURUSD_HIST_DATA_CSV = 'data/eur_usd_fx_historical_data' + DATA_FILE_TIME_PERIOD_SUFFIX + '.csv'
eurUsdHistoryMap = {}
with open(EURUSD_HIST_DATA_CSV) as csvDataFile:
	csvReader = csv.reader(csvDataFile)
	next(csvReader, None)# skip header
	for row in csvReader:
		entryDate = normalizeDateFormat(row[0], '%b %d, %Y')
		#adding key-EntryDate ; value = percentChange
		eurUsdHistoryMap[entryDate] = reformatPercentageValue(row[5])

		
mergedData = mergeMapsByKey([djHistoryMap, ndHistoryMap, spHistoryMap, gldFutHistoryMap, eurUsdHistoryMap])
mergedDataWithDecisionColumn = addDecisionColumnToMergedData(mergedData)
writeDataToCSV(mergedDataWithDecisionColumn)


