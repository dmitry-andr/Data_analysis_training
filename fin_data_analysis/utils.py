from datetime import datetime

DATES_FORMAT = "%Y-%m-%d"  #2018-08-24

def normalizeDateFormat(dateToNormalize, originalFromatDescriptor):
	objDate = datetime.strptime(dateToNormalize, originalFromatDescriptor)
	normalizedDate = objDate.strftime(DATES_FORMAT)
	return normalizedDate