import re
from Package.manageFile import *
import lxml.html
import time
import sqlite3
import datetime
from datetime import date
import codecs
from datetime import datetime

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import selenium.webdriver.support.ui as ui 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def downloadWebPMUpage():
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 



	url='https://info.pmu.fr'

	caps = DesiredCapabilities.FIREFOX.copy()

	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	wait = ui.WebDriverWait(br,5)

	br.find_element_by_class_name('cnil-close').click()

	wait = ui.WebDriverWait(br,5)

	# #------------ Janvier
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 

	# #-------------décembre
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	# #-------------Novembre
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	
	
	# #------------Octobre
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	# #-----------Septembre
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	
	
	# #----------- aout
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	
	
	# #----------- Juillet
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	# #-------------Juin 
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	# #-------------mai 
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	


	# #-------------Avril 
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	


	# #-------------Février 
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	# #-------------Janvier 
	# time.sleep(2)
	# br.find_element_by_xpath("//div[@class='date']").click()
	# br.find_element_by_xpath("//a[@class='ui-datepicker-prev ui-corner-all']").click()
	# br.find_element_by_xpath(u'//a[text()="1"]').click() 	

	for v in range(1,8):
		time.sleep(2)
		wait = ui.WebDriverWait(br,5)
		br.find_element_by_xpath("//div[@class='date']").click()
		br.find_element_by_xpath(u'//a[text()="'+str(v)+'"]').click()

		wait = ui.WebDriverWait(br,5)
		time.sleep(10)	
		link = br.find_element_by_xpath	("(//button[contains(text(),'Programme en détails')])")
		link.click()
		wait = ui.WebDriverWait(br,5)

		soup=BeautifulSoup(br.page_source,'lxml')

		
		writeFile(soup.prettify(),'../02 - Page Web/listeProgramme.html')

		pagePMU = codecs.open('../02 - Page Web/listeProgramme.html', 'r','utf-8')
		listCourse=listeCoursePMU(pagePMU)
		print(listCourse)

		for j in range(0,len(listCourse)):
			query = ('UPDATE COURSE SET HIPPODROME="%s" WHERE URL = "%s" ' % 
			(	listCourse[j][0],listCourse[j][3]) )

			print(query)
			cursor.execute(query)
			connnexion.commit()

	

	br.close()














def listeCoursePMU(pagePMU):
	ligneEnreg=''
	topFlag=0

	# récupération des éléments de course
	numCourse=-1
	course={}
	listHippodrome=[]
	 
	for line in pagePMU:
		if re.search(r'.*?((<span class="hippodrome-libelle" title=")(.*?)(">))', line):
			hippo=re.search(r'.*?((<span class="hippodrome-libelle" title=")(.*?)(">))', line).group(1)
			listHippodrome.append(hippo.split('"')[3])

	
		if re.search(r'timeline-course-link', line):
			getCourse = re.split('"', line)
			numCourse+=1
			nomCourse = reTraiteInfos(str(getCourse[5][7:]))
			dateCourse = reTraiteInfos(str(getCourse[3][8:16]))
			cheminCourse = reTraiteInfos(str(getCourse[3]))
			numReunion=int(cheminCourse.split('/')[2].replace('R',''))-1
		
			#InfoCourse nom de la course/ chemin de la course / 
			infosCourse = [reTraiteInfos(listHippodrome[numReunion]),
						nomCourse,
			            dateCourse,
			            cheminCourse]
			course[numCourse]=infosCourse

	return course





downloadWebPMUpage()


