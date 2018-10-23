from datetime import datetime

DATES_FORMAT = "%Y-%m-%d"  #2018-08-24
CSV_GENERATED_DATA_FOLDER = "data/ml_data_generated"
DATA_RECORD_CSV_FILE = "indices_scrapping_data.csv"


LOW_DECISION_VAL = 0.0098
TOP_DECISION_VAL = 0.0099


def normalizeDateFormat(dateToNormalize, originalFromatDescriptor):
	objDate = datetime.strptime(dateToNormalize, originalFromatDescriptor)
	normalizedDate = objDate.strftime(DATES_FORMAT)
	return normalizedDate

def reformatPercentageValue(percentageValue):
	formattedValue = percentageValue.replace("%","")
	
	return formattedValue
	
def getDecisionLabel(rawValue):
	if(float(rawValue) < LOW_DECISION_VAL):
		print("'-1:No' - Label : ", rawValue)
		return "-1:No"
	elif (float(rawValue) > TOP_DECISION_VAL):
		print("'1:Yes' - Label : ", rawValue)
		return "1:Yes"
	else:
		print("'0:Risk' - Label : ", rawValue)
		return "0:Risk"
