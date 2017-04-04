from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
import time
import re

class pageLoaded(object):
	def __init__(self,currentPage):
		self.currentPage = currentPage

	def __call__(self,driver):
		pageNum = driver.find_element_by_css_selector('.pagination-page.ng-scope.active').text
		return self.currentPage == pageNum

def getBsObj(source,handler = 'html.parser'):
	return BeautifulSoup(source,handler)	

def getPageNum(driver,url):
	'''
	this function to get the specifict page numbers of the links to scrawl
	'''
	try:
		driver.get(url)
		element = WebDriverWait(driver,30).until( EC.presence_of_element_located((By.CSS_SELECTOR,'.total.ng-binding')) )
		num = re.findall('共(\d+)页',driver.find_element_by_css_selector('.total.ng-binding').text)[0]
		print('total number of the pages is :'+num)
		return int(num)
	except Exception as e:
		print('error happens when finding the max pageMax of getting the links')
		print(e)
		driver.close()


def getUrlLinks(driver,urlHead,urlTail,numOfPage,destFile):
	fout = open(destFile,'w')
	for i in range(numOfPage):
		url = urlHead + '/p' + str(i+1) + urlTail
		print('+++++++++++++++++++')
		print(url)
		print('+++++++++++++++++++')
		try:
			driver.get(url)
			WebDriverWait(driver,30).until(pageLoaded(str(i+1)))
			bsObj = getBsObj(driver.page_source)
			links = bsObj.findAll('a',class_ = 'query_name search-new-color')	
			for i in range(len(links)):
				link = links[i].text + '\t'+ links[i].attrs['href'] + '\n'
				fout.write(link)
				print(i,':',link)
		except Exception as e:
			print('error happened in getting links, page:'+str(i+1))
			print(e)
		finally:
			fout.flush()
	#end the driver
	fout.close()
	driver.close()


if __name__ == "__main__":
	urlHead = 'http://sc.tianyancha.com/search'
	urlTail = '?key=%E5%BB%BA%E7%AD%91'
	destFile = 'NameLinks.txt'
	driver = webdriver.PhantomJS(executable_path='/Users/wujiakun/phantomjs/phantomjs-2.1.0-macosx/bin/phantomjs')
	totalPages = getPageNum(driver,urlHead+urlTail)
	getUrlLinks(driver,urlHead,urlTail,totalPages,destFile)
	print('All links has been get')

