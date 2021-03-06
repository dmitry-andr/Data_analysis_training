import time
import xlsxwriter
import os


from datetime import datetime


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from nltk import app
from _tracemalloc import start

#custom modules imports
import utils





MSG_ELEMENT_NOT_FOUND = "ERR : Element not found"

DATA_RECORD_INTERVAL_SEC = 10
DATA_RECORD_ITERATIONS_MAX = 200


TABLE_COLUMN_NO = "No"
TICKER_DATA_KEY_TICKER_NAME = "Ticker name"
TICKER_DATA_KEY_RECORD_DATE = "Record date"
TICKER_DATA_KEY_RECORD_TIME = "Record time"
TICKER_DATA_KEY_ABS_VALUE = "Value"
TICKER_DATA_KEY_CHANGE_VALUE = "Value change"
TICKER_DATA_KEY_CHANGE_PERCENT = "Value change percent"


columnsOrderList = [TABLE_COLUMN_NO,
                    TICKER_DATA_KEY_TICKER_NAME,
                    TICKER_DATA_KEY_RECORD_DATE,
                    TICKER_DATA_KEY_RECORD_TIME,
                    TICKER_DATA_KEY_ABS_VALUE,
                    TICKER_DATA_KEY_CHANGE_VALUE,
                    TICKER_DATA_KEY_CHANGE_PERCENT]



def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_css_selector(browser, cssSelector):

    #DEBUG data print
    #print("browser", browser)
    #print("cssSelector", cssSelector)

    try:
        browser.find_element_by_css_selector(cssSelector)
    except NoSuchElementException:
        return False
    return True

def cleanHtmlInnerContent(contentToClean):
    contentToClean = contentToClean.strip()
    contentToClean = contentToClean.replace("<p>", "\n")
    contentToClean = contentToClean.replace("<br>", "\n")
    contentToClean = contentToClean.replace("</p>", "")
    contentToClean = contentToClean.replace("&amp;", "&")
    contentToClean = contentToClean.replace("<i>", "'")
    contentToClean = contentToClean.replace("</i>", "'")
    contentToClean = contentToClean.replace("<b>", "")
    contentToClean = contentToClean.replace("</b>", "")
    contentToClean = contentToClean.replace("<u>", "")
    contentToClean = contentToClean.replace("</u>", "")
    
    return contentToClean
    
  




def extractTickerValueFromPage(browser):
    selector = "span#last_last"
    if(check_exists_by_css_selector(browser, selector)):
        valueElement = browser.find_element_by_css_selector(selector)
        value = str(valueElement.get_attribute('innerHTML'))
        return value
    else:
        return MSG_ELEMENT_NOT_FOUND


def extractTickerValueChangeFromPage(browser):
    selector = "span.arial_20"
    if(check_exists_by_css_selector(browser, selector)):
        valueChangeElement = browser.find_element_by_css_selector(selector)
        valueChange = str(valueChangeElement.get_attribute('innerHTML'))
        return valueChange
    else:
        return MSG_ELEMENT_NOT_FOUND
    
def extractTickerValueChangePercentFromPage(browser):
    selector = "span.arial_20.parentheses"
    if(check_exists_by_css_selector(browser, selector)):
        valueChangePercentElement = browser.find_element_by_css_selector(selector)
        valueChangePercent = str(valueChangePercentElement.get_attribute('innerHTML'))
        return valueChangePercent
    else:
        return MSG_ELEMENT_NOT_FOUND




def extractTickerData(browser, tickerName, scrapDate, scrapTime):

    tickerDataRecord = {
        TICKER_DATA_KEY_TICKER_NAME : tickerName
    }

    tickerDataRecord[TICKER_DATA_KEY_RECORD_DATE] = scrapDate
    tickerDataRecord[TICKER_DATA_KEY_RECORD_TIME] = scrapTime

    tickerVal = extractTickerValueFromPage(browser)
    tickerDataRecord[TICKER_DATA_KEY_ABS_VALUE] = tickerVal
    print("TICKER_DATA_KEY_ABS_VALUE : ", tickerVal)

    tickerValChange = extractTickerValueChangeFromPage(browser)
    tickerDataRecord[TICKER_DATA_KEY_CHANGE_VALUE] = tickerValChange
    print("TICKER_DATA_KEY_CHANGE_VALUE : ", tickerValChange)

    tickerValChangePercent = extractTickerValueChangePercentFromPage(browser)
    tickerDataRecord[TICKER_DATA_KEY_CHANGE_PERCENT] = utils.reformatPercentageValue(tickerValChangePercent)
    print("TICKER_DATA_KEY_CHANGE_PERCENT : ", tickerValChangePercent)
    
    return tickerDataRecord

def writeDataToCSV(dataRecordsArr):
    dataToWrite = []
    dataToWrite.append(dataRecordsArr[0][TICKER_DATA_KEY_RECORD_DATE])
    dataToWrite.append(dataRecordsArr[0][TICKER_DATA_KEY_RECORD_TIME])
    for record in dataRecordsArr:
        print(record)
        dataToWrite.append(record[TICKER_DATA_KEY_CHANGE_PERCENT])

    CSV_FILE_PATH = utils.CSV_GENERATED_DATA_FOLDER + "/" + utils.DATA_RECORD_CSV_FILE
    with open(CSV_FILE_PATH, 'a') as datafile:
        print("dataToWrite", dataToWrite)
        txtData = ""
        for idx, val in enumerate(dataToWrite):
            txtData += val
            if (idx < (len(dataToWrite) - 1)):
                 txtData += ","

        print("txtData", txtData)
        #If not beginning of the file, add new line cusrsor move
        if os.stat(CSV_FILE_PATH).st_size != 0:
            txtData = "\n" + txtData

        datafile.write(txtData)

    return 1;


# MAIN PROGRAM
print("Starting Selenium script to grab ticker data from web page")
options = webdriver.ChromeOptions()
options.add_argument("--lang=en")

browser_dji = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
browser_nd = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
browser_sp = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
browser_gld = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
browser_eurusd = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
# Make request - load page
browser_dji.get("https://www.investing.com/indices/us-30")
browser_nd.get("https://www.investing.com/indices/nasdaq-composite")
browser_sp.get("https://www.investing.com/indices/us-spx-500")
browser_gld.get("https://www.investing.com/commodities/gold")
browser_eurusd.get("https://www.investing.com/currencies/eur-usd")
time.sleep(10)



'''
print(">>>Test selector check")
print(check_exists_by_css_selector(browser, "span#last_last"))
'''



counter = 0
while (counter < DATA_RECORD_ITERATIONS_MAX):
        print('Iteration >>>> ', str(counter + 1))

        currentDateTime = datetime.now()
        currentDate = currentDateTime.strftime(utils.DATES_FORMAT)
        currentTime = currentDateTime.strftime('%H:%M:%S')
        print("Scrapping on : ", currentDate, currentTime)

        djiData = extractTickerData(browser_dji, "dji", currentDate, currentTime)
        ndData = extractTickerData(browser_nd, "nd", currentDate, currentTime)
        spData = extractTickerData(browser_sp, "sp", currentDate, currentTime)
        gldData = extractTickerData(browser_gld, "gld", currentDate, currentTime)
        eurusdData = extractTickerData(browser_eurusd, "eurusd", currentDate, currentTime)

        print(">>>dji : ", djiData)
        print(">>>ndData : ", ndData)
        print(">>>spData : ", spData)
        print(">>>gldData : ", gldData)
        print(">>>eurusdData : ", eurusdData)




        #Write data to file
        print("Writing data to CSV file : ", DATA_RECORD_CSV_FILE)
        writeDataToCSV([djiData, ndData, spData, gldData, eurusdData])



        counter += 1
        time.sleep(DATA_RECORD_INTERVAL_SEC)







browser_dji.close()
browser_nd.close()
browser_sp.close()
browser_gld.close()
browser_eurusd.close()
print("Selenium script - FINISHED")
