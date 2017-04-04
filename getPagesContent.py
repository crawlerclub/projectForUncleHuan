from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup 
import time
import re
import os

def pageReady(d):
	return d.execute_script('return document.readyState') == 'complete'

if __name__ == '__main__':
	linkFile = open('NameLinks.txt','r')
	dcap = dict(DesiredCapabilities.PHANTOMJS)
	dcap['phantomjs.page.settings.userAgent']=('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')
	driver = webdriver.PhantomJS(executable_path='/Users/wujiakun/phantomjs/phantomjs-2.1.0-macosx/bin/phantomjs',desired_capabilities = dcap)
	outputDir = 'pageFiles'
	for c in linkFile:
		[name,link] = c.split('\t')
		try:
			linkname = re.findall('(\d+)',link)[0]
			outputFile = outputDir+'/'+linkname
			yesFile = outputDir + '/Y_' +linkname
			if os.path.exists(yesFile):
				continue
			driver.get(link)
			time.sleep(1)
			WebDriverWait(driver,10).until(pageReady)
			bsObj = BeautifulSoup(driver.page_source,'html.parser')
			pname = bsObj.find('div',class_='in-block ml10 f18 mb5 ng-binding').text
			print('-------loading %s ---------'%(name))
			print('               %s'%(pname))
			fout = open(outputFile,'w')
			fout.write(driver.page_source)
			fout.close()
			os.system('mv %s %s' % (outputFile,yesFile))
		except Exception as e:
			print('Error happens where download %s page:'%name,link)
			print(e)

