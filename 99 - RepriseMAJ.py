# -*- coding: UTF8 -*-
from Package.downloadWebPMU import *
import sqlite3
from Package.coursePMU import *
from Package.classmentTrueskill import *
from Package.recalculTps import *
import codecs
import datetime
import os
from Package.coursePMU_Rapport import *

def participantCourseAVenirV3_reprise(url):

	topFlag=0
	ligneEnreg=""
	ligneFichier=''
	champs=[]
	champs_num=[]
	champs_name=[]
	champs_sex=[]
	champs_driver=[]
	champs_entraineur=[]
	champs_poids_driver=[]
	champs_handicap=[]
	
	participant={}

	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 


	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------
	pagePMU = codecs.open('../02 - Page Web/course.html', 'r','utf-8')

	for line in pagePMU:
		ligneFichier+=line.strip()
    # recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--arrivee-definitive">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0


	print('---------------------------------------------------------------------')
	print(ligneEnreg)
	print('---------------------------------------------------------------------')
	#On récupère les champs du tableaux
	if re.search(r'<th class="participants-thead-th participants-thead-th', ligneEnreg):
		listColonne=re.findall(r'.*?((<th class="participants-thead-th participants-thead-th.*?>)(.*?)(>))', ligneEnreg)
		for i in range(len(listColonne)):
			if (len(listColonne[i][2].split('"'))==3):
				champs.append(listColonne[i][2].split('"')[1])
	
	#On récupère le nombre de cheval			
	listParticipant=re.findall(r'.*?((<tr class="participants-tbody-tr)(.*?)(</tr>))', ligneEnreg)
	for j in range(len(listParticipant)):
		#On recupere le n° du cheval
		print('---------------------------------------------------------------------')
		print(listParticipant[j])    
		print('---------------------------------------------------------------------')
		listNum=re.findall(r'.*?((<span class="participants-num">)(.*?)(</span>))', str(listParticipant[j]))
		champs_num.append(listNum[0][2].replace(' title=','').replace('"',''))
	    
		listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', str(listParticipant[j]))
		champs_name.append(listName[0][2].replace(' title=','').replace('"',''))

		listDriver=re.findall(r'.*?((<span class="participants-driver ")(.*?)(>))', str(listParticipant[j]))
		if listDriver :
			champs_driver.append(listDriver[0][2].replace(' title=','').replace('"',''))
		else:
			listDriver=re.findall(r'.*?((<span class="participants-jokey ")(.*?)(>))', str(listParticipant[j]))
			if listDriver :
				champs_driver.append(listDriver[0][2].replace(' title=','').replace('"',''))
			else :
				champs_driver.append('')

		listEntraineur=re.findall(r'.*?((<span class="participants-entraineur")(.*?)(>))', str(listParticipant[j]))
		if listEntraineur :
			champs_entraineur.append(listEntraineur[0][2].replace(' title=','').replace('"',''))
		else:
			champs_entraineur.append('')



		if(re.search(r'<strong>Plat</strong>', str(ligneFichier))):
			listPoidsDriver=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listPoidsDriver :
				temp=listPoidsDriver[6][2].split('<br/>')
				champs_poids_driver.append(temp[0].replace('">','').replace('<',''))
			else:
				champs_poids_driver.append('0')
	
			listHandicap=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listHandicap:
				print('---////////////////////---'+str(listHandicap[7][2]))
				champs_handicap.append(listHandicap[7][2].replace('">','').replace('<','').replace('-','0'))
			else:
				champs_handicap.append('0')



		if(re.search(r'<strong>Trot Attelé</strong>', str(ligneFichier))):
			champs_poids_driver.append('0')
			champs_handicap.append('0')



		if(re.search(r'<strong>Trot Monté</strong>', str(ligneFichier))):
			listPoidsDriver=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			print('-------------------------**********************')
			print(listPoidsDriver)
			print('-------------------------')

			if listPoidsDriver :
				champs_poids_driver.append(listPoidsDriver[5][2].replace(' txtC">','').replace('<','').replace('-','0'))
			else:
				champs_poids_driver.append('0')
	
			champs_handicap.append('0')


		if(re.search(r'<strong>Obstacle Steeple</strong>', str(ligneFichier))):
			listPoidsDriver=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			print('-------------------------**********************')
			print(listPoidsDriver)
			print('-------------------------')
			if listPoidsDriver :
				temp=listPoidsDriver[5][2].split('<br/>')
				champs_poids_driver.append(temp[0].replace('">',''))
			else:
				champs_poids_driver.append('0')
	
			listHandicap=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listHandicap:
				temp=listHandicap[6][2].split('<br/>')
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0'))
			else:
				champs_handicap.append('0')

		if(re.search(r'<strong>Obstacle Haies</strong>', str(ligneFichier))):
			listPoidsDriver=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			print('-------------------------**********************')
			print(listPoidsDriver)
			print('-------------------------')
			if listPoidsDriver :
				temp=listPoidsDriver[5][2].split('<br/>')
				champs_poids_driver.append(temp[0].replace('">',''))
			else:
				champs_poids_driver.append('0')
	
			listHandicap=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listHandicap:
				temp=listHandicap[6][2].split('<br/>')
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0'))
			else:
				champs_handicap.append('0')

		if(re.search(r'<strong>Obstacle Cross</strong>', str(ligneFichier))):
			listPoidsDriver=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			print('-------------------------**********************')
			print(listPoidsDriver)
			print('-------------------------')
			if listPoidsDriver :
				temp=listPoidsDriver[5][2].split('<br/>')
				champs_poids_driver.append(temp[0].replace('">',''))
			else:
				champs_poids_driver.append('0')
	
			listHandicap=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listHandicap:
				temp=listHandicap[6][2].split('<br/>')
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0'))
			else:
				champs_handicap.append('0')


	for j in range(len(listParticipant)):
		participant['NUMERO']=champs_num[j]
		participant['URL']=url      
		participant['NOM']=reTraiteInfos(champs_name[j])
		participant['DRIVER']=reTraiteInfos(champs_driver[j])
		participant['ENTRAINEUR']=reTraiteInfos(champs_entraineur[j])
		participant['POIDS_DRIVER']=champs_poids_driver[j]
		participant['HANDICAP']=champs_handicap[j].replace(',','.')

		query = 'UPDATE PARTICIPANT SET ENTRAINEUR = ?, POIDS_DRIVER = ?, HANDICAP = ? WHERE URL = ? and NOM= ? and NUMERO=? '
		cursor.execute(query, (participant['ENTRAINEUR'], participant['POIDS_DRIVER'], participant['HANDICAP'],participant['URL'],participant['NOM'],participant['NUMERO']))
		connnexion.commit()

		query = 'UPDATE PRONOS SET ENTRAINEUR = ?, POIDS_DRIVER = ?, HANDICAP = ? WHERE URL = ? and NOM= ? and NUMERO=? '
		cursor.execute(query, (participant['ENTRAINEUR'], participant['POIDS_DRIVER'], participant['HANDICAP'],participant['URL'],participant['NOM'],participant['NUMERO']))
		connnexion.commit()

#----------------------------------------------------------------------------------------------------------
#Connexion a la base de données
try:
	connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
except:
	print ('une erreur est survenue lors de la connection de la base')
	exit(1)
#----------------------------------------------------------------------------------------------------------

cursor = connnexion.cursor() 
query=( "select distinct url from VERIF_PRONOS where POIDS_DRIVER like '%txt%'") 

print(query)
cursor.execute(	query )

rows = cursor.fetchall()

for i in range(0,len(rows)):	
	url=rows[i][0]
	course,pronos=downloadWebPMUCourseV3(url)
	course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')
	participantCourseAVenirV3_reprise(url)


