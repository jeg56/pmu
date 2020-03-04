# -*- coding: UTF8 -*-
import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import selenium.webdriver.support.ui as ui 
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from Package.manageFile import *
import codecs


def downloadWebPMUpage():
	url='https://info.pmu.fr'

	caps = DesiredCapabilities.FIREFOX.copy()
	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	wait = ui.WebDriverWait(br,5)
	time.sleep(10)

	br.find_element_by_class_name('cnil-close').click()


	#br.find_element_by_xpath("//a[@id='calendar-previous']").click()
	br.find_element_by_xpath("//a[@id='calendar-next']").click()
	wait = ui.WebDriverWait(br,5)

	

	link = br.find_element_by_xpath	("(//button[contains(text(),'Programme en détails')])")
	link.click()
	time.sleep(10)

	wait = ui.WebDriverWait(br,5)

	soup=BeautifulSoup(br.page_source,'lxml')

	br.close()
	writeFile(soup.prettify(),'../02 - Page Web/listeProgramme.html')

	file = codecs.open('../02 - Page Web/listeProgramme.html', 'r','utf-8')
	return file
	




def downloadWebPMUCourse(course_url):
	url='https://info.pmu.fr/programme/'+course_url

	caps = DesiredCapabilities.FIREFOX.copy()
	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	time.sleep(5)

	br.find_element_by_class_name('cnil-close').click()
	time.sleep(1)
	br.find_element_by_xpath("//li[@class='partants actif visible']" and "//li[@data-tag='tag:clic:tableauPartants']").click()
	time.sleep(2)
	soup=BeautifulSoup(br.page_source,'lxml')
	br.close()
	
	writeFile(soup.prettify(),'../02 - Page Web/course.html')
	#writeFile(soup.prettify(),'../02 - Page Web/'+course_url.replace('/','_')+'.html')
	wait = ui.WebDriverWait(br,5)
	file = codecs.open('../02 - Page Web/course.html', 'r','utf-8')
	
	return file.read()



def downloadWebPMURapport(course_url):
	url='https://info.pmu.fr/programme/'+course_url

	caps = DesiredCapabilities.FIREFOX.copy()
	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	time.sleep(5)

	br.find_element_by_class_name('cnil-close').click()

	soup=BeautifulSoup(br.page_source,'lxml')

	time.sleep(1)
	wait = ui.WebDriverWait(br,5)





def downloadWebPMUCourseV2(course_url):
	url='https://info.pmu.fr/programme/'+course_url

	caps = DesiredCapabilities.FIREFOX.copy()
	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	time.sleep(10)

	br.find_element_by_class_name('cnil-close').click()

	soup=BeautifulSoup(br.page_source,'lxml')
	
	writeFile(soup.prettify(),'../02 - Page Web/course.html')
	#writeFile(soup.prettify(),'../02 - Page Web/'+course_url.replace('/','_')+'.html')
	time.sleep(1)

	wait = ui.WebDriverWait(br,10)
	
	dicRapport={}

	type_RAPPORT='SIMPLE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')

		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='SIMPLE_INTERNATIONAL'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')

		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''


	type_RAPPORT='SIMPLE_GAGNANT_INTERNATIONAL'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')

		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''



	type_RAPPORT='COUPLE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
		print(dicRapport[type_RAPPORT])
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='COUPLE_ORDRE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''


	type_RAPPORT='COUPLE_ORDRE_INTERNATIONAL'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')

		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''


	type_RAPPORT='TRIO_ORDRE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='TRIO'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='TRIO_ORDRE_INTERNATIONAL'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')

		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''



	type_RAPPORT='DEUX_SUR_QUATRE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='MULTI'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='MINI_MULTI'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''


	type_RAPPORT='TIERCE'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='QUARTE_PLUS'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''

	type_RAPPORT='QUINTE_PLUS'
	try:
		br.find_element_by_xpath("//li[@class='picto-pari-action pari-list-item svg']" and "//li[@data-family='"+type_RAPPORT+"']").click()
		time.sleep(5)
		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),"../02 - Page Web/rapport_"+type_RAPPORT+".html")
		wait = ui.WebDriverWait(br,5)
		dicRapport[type_RAPPORT]= codecs.open("../02 - Page Web/rapport_"+type_RAPPORT+".html", 'r','utf-8')
	except Exception as e:
		dicRapport[type_RAPPORT]=''
	
	
	br.close()
	return dicRapport


def downloadWebPMUCourseV3(course_url):
	url='https://info.pmu.fr/programme/'+course_url

	caps = DesiredCapabilities.FIREFOX.copy()
	caps['marionette'] = True
	br = webdriver.Firefox(capabilities=caps, executable_path='./Package/geckodriver.exe')
	br.get(url)

	soup=''
	time.sleep(10)

	br.find_element_by_class_name('cnil-close').click()

	soup=BeautifulSoup(br.page_source,'lxml')
	
	writeFile(soup.prettify(),'../02 - Page Web/course.html')
	#writeFile(soup.prettify(),'../02 - Page Web/'+course_url.replace('/','_')+'.html')
	time.sleep(1)
	wait = ui.WebDriverWait(br,5)

	file = codecs.open('../02 - Page Web/course.html', 'r','utf-8')


	br.find_element_by_xpath("//i[@class='icon icon-formule']").click()

	time.sleep(5)

	wait = ui.WebDriverWait(br,5)

	soup=BeautifulSoup(br.page_source,'lxml')
	

	writeFile(soup.prettify(),'../02 - Page Web/course_pronos_page_1.html')
	wait = ui.WebDriverWait(br,5)
	file_pronos = codecs.open('../02 - Page Web/course_pronos_page_1.html', 'r','utf-8')

	topFlag=0;
	ligneEnreg=""
	for line in file_pronos:
		# recherche du debut de la zone cible*
		if re.search(r'<ol class="pager">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</ol>', line) and topFlag==1:
			topFlag=0

	nbPage=re.findall(r'.*?((<li)(.*?)(</li>))', ligneEnreg)

	for k in range(len(nbPage)-1):
		index=k+2
		print("//ol//li["+str(index)+"]")
		br.find_element_by_xpath("//ol//li["+str(index)+"]").click()
		wait = ui.WebDriverWait(br,5)
		
		time.sleep(2)

		wait = ui.WebDriverWait(br,5)
		soup=BeautifulSoup(br.page_source,'lxml')
		writeFile(soup.prettify(),'../02 - Page Web/course_pronos_page_'+str(index)+'.html')
	
	
	br.quit()
	return file.read() , file_pronos.read()

