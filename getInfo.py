import os
from bs4 import BeautifulSoup

def getInfoString(bsObj):
	infos = list(bsObj.find('div',class_='company_info_text'))
	infoString = '===================\n'
	infoString += infos[0].text + '\n'
	for i in infos[2:]:
		infoString += i.text + '\n'
	return infoString

if __name__ == '__main__':
	infoDir = 'pageFiles'
	fout = open('companyInfo.txt','w')
	for	dirpath,dirnames,filenames in os.walk('pageFiles'):
		if dirpath == infoDir:
			break
	for f in filenames:
		try:
			bsObj = BeautifulSoup(open(infoDir+'/'+f,'r').read(),'html.parser')
			infomation = getInfoString(bsObj)
			infomation += f+'\n'
			print(infomation)
			fout.write(infomation)
		except Exception as e:
			print('error happends in :',f)
			print(e)
		finally:
			fout.flush()
	fout.close()
	print('=========Done==============')
