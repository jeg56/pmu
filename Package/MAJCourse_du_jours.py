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

def MAJCourse_du_jours():
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	query = (	"select url,heure_depart " 
				"from COURSE " 
				"where date=strftime('%d%m%Y',  date('now','0 day')) " 
				"order by url " )
	print(query)
	cursor.execute (query)
	rows = cursor.fetchall()	

	for row in rows: 
#		if (row[0][:20]!='courses/09012018/R4/'):
#			continue 
		
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
			downloadWebPMUCourseV3(row[0])
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
				if re.search(r'<td class="participants-tbody-td participants-tbody-td--rapport-probable-first', line):
					topFlagProbaFirst=1

				if topFlagProbaFirst==1:
					ligneEnregProbaFirst+=line.strip()

				if re.search(r'</td>', line) and topFlagProbaFirst==1:
					topFlagProbaFirst=0
					if(ligneEnregProbaFirst.split('>')[1].split('<')[0]!='-'):
						champs_rapport1.append(ligneEnregProbaFirst.split('>')[1].split('<')[0].replace(',','.').replace('-',''))
						ligneEnregProbaFirst=''


				#-------------------------------------------------------------------------------------------------------------
				if re.search(r'<td class="participants-tbody-td participants-tbody-td--rapport-probable-last', line):
					topFlagProbaLast=1

				if topFlagProbaLast==1:
					ligneEnregProbaLast+=line.strip()

				if re.search(r'</td>', line) and topFlagProbaLast==1:
					topFlagProbaLast=0
					champs_rapport2.append(ligneEnregProbaLast.split('<div>')[0].replace(',','.').replace('</div></td>','').replace('<td class="participants-tbody-td participants-tbody-td--rapport-probable-last"><div class="participants-tbody-td--rapport-probable-cote">','').replace('<td class="participants-tbody-td participants-tbody-td--rapport-probable-last txtS"><div class="participants-tbody-td--rapport-probable-cote">','').replace('</div><div class="participants-tbody-td--rapport-probable-tendance"><i class="icon-fading"></i>','').replace('</div><div class="participants-tbody-td--rapport-probable-tendance"><i class="icon-rising"></i>','').replace('-',''))
					ligneEnregProbaLast=''

			listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', ligneEnreg)

			for i in range(len(champs_rapport1)):
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
			cursor = connnexion.cursor()

			for j in range(len(listPronosEquidia)):
				if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>',''):
					query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
						(j+1,row[0],listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>','')) )
					print(query)
					cursor.execute(query)
					connnexion.commit()



	#-------------------------------------------------------------------------------------------------------------
	# Gestion des pronos
	#-------------------------------------------------------------------------------------------------------------
	#-------------------------------------------------------------------------------------------------------------
		topFlag=0
		topFlagPronos=0
		ligneEnregPronos=""
		ligneEnreg=""
		champs=[]
		champs_PronosEquidia=[]
		champs_pronos=[]
		participant={}
		listParticipant=[]
		champs_Pronos=[]
		topFlagPronosNbPage=0
		ligneEnregPronosNbPage=""
		pagePronos = codecs.open('../02 - Page Web/course_pronos_page_1.html', 'r','utf-8')

		for line in pagePronos:
			# recherche du debut de la zone cible*
			if re.search(r'<ul class="course-infos-pronostic-list">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'</ul>', line) and topFlag==1:
				topFlag=0
			#-----------------------------------------------------------------------------------
			# recherche du debut de la zone cible*
			if re.search(r'<div class="expand-layout--pronostics pronostics-details">', line):
				topFlagPronos=1

			if topFlagPronos==1:
				ligneEnregPronos+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlagPronos==1:
				topFlagPronos=0

			#-----------------------------------------------------------------------------------
			# recherche du debut de la zone cible*
			if re.search(r'<ol class="pager">', line):
				topFlagPronosNbPage=1

			if topFlagPronosNbPage==1:
				ligneEnregPronosNbPage+=line.strip()

			if re.search(r'</ol>', line) and topFlagPronosNbPage==1:
				topFlagPronosNbPage=0

			
		#----------------------------------------------------------------------------------------------------------
		#----------------------------------------------------------------------------------------------------------
		#On récupère les infos 	
		url=row[0]
		listPronosEquidia=ligneEnreg.split('</li>')
		cursor = connnexion.cursor()
		DATE_COURSE=str(url[12:16]+'-'+url[10:12]+'-'+url[8:10])
		for j in range(len(listPronosEquidia)):	
			if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>',''):
				query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
					(j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>','')) )
				print(query)
				cursor.execute(query)
				connnexion.commit()

				query = ('UPDATE PRONOS SET DATE_COURSE="%s" ,PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
					(DATE_COURSE,j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>','')) )
				print(query)
				cursor.execute(query)
				connnexion.commit()
		print("----------------------------------------------------------------------------------------------")
		print("----------------------------------------------------------------------------------------------")
		print("----------------------------------------------------------------------------------------------")

		listPronos=re.findall(r'.*?((<table>)(.*?)(</table>))', ligneEnregPronos)
		topFlagProbaLast=0
		#-------------------------------------------------------------------------------------------------------------
		if re.search(r'<table>', line):
			topFlagProbaLast=1

		if topFlagProbaLast==1:
			ligneEnregProbaLast+=line.strip()

		if re.search(r'</table>', line) and topFlagProbaLast==1:
			topFlagProbaLast=0
			champs_rapport2.append(ligneEnregProbaLast.split('<div>')[1].split('</div>')[0].replace(',','.').replace('-',''))
			ligneEnregProbaLast=''

		for k in range(len(listPronos)):	
			champs_EnteteTableau=[]
			champs_nomPronostiqueurs=[]
			champs_avisNumero=[]
			champs_avisNom=[]

			EnteteTableau=re.findall(r'.*?((<caption>)(.*?)(</caption>))', str(listPronos[k][0]))
			for L in range(len(EnteteTableau)):
				if len(EnteteTableau)!=0 and EnteteTableau[L][2] !='LES FAVORIS' and EnteteTableau[L][2] !='LES OUTSIDERS' and EnteteTableau[L][2] !='LES DÉLAISSÉS' :
					champs_EnteteTableau.append(EnteteTableau[L][2])
					


			nomPronostiqueurs=re.findall(r'.*?((<th colspan="2">)(.*?)(<))', str(listPronos[k][0]))
			for L in range(len(nomPronostiqueurs)):
				if len(nomPronostiqueurs)!=0:
					champs_nomPronostiqueurs.append(nomPronostiqueurs[L][2])
				else:
					champs_nomPronostiqueurs.append('')
		


			avis=re.findall(r'.*?((<tr class=")(.*?)(</tr>))', str(listPronos[k][0]))
			for L in range(len(avis)):
				champs_avisNumero.append(avis[L][0].split('<td>')[1].replace('</td>',''))
				champs_avisNom.append(avis[L][0].split('<td>')[2].replace('</td>','').replace('</tr>',''))


			if len(champs_nomPronostiqueurs)!=0:
				pronostiqueur=reTraiteInfos(champs_EnteteTableau[0])+'_'+reTraiteInfos(champs_nomPronostiqueurs[0])
			for L in range(len(champs_avisNom)):
				query = ('UPDATE PRONOS SET %s=%s WHERE URL = "%s" and NUMERO = %s and upper(NOM)=upper("%s") '  % 
					(pronostiqueur,L+1,url,reTraiteInfos(champs_avisNumero[L]), reTraiteInfos(champs_avisNom[L])))
				print(query)
				cursor.execute(query)
				connnexion.commit()


		nbPage=re.findall(r'.*?((<li)(.*?)(</li>))', ligneEnregPronosNbPage)
		print('----------------------------'+str(len(nbPage)))

		for k in range(len(nbPage)-1):
			print('----------------------------/!\\'+str(len(nbPage)))
			index=k+2
			pagePronos = codecs.open('../02 - Page Web/course_pronos_page_'+str(index)+'.html', 'r','utf-8')
			print('course_pronos_page_'+str(index)+'.html')
			topFlagPronos=0
			ligneEnregPronos=''
			for line in pagePronos:
				#-----------------------------------------------------------------------------------
				# recherche du debut de la zone cible*
				if re.search(r'<div class="carousel-avis-slideshow-container">', line):
					topFlagPronos=1

				if topFlagPronos==1:
					ligneEnregPronos+=line.strip()

				if re.search(r'</figure>', line) and topFlagPronos==1:
					topFlagPronos=0

			

			listPronos=re.findall(r'.*?((<table>)(.*?)(</table>))', ligneEnregPronos)

			for k in range(len(listPronos)):
				champs_EnteteTableau=[]
				champs_nomPronostiqueurs=[]
				champs_avisNumero=[]
				champs_avisNom=[]

				EnteteTableau=re.findall(r'.*?((<caption>)(.*?)(</caption>))', str(listPronos[k][0]))
				for L in range(len(EnteteTableau)):
					if len(EnteteTableau)!=0 and EnteteTableau[L][2] !='LES FAVORIS' and EnteteTableau[L][2] !='LES OUTSIDERS' and EnteteTableau[L][2] !='LES DÉLAISSÉS' :
						champs_EnteteTableau.append(EnteteTableau[L][2])
				print('champs_EnteteTableau : '+str(champs_EnteteTableau))

				nomPronostiqueurs=re.findall(r'.*?((<th colspan="2">)(.*?)(<))', str(listPronos[k][0]))
				for L in range(len(nomPronostiqueurs)):
					if len(nomPronostiqueurs)!=0:
						champs_nomPronostiqueurs.append(nomPronostiqueurs[L][2])
					else:
						champs_nomPronostiqueurs.append('')
				print('champs_nomPronostiqueurs'+str(champs_nomPronostiqueurs))
				
				avis=re.findall(r'.*?((<tr class=")(.*?)(</tr>))', str(listPronos[k][0]))
				for L in range(len(avis)):
					champs_avisNumero.append(avis[L][0].split('<td>')[1].replace('</td>',''))
					champs_avisNom.append(avis[L][0].split('<td>')[2].replace('</td>','').replace('</tr>',''))
				print('champs_avisNom ' + str(champs_avisNom))
				
				
				for L in range(len(champs_avisNom)):
					pronostiqueur=reTraiteInfos(champs_EnteteTableau[0])+'_'+reTraiteInfos(champs_nomPronostiqueurs[0])
					query = ('UPDATE PRONOS SET %s=%s WHERE URL = "%s" and NUMERO = %s and upper(NOM)=upper("%s") '  % 
						(pronostiqueur,L+1,url,reTraiteInfos(champs_avisNumero[L]), reTraiteInfos(champs_avisNom[L])))
					print(query)
					cursor.execute(query)
					connnexion.commit()
