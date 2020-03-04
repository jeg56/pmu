import re
from Package.manageFile import *
import lxml.html
import time
import sqlite3
import datetime

def listeCoursePMU(pagePMU):
	# récupération des éléments de course
	numCourse=-1
	course={}
	 
	for line in pagePMU:
    # recheche du debut de la zone cible
	    if re.search(r'timeline-course-link', line):
	        getCourse = re.split('"', line)
	        numCourse+=1
	        nomCourse = reTraiteInfos(str(getCourse[5][7:]))
	        dateCourse = reTraiteInfos(str(getCourse[3][8:16]))
	        cheminCourse = reTraiteInfos(str(getCourse[3]))
	        #InfoCourse nom de la course/ chemin de la course / 
	        infosCourse = [nomCourse,
	                    dateCourse,
	                    cheminCourse]
	        course[numCourse]=infosCourse
	return course

def infosCourseAVenir(pagePMU):
	# récupération des éléments de course
	numCourse=0
	course={}
	topFlag =-1
	topFlagHeure=-1
	topFlag2=-1
	ligneEnreg=""
	ligneEnregHeure=""
	extract_split=""
	 
	for line in pagePMU:
    # recherche du debut de la zone cible
		if re.search(r'<header class="course-infos-header">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</header>', line) and topFlag==1:
			#print (ligneEnreg)
			topFlag=0
			extract=re.search(r'.*?(<p>.*?<span class="boost-region course-infos-header-boosters-list")', ligneEnreg).group(1)
			extract2=extract.replace('</b>','¤').replace('<b>','¤').replace('|','¤').replace('<span','¤')
			extract_split=extract2.split('¤')
			course = [extract_split[1],extract_split[4],extract_split[6],extract_split[7]]

		# ----------------------------------------------------------------------------------------------------------------------#

		if re.search(r'<div class="course-infos-meteo">', line):
			topFlag2=1
			ligneEnreg=""

		if topFlag2==1:
			ligneEnreg+=line.strip()

		if re.search(r'</p>', line) and topFlag2==1:
			#print('--------------')
			#print (ligneEnreg)
			extract_meteo=ligneEnreg.split('"')

			topFlag2=0
			extract=re.search(r'.*?(</span>.*?</p>)', ligneEnreg).group(1)
			#print('---'+extract)
			extract2=extract.replace('</span>','').replace('</p>','').replace('vent ','')

			extract_split=extract2.split(',')
			#print(extract_split)
			course.append(extract_meteo[3])
			course.append(extract_meteo[5])
			course.append(extract_split[0])
			course.append(extract_split[1])
			
		# ----------------------------------------------------------------------------------------------------------------------#

		if re.search(r'<span class="icon-clock">', line):
			topFlagHeure=1

		if topFlagHeure==1:
			ligneEnregHeure+=line.strip()

		if re.search(r'</p>', line) and topFlagHeure==1:
			#print (ligneEnreg)
			topFlagHeure=0
			extract=re.search(r'.*?(</span>.*?</p>)', ligneEnregHeure).group(1)
			extract3=extract.replace('</span>','').replace('</p>','')
			course.append(extract3)

		# ----------------------------------------------------------------------------------------------------------------------#

	return course




def participantCourseAVenir(url,pagePMU, pagePronos):
	topFlag=0
	ligneEnreg=""
	champs=[]
	champs_num=[]
	champs_name=[]
	champs_sex=[]
	participant={}
	listParticipant=[]

	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	connnexion.execute("delete from PARTICIPANT where URL='{0}'".format(url))
	connnexion.commit()

	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------

	for line in pagePMU:
    # recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--a-partir">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0

	#On récupère les champs du tableaux
	if re.search(r'<th class="participants-thead-th participants-thead-th', ligneEnreg):
		listColonne=re.findall(r'.*?((<th class="participants-thead-th participants-thead-th.*?>)(.*?)(>))', ligneEnreg)
		for i in range(len(listColonne)):
			if (len(listColonne[i][2].split('"'))==3):
				champs.append(listColonne[i][2].split('"')[1])
	
	#On récupère le nombre de cheval			
	listNum=re.findall(r'.*?((<span class="participants-num">)(.*?)(</span>))', ligneEnreg)
	for j in range(len(listNum)):
		champs_num.append(listNum[j][2])
	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------


	#On alimente ces champs
	listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', ligneEnreg)


	for i in range(len(champs_num)):
		participant['NUMERO']=i+1
		participant['URL']=url			
		participant['NOM']=reTraiteInfos(listName[i][2].split('"')[1])

		#alimentation dans la BDD du participant
		colums = ", ".join(participant.keys())
		placeholders = ':'+', :'.join(participant.keys())
		query = "INSERT INTO PARTICIPANT (%s) VALUES (%s)" % (colums,placeholders)
		print(participant)
		cursor.execute(query, participant)
		connnexion.commit()



#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------
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

	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------

	#On récupère les infos 	
	listPronosEquidia=ligneEnreg.split('</li>')
	cursor = connnexion.cursor()

	for j in range(len(listPronosEquidia)):
		if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>',''):
			query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
				(j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>','')) )
			print(query)
			cursor.execute(query)
			connnexion.commit()











def participantResultat(url,pagePMU):
	topFlag=0
	ligneEnreg=""
	champs=[]
	champs_num=[]
	champs_name=[]
	champs_finisher=[]
	champs_sex=[]
	participant={}
	listParticipant=[]

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
	for line in pagePMU:
	# recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--arrivee-definitive">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0

	#On récupère les champs du tableaux
	listColonne=re.findall(r'.*?((<th class="participants-thead-th participants-thead-th--place .*?>)(.*?)(>))', ligneEnreg)
	for i in range(len(listColonne)):
		if (len(listColonne[i][2].split('"'))==3):
			champs.append(listColonne[i][2].split('"')[1])



	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------

	#On récupère les infos 	
	listNum=re.findall(r'.*?((<span class="participants-num">)(.*?)(</span>))', ligneEnreg)	
	listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', ligneEnreg)
	listFinisher=re.findall(r'.*?((<span class="participants-place">)(.*?)(</span>))', ligneEnreg)

	for j in range(len(listNum)):
		champs_num.append(listNum[j][2])
		champs_name.append(reTraiteInfos(listName[j][2].split('"')[1]))
		
		if(j<len(listFinisher)):
			champs_finisher.append(listFinisher[j][2].split('<sup>')[0])
		else:
			champs_finisher.append('-')
		
		

	#On alimente ces champs

	for i in range(len(champs_num)):
		participant['PLACE']=i+1
		participant['URL']=url			
		participant['NOM']=str(champs_name[i])
		participant['FINISHER']=str(champs_finisher[i])

		#alimentation dans la BDD du participant
		query = ('UPDATE PARTICIPANT SET PLACE=%s ,FINISHER="%s" WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
					(participant['PLACE'],participant['FINISHER'],url,participant['NOM']) )
		print(query)
		
		cursor.execute(query)
		connnexion.commit()
			


#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------



def participantResultatV2(url,pagePMU):
	topFlag=0
	topFlag_TpsCourse=0
	topFlagProbaFirst=0
	topFlagProbaLast=0
	ligneEnreg=""
	ligneEnreg_TpsCourse=""
	champs=[]
	champs_num=[]
	champs_name=[]
	entete_variable=[]
	champs_finisher=[]
	champs_sex=[]
	participant={}
	listParticipant=[]
	listReducKilo=[]
	champs_tps=[]

	champs_ecartPrec=[]

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
	for line in pagePMU:
		if re.search(r'<p class="participants-arrivee-temps-value">', line):
			topFlag_TpsCourse=1

		if topFlag_TpsCourse==1:
			ligneEnreg_TpsCourse+=line.strip()

		if re.search(r'</p>', line) and topFlag_TpsCourse==1:
			topFlag_TpsCourse=0
			print('Tps:' + str(ligneEnreg_TpsCourse.split('>')[1].split('<')[0]))
			if (ligneEnreg_TpsCourse.split('>')[1].split('<')[0]=='-'):
				x = datetime.datetime.strptime("0'0'0","%M'%S'%f")
			else:
				x = datetime.datetime.strptime(ligneEnreg_TpsCourse.split('>')[1].split('<')[0],"%M'%S"'"%f')
			TpsCourse=x.minute*60+x.second+x.microsecond/1000000
			query="UPDATE COURSE SET TPS_COURSE=%s WHERE URL='%s'" % (TpsCourse,url)
			print(query)
			cursor.execute(query)
			connnexion.commit()




	# recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--arrivee-definitive">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0


	#On récupère les champs du tableaux
		
	listColonne=re.findall(r'.*?((<th.*?>)(.*?)(</th>))', ligneEnreg)
	
	for j in range(len(listColonne)):	
		if(str(listColonne[j]).split('>')[1][:1]!="<"):
			champs=str(listColonne[j]).split('>')
			entete_variable.append(champs[1].replace('</th','').replace('<br',''))

	print(entete_variable)
	
	for j in range(len(entete_variable)):
		if(entete_variable[j]=='Red. Km'):
			listReducKilo=re.findall(r'.*?((<td class="participants-tbody-td center">)(.*?)(</td>))', ligneEnreg)
			
			for k in range(len(listReducKilo)):
				if(listReducKilo[k][2]=='-'):
					champs_tps.append(-1)
				else:
					x = datetime.datetime.strptime(listReducKilo[k][2],"%M'%S"'"%f')
					champs_tps.append(x.minute*60+x.second+x.microsecond/1000000)

		if(entete_variable[j]=='Ecart prèc.'):
			listEcartPrec=re.findall(r'.*?((<td class="participants-tbody-td center">)(.*?)(</td>))', ligneEnreg)
			for k in range(len(listEcartPrec)):
				if(listEcartPrec[k][2]==''):
					champs_ecartPrec.append('')
				else:
					champs_ecartPrec.append(listEcartPrec[k][2])


	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------

	#On récupère les infos 	
	listNum=re.findall(r'.*?((<span class="participants-num">)(.*?)(</span>))', ligneEnreg)	
	listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', ligneEnreg)
	listFinisher=re.findall(r'.*?((<span class="participants-place">)(.*?)(</span>))', ligneEnreg)

	for j in range(len(listNum)):
		champs_num.append(listNum[j][2])
		champs_name.append(reTraiteInfos(listName[j][2].split('"')[1]))
		
		if(j<len(listFinisher)):
			champs_finisher.append(listFinisher[j][2].split('<sup>')[0])
		else:
			champs_finisher.append('-')
		
		

	#On alimente ces champs

	for i in range(len(champs_num)):
		participant['PLACE']=i+1	
		participant['NOM']=str(champs_name[i])
		participant['FINISHER']=str(champs_finisher[i])
		

		#alimentation dans la BDD du participant
		query = ('UPDATE PARTICIPANT SET PLACE=%s ,FINISHER="%s" WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
					(participant['PLACE'],participant['FINISHER'],url,participant['NOM']) )

		print(query)

		cursor.execute(query)
		connnexion.commit()

	print('-------------------------------------------------')
	print(entete_variable)
	print('-------------------------------------------------')

	for j in range(len(entete_variable)):
		if(entete_variable[j]=='Red. Km'):
			for i in range(len(champs_tps)):
				participant['NOM']=str(champs_name[i])
				participant['TEMPS']=champs_tps[i]
				#alimentation dans la BDD du participant
				query = ('UPDATE PARTICIPANT SET TEMPS=%s WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
							(participant['TEMPS'],url,participant['NOM']) )

				print(query)

				cursor.execute(query)
				connnexion.commit()

		if(entete_variable[j]=='Ecart prèc.'):
			for i in range(len(champs_ecartPrec)):
				participant['NOM']=str(champs_name[i])
				participant['DISTANCE_PREC']=champs_ecartPrec[i]
				#alimentation dans la BDD du participant
				query = ('UPDATE PARTICIPANT SET DISTANCE_PREC="%s" WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
							(participant['DISTANCE_PREC'],url,participant['NOM']) )

				print(query)

				cursor.execute(query)
				connnexion.commit()

		if(len(entete_variable[j])==6 and j!=len(entete_variable)):
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
			if re.search(r'<td class="participants-tbody-td participants-tbody-td--rapport-probable-last">', line):
				topFlagProbaLast=1

			if topFlagProbaLast==1:
				ligneEnregProbaLast+=line.strip()

			if re.search(r'</td>', line) and topFlagProbaLast==1:
				topFlagProbaLast=0
				champs_rapport2.append(ligneEnregProbaLast.split('<div>')[1].split('</div>')[0].replace(',','.'))
				ligneEnregProbaLast=''


