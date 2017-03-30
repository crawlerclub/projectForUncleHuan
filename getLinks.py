from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
import time

def pageLoaded(driver):
	return driver.execute_script("return document.readyState") == "complete"

def getBsObj(source,handler = 'html.parser'):
	return BeautifulSoup(source,handler)	

def getUrlLinks(driver,urlHead,urlTail,numOfPage):
	for i in range(numOfPage):
		url = urlHead + '/p' + str(i+1) + urlTail
		print('+++++++++++++++++++')
		print(url)
		print('+++++++++++++++++++')
		bsObj = None
		try:
			driver.get(url)
			element = WebDriverWait(driver,20).until(pageLoaded)
		finally:
			bsObj = getBsObj(driver.page_source)
		links = bsObj.findAll('a',class_ = 'query_name search-new-color')	
		for i in range(len(links)):
			print(i,':',links[i].attrs['href'])


if __name__ == "__main__":
	urlHead = 'http://sc.tianyancha.com/search'
	urlTail = '?key=建筑'
	driver = webdriver.PhantomJS(executable_path='/Users/wujiakun/phantomjs/phantomjs-2.1.0-macosx/bin/phantomjs')
	getUrlLinks(driver,urlHead,urlTail,50)

