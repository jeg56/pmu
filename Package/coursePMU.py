import re
from Package.manageFile import *
import lxml.html
import time
import sqlite3
import datetime
import codecs

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

def listeCoursePMU2(pagePMU):
	ligneEnreg=''
	topFlag=0
	numReunion=0
	coursePrec=''

	# récupération des éléments de course
	numCourse=-1
	course={}
	listHippodrome=[]
	 
	for line in pagePMU:
		if re.search(r'.*?((<span class="hippodrome-libelle" title=")(.*?)(">))', line):
			hippo=re.search(r'.*?((<span class="hippodrome-libelle" title=")(.*?)(">))', line).group(1)
			listHippodrome.append(hippo.split('"')[3])
			print(listHippodrome)
		
		if re.search(r'timeline-course-link', line):
			getCourse = re.split('"', line)
			numCourse+=1
			nomCourse = reTraiteInfos(str(getCourse[5][7:]))
			dateCourse = reTraiteInfos(str(getCourse[3][8:16]))
			cheminCourse = reTraiteInfos(str(getCourse[3]))

			print(coursePrec+'-'+cheminCourse.split('/')[2])
			if (coursePrec!=cheminCourse.split('/')[2]):
				numReunion+=1
		
			#InfoCourse nom de la course/ chemin de la course / 
			infosCourse = [reTraiteInfos(listHippodrome[numReunion-1]),
						nomCourse,
			            dateCourse,
			            cheminCourse]
			course[numCourse]=infosCourse

			coursePrec=cheminCourse.split('/')[2]

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
			topFlag=0
			#extract=re.search(r'.*?(<p>.*?<span class="boost-region course-infos-header-boosters-list")', ligneEnreg).group(1)
			#extract2=extract.replace('</b>','¤').replace('<b>','¤').replace('|','¤').replace('<span','¤')
			print(ligneEnreg)
			extract=re.search(r'.*?(<ul class="course-infos-header-extras-main">.*?</ul>)', ligneEnreg).group(1)
			print(extract)

			extract2=extract.replace('<strong>','¤').replace('</strong>','¤').replace('</li>','¤').replace('<li>','¤')
			print(extract2)
			extract_split=extract2.split('¤')
			print(extract_split)
			print("Type de course "+ extract_split[2]) # Type de course
			print("Gain "+ extract_split[6]) # GAIN
			print("Distance "+ extract_split[9]) # Distance
			print("Nbre de partant "+ extract_split[11]) #Nbre de partant

			#course = [extract_split[1],extract_split[3],extract_split[5],extract_split[7]]
			course = [extract_split[2],extract_split[6],extract_split[9],extract_split[11]]

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
			print(ligneEnregHeure)
			extract=re.search(r'.*?(</span>.*?</p>)', ligneEnregHeure).group(1)
			print(extract)
			extract3=extract.replace('</span>','').replace('</p>','')
			print(extract3)
			course.append(extract3)

		if re.search(r'<span class="icon-flag-checkered">', line):
			course.append('00h00')
			

		# ----------------------------------------------------------------------------------------------------------------------#

	return course

def participantResultatV2(url,pagePMU):
	topFlag=0
	topFlag_TpsCourse=0
	ProbaFirst=0
	ligneEnreg=""
	ligneEnreg_TpsCourse=""
	champs=[]
	champs_num=[]
	champs_name=[]
	entete_variable=[]
	champs_finisher=[]
	champs_sex=[]
	champs_rapport1=[]
	champs_rapport2=[]
	champs_commentaire=[]
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
		if re.search(r'<span class="icon-course-annulee">', line):
			query="UPDATE COURSE SET ETAT='%s' WHERE URL='%s'" % ('Annulé',url)
			print(query)
			cursor.execute(query)
			connnexion.commit()

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
		#if(entete_variable[j]=='Jockey' or entete_variable[j]=='Driver'):
		#	listJokey=re.findall(r'.*?((<span class="participants-jokey)(.*?)(>))', ligneEnreg)
		#	print('------>>>>>>>>>'+str(listJokey))
		#	print('------>>>>>>>>>'+str(len(listJokey)))
		#	for k in range(len(listJokey)):
		#		print('------>>>>>>>>>'+str(listJokey[k][2].replace('" title="','').replace('','')))

		
		if(entete_variable[j][:12]=='Commentaires'):
			listCommentaire=re.findall(r'.*?((<td class="participants-tbody-td participants-tbody-td--commentaire">)(.*?)(</td>))', ligneEnreg)
			for k in range(len(listCommentaire)):
				print(listCommentaire[k][2])
				if(listCommentaire[k][2]==''):
					champs_commentaire.append('')
				else:
					champs_commentaire.append(listCommentaire[k][2])


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

		#-------------------------------------------------------------------------------------------------------------

		if(len(entete_variable[j])==6 and j!=len(entete_variable) and ProbaFirst!=1):
			listProbaFirst=re.findall(r'.*?((<td class="participants-tbody-td participants-tbody-td--rapport-probable-first">)(.*?)(</td>))', ligneEnreg)
			listProbaLast=re.findall(r'.*?((<div class="participants-tbody-td--rapport-probable-cote">)(.*?)(</td>))', ligneEnreg)

			ProbaFirst=1
			for k in range(len(listProbaFirst)):
				if(listProbaFirst[k][2]!='-'):
					champs_rapport1.append(listProbaFirst[k][2].replace(',','.'))
				else:
					champs_rapport1.append(-1)

				if(listProbaLast[k][2].replace('<div>','').replace('</div>','')!='-'):
					champs_rapport2.append(listProbaLast[k][2].replace('<div>','').replace('</div>','').replace(',','.'))
				else:
					champs_rapport2.append(-1)

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

		#alimentation dans la BDD du participant
		query = ('UPDATE PRONOS SET FINISHER="%s" WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
					(participant['FINISHER'],url,participant['NOM']) )

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
				participant['RED_KM']=champs_tps[i]
				#alimentation dans la BDD du participant
				query = ('UPDATE PARTICIPANT SET RED_KM=%s WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
							(participant['RED_KM'],url,participant['NOM']) )

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


		if(entete_variable[j][:12]=='Commentaires'):
			for i in range(len(champs_commentaire)):
				participant['NOM']=str(champs_name[i])
				participant['COMMENTAIRE']=champs_commentaire[i].replace('"',"'")
				#alimentation dans la BDD du participant
				query = ('UPDATE PARTICIPANT SET COMMENTAIRE="%s" WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
							(participant['COMMENTAIRE'],url,participant['NOM']) )

				print(query)

				cursor.execute(query)
				connnexion.commit()

		if(len(entete_variable[j])==6 and j<len(entete_variable)):
			for i in range(len(champs_rapport1)):
				participant['NOM']=str(champs_name[i])
				participant['RAPPORT1']=champs_rapport1[i]
				participant['RAPPORT2']=champs_rapport2[i]
				#alimentation dans la BDD du participant
				query = ('UPDATE PARTICIPANT SET RAPPORT1=%s, RAPPORT2=%s WHERE URL = "%s" and upper(NOM) = upper("%s")' % 
							(participant['RAPPORT1'],participant['RAPPORT2'],url,participant['NOM']) )

				print(query)

				cursor.execute(query)
				connnexion.commit()



def participantCourseAVenirV2(url):
	topFlag=0
	ligneEnreg=""
	champs=[]
	champs_num=[]
	champs_name=[]
	champs_sex=[]
	champs_driver=[]
	participant={}

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
	connnexion.execute("delete from PRONOS where URL='{0}'".format(url))
	connnexion.commit()

	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------
	pagePMU = codecs.open('../02 - Page Web/course.html', 'r','utf-8')

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
	listParticipant=re.findall(r'.*?((<tr class="participants-tbody-tr)(.*?)(</tr>))', ligneEnreg)
	for j in range(len(listParticipant)):
		#On recupere le n° du cheval
		#print(listParticipant[j])    
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

	for j in range(len(listParticipant)):
		print(str(champs_num[j])+'-'+str(reTraiteInfos(champs_name[j]))+'-'+str(champs_driver[j])) 
		participant['NUMERO']=champs_num[j]
		participant['URL']=url      
		participant['NOM']=reTraiteInfos(champs_name[j])
		participant['DRIVER']=reTraiteInfos(champs_driver[j])

		#alimentation dans la BDD du participant
		colums = ", ".join(participant.keys())
		placeholders = ':'+', :'.join(participant.keys())
		query = "INSERT INTO PARTICIPANT (%s) VALUES (%s)" % (colums,placeholders)
		print(query)
		cursor.execute(query, participant)
		connnexion.commit()

		#alimentation dans la BDD du participant
		colums = ", ".join(participant.keys())
		placeholders = ':'+', :'.join(participant.keys())
		query = "INSERT INTO PRONOS (%s) VALUES (%s)" % (colums,placeholders)
		print(query)
		cursor.execute(query, participant)
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
		listPronosEquidia=ligneEnreg.split('</li>')
		cursor = connnexion.cursor()
		DATE_COURSE=str(url[12:16]+'-'+url[10:12]+'-'+url[8:10])
		for j in range(len(listPronosEquidia)):	
			if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>',''):
				query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
					(j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>','')) )
				print(query)
				cursor.execute(query)
				connnexion.commit()

				query = ('UPDATE PRONOS SET DATE_COURSE="%s" ,PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
					(DATE_COURSE,j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li>','').replace('</ul>','')) )
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

#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------


def participantCourseAVenirV3(url):
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
	connnexion.execute("delete from PARTICIPANT where URL='{0}'".format(url))
	connnexion.commit()
	connnexion.execute("delete from PRONOS where URL='{0}'".format(url))
	connnexion.commit()

	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------
	pagePMU = codecs.open('../02 - Page Web/course.html', 'r','utf-8')

	for line in pagePMU:
		ligneFichier+=line.strip()
    # recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--a-partir">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0


	print('---------------------------------------------------------------------')
	#print(ligneEnreg)
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
		#print(listParticipant[j])    
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
				print('------'+str(listHandicap[7][2]))
				champs_handicap.append(listHandicap[7][2].replace('">','').replace('<','').replace('-','0').replace(',','.'))
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
				champs_poids_driver.append(listPoidsDriver[5][2].replace(' txtC">','').replace('<','').replace('-','0').replace(' participants-tbody-td--change',''))
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
				champs_poids_driver.append(temp[0].replace('">','').replace(' participants-tbody-td--change',''))
			else:
				champs_poids_driver.append('0')
	
			listHandicap=re.findall(r'.*?((<td class="participants-tbody-td)(.*?)(/td>))', str(listParticipant[j]))
			if listHandicap:
				temp=listHandicap[6][2].split('<br/>')
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0').replace(',','.'))
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
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0').replace(',','.'))
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
				champs_handicap.append(temp[0].replace('">','').replace('<','').replace('-','0').replace(',','.'))
			else:
				champs_handicap.append('0')

	print(listParticipant)
	for j in range(len(listParticipant)):
		participant['NUMERO']=champs_num[j]
		participant['URL']=url      
		participant['NOM']=reTraiteInfos(champs_name[j])
		participant['DRIVER']=reTraiteInfos(champs_driver[j])
		participant['ENTRAINEUR']=reTraiteInfos(champs_entraineur[j])
		participant['POIDS_DRIVER']=champs_poids_driver[j]
		participant['HANDICAP']=champs_handicap[j]

		#alimentation dans la BDD du participant
		colums = ", ".join(participant.keys())
		placeholders = ':'+', :'.join(participant.keys())
		query = "INSERT INTO PARTICIPANT (%s) VALUES (%s)" % (colums,placeholders)
		print(query)
		cursor.execute(query, participant)
		connnexion.commit()

		#alimentation dans la BDD du participant
		colums = ", ".join(participant.keys())
		placeholders = ':'+', :'.join(participant.keys())
		query = "INSERT INTO PRONOS (%s) VALUES (%s)" % (colums,placeholders)
		print(query)
		cursor.execute(query, participant)
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
		print('-------------------------------------------------------------------------------------------')
		print('-------------------------------------------------------------------------------------------')
		print('-------------------------------------------------------------------------------------------')
		for line in pagePronos:
			# recherche du debut de la zone cible*
			if re.search(r'<ul class="course-infos-pronostic-list">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()
				print(line.strip())

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
	listPronosEquidia=ligneEnreg.split('</li>')
	print('--------------')
	print(ligneEnreg)
	print('--------------')
	
	cursor = connnexion.cursor()
	DATE_COURSE=str(url[12:16]+'-'+url[10:12]+'-'+url[8:10])
	query = ('UPDATE PRONOS SET DATE_COURSE="%s" WHERE URL = "%s" ' % 
		(DATE_COURSE,url))
	cursor.execute(query)
	connnexion.commit()
	for j in range(len(listPronosEquidia)):	
		if listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>',''):
			query = ('UPDATE PARTICIPANT SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
				(j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>','')) )
			print(query)
			cursor.execute(query)
			connnexion.commit()

			query = ('UPDATE PRONOS SET PRONO_EQUIDIA=%s WHERE URL = "%s" and NUMERO = %s' % 
				(j+1,url,listPronosEquidia[j].replace('<ul class="course-infos-pronostic-list">','').replace('<li class="course-infos-pronostic-list-item">','').replace('<li>','').replace('</ul>','')) )
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

#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------