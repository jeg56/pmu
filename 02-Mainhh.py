import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import selenium.webdriver.support.ui as ui 
from bs4 import BeautifulSoup
import sqlite3

from datetime import datetime
import os
from Course_a_venir import *
from Course_veille import *
from Package.mail import *
import sys
from reporting import *


try:
	connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
except sqlite3.Error as er:
	print ('une erreur est survenue lors de la connection de la base' + er.message)
	exit(1)

cursor = connnexion.cursor() 

query = (	"select url,heure_depart " 
			"from COURSE " 
			"where date=strftime('%d%m%Y',  date('now','0 day') )  " 
			"order by url " )

cursor.execute (query)
rows = cursor.fetchall()

print(rows)

for row in rows:
	print(row[0])

	topFlagProbaFirst=-1
	topFlagProbaLast=-1
	topFlag=-1
	ligneEnregProbaFirst=""
	ligneEnregProbaLast=""
	ligneEnreg=""
	champs_name=[]
	champs_rapport1=[]
	champs_rapport2=[]
	participant={}



	if( (int(row[1][:2])*60 + int(row[1][3:])) >(int(datetime.datetime.now().strftime('%H'))*60  + int(datetime.datetime.now().strftime('%M'))  ) and
		(int(row[1][:2])*60 + int(row[1][3:])) < (int(datetime.datetime.now().strftime('%H'))*60  + int(datetime.datetime.now().strftime('%M')) +40 )
	 ) or 1==1:
		downloadWebPMUCourseV2(row[0])
		course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')
		
		#On alimente ces champs

		for line in course:
			if re.search(r'<table class="participants-table participants-table--a-partir">', line) or  re.search(r'<table class="participants-table participants-table--arrivee-definitive">', line) or re.search(r'<table class="participants-table participants-table--arrivee-provisoire">', line):           
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'</table>', line) and topFlag==1:
				topFlag=0

			#-------------------------------------------------------------------------------------------------------------			
			if re.search(r'<td class="participants-tbody-td participants-tbody-td--rapport-probable-first">', line):
				topFlagProbaFirst=1

			if topFlagProbaFirst==1:
				ligneEnregProbaFirst+=line.strip()

			if re.search(r'</td>', line) and topFlagProbaFirst==1:
				topFlagProbaFirst=0
				if(ligneEnregProbaFirst.split('>')[1].split('<')[0]!='-'):
					champs_rapport1.append(ligneEnregProbaFirst.split('>')[1].split('<')[0].replace(',','.'))
					ligneEnregProbaFirst=''


			#-------------------------------------------------------------------------------------------------------------
			if re.search(r'<td class="participants-tbody-td participants-tbody-td--rapport-probable-last', line):
				topFlagProbaLast=1

			if topFlagProbaLast==1:
				ligneEnregProbaLast+=line.strip()

			if re.search(r'</td>', line) and topFlagProbaLast==1:
				topFlagProbaLast=0
				champs_rapport2.append(ligneEnregProbaLast.split('<div>')[1].split('</div>')[0].replace(',','.'))
				ligneEnregProbaLast=''

		listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', ligneEnreg)
		print(ligneEnreg)
		print(listName)
		for i in range(len(champs_rapport1)):
			print(champs_rapport1[i])
			print(champs_rapport2[i])

			print(listName[i][2])
			print(row[0])
			print(reTraiteInfos(listName[i][2].split('"')[1]))
			#alimentation dans la BDD du participant
			query = ("UPDATE PARTICIPANT set RAPPORT1=%s, RAPPORT2=%s  WHERE URL='%s' and NOM='%s'" % 
				(champs_rapport1[i],champs_rapport2[i],row[0],reTraiteInfos(listName[i][2].split('"')[1])))
			print(query)
			cursor.execute(query)
			connnexion.commit()

		#----------------------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------------------

		pagePronos = codecs.open('../02 - Page Web/course_pronos.html', 'r','utf-8')
		topFlag=0
		ligneEnreg=""
		champs=[]
		champs_PronosEquidia=[]

		participant={}
		listParticipant=[]

		for line in pagePronos:
		# recherche du debut de la zone cible
			if re.search(r'<ul class="course-infos-pronostic-list">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'</ul>', line) and topFlag==1:
				topFlag=0


		#On récupère les infos 	

		listPronosEquidia=ligneEnreg.split('</li>')
		print(listPronosEquidia)
		cursor = connnexion.cursor()

		for j in range(len(listPronosEquidia)):
			if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>',''):
				query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
					(j+1,row[0],listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>','')) )
				print(query)
				cursor.execute(query)
				connnexion.commit()

		