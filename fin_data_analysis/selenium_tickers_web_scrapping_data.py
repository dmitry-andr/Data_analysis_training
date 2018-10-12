import time
import xlsxwriter

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from nltk import app
from _tracemalloc import start



BASE_URL = "https://www.investing.com/currencies/eur-usd"

MSG_ELEMENT_NOT_FOUND = "ERR : Element not found"

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
                    TICKER_DATA_KEY_ABS_VALUE]



def check_exists_by_xpath(browser, xpath):
    try:
        browser.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

def check_exists_by_css_selector(browser, cssSelector):

    print("browser", browser)
    print("cssSelector", cssSelector)

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
    
  


def extractAppNameFromPage(browser):
    appNameElement = browser.find_element_by_css_selector("div .id-app-title")
    appName = str(appNameElement.get_attribute('innerHTML'))
    return appName

def extractAppAdditionalInfo(browser):
    appInfoList = {
        'default': 'Value23568576'
    }
    additionalInfoItems = browser.find_elements_by_css_selector("div.details-section-contents div.meta-info")
    for addInfoContainer in additionalInfoItems:
        additionalInfoTitle = cleanHtmlInnerContent(addInfoContainer.find_element_by_css_selector("div .title").get_attribute('innerHTML'))
        print(additionalInfoTitle)
        additionalInfoContent = cleanHtmlInnerContent(addInfoContainer.find_element_by_css_selector("div .content").get_attribute('innerHTML'))
        print(additionalInfoContent)
        print("***************")
        appInfoList[additionalInfoTitle] = additionalInfoContent
    
    return appInfoList


def extract5StarsRatingsCountFromPage(browser):
    star5Element = browser.find_element_by_xpath("//*[@id='body-content']/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[1]/span[3]")
    numOf5stars = str(star5Element.get_attribute('innerHTML'))
    numOf5stars = numOf5stars.replace("&nbsp;", " ")
    return numOf5stars



def extractAppRankningScoreFromPage(browser):    
    RankScoreElement = browser.find_element_by_css_selector("div.score-container div.score")
    appRankingScore = str(RankScoreElement.get_attribute('innerHTML'))
    return appRankingScore

def extractTickerValueFromPage(browser):
    selector = "span#last_last"
    if(check_exists_by_css_selector(browser, selector)):
        valueElement = browser.find_element_by_css_selector(selector)
        value = str(valueElement.get_attribute('innerHTML'))
        return value
    else:
        return MSG_ELEMENT_NOT_FOUND
    





def extractTickerData(browser, tickerName):
    
 
    
    tickerDataRecord = {
        TICKER_DATA_KEY_TICKER_NAME : tickerName
    }
    tickerVal = extractTickerValueFromPage(browser)
    tickerDataRecord[TICKER_DATA_KEY_ABS_VALUE] = tickerVal
    print("TICKER_DATA_KEY_ABS_VALUE : ", tickerVal)
    
    
    

    return tickerDataRecord



# MAIN PROGRAM
print("Starting Selenium script to grap ticker data from web page")
options = webdriver.ChromeOptions()
options.add_argument("--lang=en")
browser = webdriver.Chrome("C:\development_softw\chromedriver_win32\chromedriver.exe", chrome_options=options)
# Make request - load page
browser.get(BASE_URL)
time.sleep(6)
extractTickerData(browser, "urd")


'''
print(">>>Test selector check")
print(check_exists_by_css_selector(browser, "span#last_last"))
'''


time.sleep(1)
print("Selenium script - FINISHED")
browser.close()
