from datetime import datetime

DATES_FORMAT = "%Y-%m-%d"  #2018-08-24
CSV_GENERATED_DATA_FOLDER = "data/ml_data_generated"

def normalizeDateFormat(dateToNormalize, originalFromatDescriptor):
	objDate = datetime.strptime(dateToNormalize, originalFromatDescriptor)
	normalizedDate = objDate.strftime(DATES_FORMAT)
	return normalizedDate

def reformatPercentageValue(percentageValue):
	formattedValue = percentageValue.replace("%","")
	
	return formattedValue