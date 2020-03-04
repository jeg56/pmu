import re
from Package.manageFile import *
import lxml.html
import time
import sqlite3
import datetime
import codecs

def courseRapport(url,file_rapport):
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
	query = ("""UPDATE COURSE SET GAGNANT_SIMPLE=null, RAPPORT_GAGNANT=null,  PLACE_1=null, RAPPORT_PLACE_1=null, PLACE_2=null, RAPPORT_PLACE_2=null, PLACE_3=null, RAPPORT_PLACE_3=null, 
				GAGNANT_COUPLE=null, RAPPORT_COUPLE=null,  COUPLE_1=null, RAPPORT_COUPLE_1=null, COUPLE_2=null, RAPPORT_COUPLE_2=null, COUPLE_3=null, RAPPORT_COUPLE_3=null, 
				GAGNANT_MULTI=null, RAPPORT_MULTI_4=null, RAPPORT_MULTI_5=null, RAPPORT_MULTI_6=null, RAPPORT_MULTI_7=null,
				GAGNANT_TRIO=null, RAPPORT_TRIO=null,  
				RAPPORT_QUARTE_ORDRE=null, RAPPORT_QUARTE_DESORDRE=null, RAPPORT_QUARTE_BONUS=null, 
				GAGNANT_TRIO=null, RAPPORT_TRIO=null,  
				RAPPORT_QUARTE_ORDRE=null, RAPPORT_QUARTE_DESORDRE=null, RAPPORT_QUARTE_BONUS=null, 
				GAGNANT_QUINTE_ORDRE_TIRELIRE=null, RAPPORT_QUINTE_ORDRE_TIRELIRE=null, GAGNANT_QUINTE_ORDRE=null, RAPPORT_QUINTE_ORDRE=null,GAGNANT_QUINTE_DESORDRE=null,
					RAPPORT_QUINTE_DESORDRE=null,GAGNANT_QUINTE_BONUS_4sur5_1=null, RAPPORT_QUINTE_BONUS_4sur5_1=null, GAGNANT_QUINTE_BONUS_4sur5_2=null, 
					RAPPORT_QUINTE_BONUS_4sur5_2=null, GAGNANT_QUINTE_BONUS_4sur5_3=null, RAPPORT_QUINTE_BONUS_4sur5_3=null,GAGNANT_QUINTE_BONUS_4sur5_4=null, 
					RAPPORT_QUINTE_BONUS_4sur5_4=null,GAGNANT_QUINTE_BONUS_3=null, RAPPORT_QUINTE_BONUS_3=null, GAGNANT_QUINTE_BONUS=null, RAPPORT_QUINTE_BONUS=null  
			WHERE URL = '%s' """ % 
				(url) )

	cursor.execute(query)
	connnexion.commit()
	#----------------------------------------------------------------------------------------------------------
	#----------------------------------------------------------------------------------------------------------

	
	if(file_rapport['SIMPLE']!='' and file_rapport['SIMPLE_INTERNATIONAL']==''):
		topFlag =-1
		ligneEnreg=''
		for line in file_rapport['SIMPLE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
		print('------------- aaaaaaaaaaaaaaaaaaa ')
		print(ligneEnreg)		
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		print('*****')
		print(extractTR)
		print('-------------')
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  and re.search(r'Autres Chevaux', str(a)) == None:
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print(len(extract))

		GAGNANT_SIMPLE=extract[2].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_GAGNANT=extract[3].replace('<td>','').replace('</td>','').replace(' ','').replace('-','0')

		PLACE_1=extract[2].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_PLACE_1=extract[5].replace('<td>','').replace('</td>','').replace(' ','').replace('-','0')

		
		if(len(extract)!=7):
			PLACE_2=extract[7].replace('<td>','').replace('</td>','').replace(' ','').replace('-','0')
			RAPPORT_PLACE_2=extract[10].replace('<td>','').replace('</td>','').replace(' ','').replace('-','0')
		else:
			PLACE_2="-1"
			RAPPORT_PLACE_2='0'

		
	
		if(len(extract)!=12 and len(extract)!=7):
			PLACE_3=extract[12].replace('<td>','').replace('</td>','').replace(' ','')
			RAPPORT_PLACE_3=extract[15].replace('<td>','').replace('</td>','').replace(' ','').replace('-','0')
		else:
			PLACE_3="-1"
			RAPPORT_PLACE_3='0'
		
		print('Gagnant :' +str(GAGNANT_SIMPLE)+'-'+str(RAPPORT_GAGNANT))
		print('placé :' +str(PLACE_1)+'-'+str(RAPPORT_PLACE_1))
		print('placé :' +str(PLACE_2)+'-'+str(RAPPORT_PLACE_2))
		print('placé :' +str(PLACE_3)+'-'+str(RAPPORT_PLACE_3))

		query = ('UPDATE COURSE SET GAGNANT_SIMPLE=%s, RAPPORT_GAGNANT=%s,  PLACE_1=%s, RAPPORT_PLACE_1=%s, PLACE_2=%s, RAPPORT_PLACE_2=%s, PLACE_3=%s, RAPPORT_PLACE_3=%s WHERE URL = "%s" ' % 
					(GAGNANT_SIMPLE,RAPPORT_GAGNANT.replace(',','.').replace('€',''),
						PLACE_1,RAPPORT_PLACE_1.replace(',','.').replace('€',''),
						PLACE_2,RAPPORT_PLACE_2.replace(',','.').replace('€',''),
						PLACE_3,RAPPORT_PLACE_3.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	
	if(file_rapport['SIMPLE']=='' and file_rapport['SIMPLE_INTERNATIONAL']!='') :
		topFlag =-1
		ligneEnreg=''
		for line in file_rapport['SIMPLE_INTERNATIONAL']: 
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
				
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print(len(extract))

		GAGNANT_SIMPLE=extract[2].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_GAGNANT=extract[3].replace('<td>','').replace('</td>','').replace(' ','')

		PLACE_1=extract[2].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_PLACE_1=extract[5].replace('<td>','').replace('</td>','').replace(' ','')
		
		PLACE_2=extract[7].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_PLACE_2=extract[10].replace('<td>','').replace('</td>','').replace(' ','')
	
		if(len(extract)!=12):
			PLACE_3=extract[12].replace('<td>','').replace('</td>','').replace(' ','')
			RAPPORT_PLACE_3=extract[15].replace('<td>','').replace('</td>','').replace(' ','')
		else:
			PLACE_3="-1"
			RAPPORT_PLACE_3='0'
		
		print('Gagnant :' +str(GAGNANT_SIMPLE)+'-'+str(RAPPORT_GAGNANT))
		print('placé :' +str(PLACE_1)+'-'+str(RAPPORT_PLACE_1))
		print('placé :' +str(PLACE_2)+'-'+str(RAPPORT_PLACE_2))
		print('placé :' +str(PLACE_3)+'-'+str(RAPPORT_PLACE_3))

		query = ('UPDATE COURSE SET GAGNANT_SIMPLE=%s, RAPPORT_GAGNANT=%s,  PLACE_1=%s, RAPPORT_PLACE_1=%s, PLACE_2=%s, RAPPORT_PLACE_2=%s, PLACE_3=%s, RAPPORT_PLACE_3=%s WHERE URL = "%s" ' % 
					(GAGNANT_SIMPLE,RAPPORT_GAGNANT.replace(',','.').replace('€',''),
						PLACE_1,RAPPORT_PLACE_1.replace(',','.').replace('€',''),
						PLACE_2,RAPPORT_PLACE_2.replace(',','.').replace('€',''),
						PLACE_3,RAPPORT_PLACE_3.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	
	if(file_rapport['SIMPLE']!='' and file_rapport['SIMPLE_INTERNATIONAL']!=''):
		topFlag =-1
		ligneEnreg=''
		for line in file_rapport['SIMPLE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
				
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print(len(extract))

	
		PLACE_1=extract[1].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_PLACE_1=extract[2].replace('<td>','').replace('</td>','').replace(' ','')
		
		PLACE_2=extract[4].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_PLACE_2=extract[5].replace('<td>','').replace('</td>','').replace(' ','')


		print('placé :' +str(PLACE_1)+'-'+str(RAPPORT_PLACE_1))
		print('placé :' +str(PLACE_2)+'-'+str(RAPPORT_PLACE_2))

		query = ('UPDATE COURSE SET  PLACE_1=%s, RAPPORT_PLACE_1=%s, PLACE_2=%s, RAPPORT_PLACE_2=%s WHERE URL = "%s" ' % 
					(	PLACE_1,RAPPORT_PLACE_1.replace(',','.').replace('€',''),
						PLACE_2,RAPPORT_PLACE_2.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------


	if(file_rapport['SIMPLE_GAGNANT_INTERNATIONAL']!=''):
		topFlag =-1
		ligneEnreg=''
		for line in file_rapport['SIMPLE_GAGNANT_INTERNATIONAL']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1:
				ligneEnreg+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
				
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)


		GAGNANT_SIMPLE=extract[1].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_GAGNANT=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant SIMPLE_GAGNANT_INTERNATIONAL:' +str(GAGNANT_SIMPLE)+'-'+str(RAPPORT_GAGNANT))

		query = ('UPDATE COURSE SET GAGNANT_SIMPLE=%s, RAPPORT_GAGNANT=%s WHERE URL = "%s" ' % 
					(GAGNANT_SIMPLE,RAPPORT_GAGNANT.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------


	if(file_rapport['COUPLE']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['COUPLE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		print('---------------------------------------')
		print(ligneEnreg)
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		print('**************------------')
		print(extractTR)
		print('**************------------')
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print('---------------------------------------')
		GAGNANT_COUPLE=extract[2].replace('<td>','').replace('</td>','').replace(' ','').replace('AutresChevaux','-')
		RAPPORT_COUPLE=extract[3].replace('<td>','').replace('</td>','').replace(' ','').replace('Remboursé','0')

		COUPLE_1=extract[2].replace('<td>','').replace('</td>','').replace(' ','').replace('AutresChevaux','-')
		RAPPORT_COUPLE_1=extract[5].replace('<td>','').replace('</td>','').replace(' ','').replace('Remboursé','0')
		
		COUPLE_2=extract[7].replace('<td>','').replace('</td>','').replace(' ','').replace('AutresChevaux','-')
		RAPPORT_COUPLE_2=extract[10].replace('<td>','').replace('</td>','').replace(' ','').replace('Remboursé','0')

		COUPLE_3=extract[12].replace('<td>','').replace('</td>','').replace(' ','').replace('AutresChevaux','-')
		RAPPORT_COUPLE_3=extract[15].replace('<td>','').replace('</td>','').replace(' ','').replace('Remboursé','0')
		
		print('Gagnant COUPLE :' +str(GAGNANT_COUPLE)+'-'+str(RAPPORT_COUPLE))
		print('placé COUPLE 1 :' +str(COUPLE_1)+'-'+str(RAPPORT_COUPLE_1))
		print('placé COUPLE 2:' +str(COUPLE_2)+'-'+str(RAPPORT_COUPLE_2))
		print('placé COUPLE 3:' +str(COUPLE_3)+'-'+str(RAPPORT_COUPLE_3))

		query = ('UPDATE COURSE SET GAGNANT_COUPLE="%s", RAPPORT_COUPLE=%s,  COUPLE_1="%s", RAPPORT_COUPLE_1=%s, COUPLE_2="%s", RAPPORT_COUPLE_2=%s, COUPLE_3="%s", RAPPORT_COUPLE_3=%s WHERE URL = "%s" ' % 
					(GAGNANT_COUPLE,RAPPORT_COUPLE.replace(',','.').replace('€','').replace('-','0'),
						COUPLE_1,RAPPORT_COUPLE_1.replace(',','.').replace('€','').replace('-','0'),
						COUPLE_2,RAPPORT_COUPLE_2.replace(',','.').replace('€','').replace('-','0'),
						COUPLE_3,RAPPORT_COUPLE_3.replace(',','.').replace('€','').replace('-','0'),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	if(file_rapport['COUPLE_ORDRE']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['COUPLE_ORDRE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
		print('---------')
		print(ligneEnreg)
		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		print(extractTR)
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print('---------')
		GAGNANT_COUPLE_ORDRE=extract[1].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_COUPLE_ORDRE=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant COUPLE ORDRE :' +str(GAGNANT_COUPLE_ORDRE)+'-'+str(RAPPORT_COUPLE_ORDRE))


		query = ('UPDATE COURSE SET GAGNANT_COUPLE_ORDRE="%s", RAPPORT_COUPLE_ORDRE=%s WHERE URL = "%s" ' % 
					(GAGNANT_COUPLE_ORDRE,RAPPORT_COUPLE_ORDRE.replace(',','.').replace('€','').replace('-','0'),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	if(file_rapport['COUPLE_ORDRE_INTERNATIONAL']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['COUPLE_ORDRE_INTERNATIONAL']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)

		GAGNANT_COUPLE_ORDRE=extract[1].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_COUPLE_ORDRE=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant COUPLE ORDRE :' +str(GAGNANT_COUPLE_ORDRE)+'-'+str(RAPPORT_COUPLE_ORDRE))


		query = ('UPDATE COURSE SET GAGNANT_COUPLE_ORDRE="%s", RAPPORT_COUPLE_ORDRE=%s WHERE URL = "%s" ' % 
					(GAGNANT_COUPLE_ORDRE,RAPPORT_COUPLE_ORDRE.replace(',','.').replace('€','').replace('-','0'),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()



	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	if(file_rapport['TRIO_ORDRE']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['TRIO_ORDRE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)

		GAGNANT_TRIO=extract[1].replace('<td>','').replace('</td>','').replace(' ','')

		RAPPORT_TRIO=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant TRIO_ORDRE :' +str(GAGNANT_TRIO)+'-'+str(RAPPORT_TRIO))


		query = ('UPDATE COURSE SET GAGNANT_TRIO="%s", RAPPORT_TRIO=%s WHERE URL = "%s" ' % 
					(GAGNANT_TRIO,RAPPORT_TRIO.replace(',','.').replace('€','').replace('-','0'),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	if(file_rapport['TRIO_ORDRE_INTERNATIONAL']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['TRIO_ORDRE_INTERNATIONAL']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()

			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''

		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		#print(extract)

		GAGNANT_TRIO=extract[1].replace('<td>','').replace('</td>','').replace(' ','')

		RAPPORT_TRIO=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant TRIO_ORDRE_INTERNATIONAL :' +str(GAGNANT_TRIO)+'-'+str(RAPPORT_TRIO))


		query = ('UPDATE COURSE SET GAGNANT_TRIO="%s", RAPPORT_TRIO=%s WHERE URL = "%s" ' % 
					(GAGNANT_TRIO,RAPPORT_TRIO.replace(',','.').replace('€','').replace('-','0'),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	if(file_rapport['TRIO']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['TRIO']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		print('*************************')
		print(extractTR)
		print('*************************')
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None and re.search(r'<td>-</td>', str(a))== None :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		print('*************************')
		GAGNANT_TRIO=extract[1].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_TRIO=extract[2].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant TRIO :' +str(GAGNANT_TRIO)+'-'+str(RAPPORT_TRIO))


		query = ('UPDATE COURSE SET GAGNANT_TRIO="%s", RAPPORT_TRIO=%s WHERE URL = "%s" ' % 
					(GAGNANT_TRIO,RAPPORT_TRIO.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	if(file_rapport['DEUX_SUR_QUATRE']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['DEUX_SUR_QUATRE']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)

		RAPPORT_2sur4=extract[3].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant RAPPORT_2sur4 :' +str(RAPPORT_2sur4))


		query = ('UPDATE COURSE SET RAPPORT_2sur4="%s" WHERE URL = "%s" ' % 
					(RAPPORT_2sur4.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	if(file_rapport['MULTI']!=''):
		print('---------------------------------------------------------------------------------------------------------------')
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['MULTI']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0
		print('---------')
		print(ligneEnreg)

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		print(extractTR)
		print('---------')
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)

		GAGNANT_MULTI=extract[3].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_MULTI_4=extract[5].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_MULTI_5=extract[9].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_MULTI_6=extract[13].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_MULTI_7=extract[17].replace('<td>','').replace('</td>','').replace(' ','')

		
		print('Gagnant MULTI :' +str(GAGNANT_MULTI)+'-'+str(RAPPORT_MULTI_4)+'-'+str(RAPPORT_MULTI_5)+'-'+str(RAPPORT_MULTI_6)+'-'+str(RAPPORT_MULTI_7))


		query = ('UPDATE COURSE SET GAGNANT_MULTI="%s", RAPPORT_MULTI_4=%s, RAPPORT_MULTI_5=%s, RAPPORT_MULTI_6=%s, RAPPORT_MULTI_7=%s WHERE URL = "%s" ' % 
					(GAGNANT_MULTI,RAPPORT_MULTI_4.replace(',','.').replace('€',''),
						RAPPORT_MULTI_5.replace(',','.').replace('€',''),
						RAPPORT_MULTI_6.replace(',','.').replace('€',''),
						RAPPORT_MULTI_7.replace(',','.').replace('€',''),
						url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()
	print('---------------------------------------------------------------------------------------------------------------')
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	if(file_rapport['MINI_MULTI']!=''):
		print('---------------------------------------------------------------------------------------------------------------')
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['MINI_MULTI']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  and re.search(r'Remboursement', str(a))== None:
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)
		if (len(extract)>3):
			GAGNANT_MULTI=extract[3].replace('<td>','').replace('</td>','').replace(' ','')
			RAPPORT_MULTI_4=extract[5].replace('<td>','').replace('</td>','').replace(' ','')
			RAPPORT_MULTI_5=extract[9].replace('<td>','').replace('</td>','').replace(' ','')
			RAPPORT_MULTI_6=extract[13].replace('<td>','').replace('</td>','').replace(' ','')

			
			print('Gagnant MULTI :' +str(GAGNANT_MULTI)+'-'+str(RAPPORT_MULTI_4)+'-'+str(RAPPORT_MULTI_5)+'-'+str(RAPPORT_MULTI_6))


			query = ('UPDATE COURSE SET GAGNANT_MULTI="%s", RAPPORT_MULTI_4=%s, RAPPORT_MULTI_5=%s, RAPPORT_MULTI_6=%s WHERE URL = "%s" ' % 
						(GAGNANT_MULTI,RAPPORT_MULTI_4.replace(',','.').replace('€',''),
							RAPPORT_MULTI_5.replace(',','.').replace('€',''),
							RAPPORT_MULTI_6.replace(',','.').replace('€',''),
							url) )
		
			print(query)
			cursor.execute(query)
			connnexion.commit()
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------

	if(file_rapport['QUARTE_PLUS']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['QUARTE_PLUS']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)

		RAPPORT_QUARTE_ORDRE=extract[5].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUARTE_DESORDRE=extract[9].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUARTE_BONUS=extract[13].replace('<td>','').replace('</td>','').replace(' ','')
		
		
		print('Rapport QUARTE_PLUS :' +str(RAPPORT_QUARTE_ORDRE)+'-'+str(RAPPORT_QUARTE_DESORDRE)+'-'+str(RAPPORT_QUARTE_BONUS))


		query = ('UPDATE COURSE SET RAPPORT_QUARTE_ORDRE=%s, RAPPORT_QUARTE_DESORDRE=%s, RAPPORT_QUARTE_BONUS=%s  WHERE URL = "%s" ' % 
					(	RAPPORT_QUARTE_ORDRE.replace(',','.').replace('€',''),
						RAPPORT_QUARTE_DESORDRE.replace(',','.').replace('€',''),
						RAPPORT_QUARTE_BONUS.replace(',','.').replace('€',''),
							url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()

	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	#------------------------------------------------------------------------------------------------------------------------------------------
	if(file_rapport['QUINTE_PLUS']!=''):
		topFlag =-1
		ligneEnreg=''

		for line in file_rapport['QUINTE_PLUS']:
			if re.search(r'<div class="rapports-definitifs-table-picto-separator">', line):
				topFlag=1

			if topFlag==1 :
				ligneEnreg+=line.strip()


			if re.search(r'<div class="course-participants-region">', line) and topFlag==1:
				topFlag=0

		extractTR=re.findall(r'(<tr.*?</tr>)', ligneEnreg)
		extractPurge=''
		for a in extractTR:
			if re.search(r'NP', str(a)) == None and re.search(r'EC :', str(a)) == None  :
				extractPurge+=a

		extract=re.findall(r'.*?(<td>.*?</td>)', extractPurge)
		print(extract)

		GAGNANT_QUINTE_ORDRE_TIRELIRE=extract[3].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_ORDRE_TIRELIRE=extract[5].replace('<td>','').replace('</td>','').replace(' ','')

		GAGNANT_QUINTE_ORDRE=extract[7].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_ORDRE=extract[9].replace('<td>','').replace('</td>','').replace(' ','')		

		GAGNANT_QUINTE_DESORDRE=extract[11].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_DESORDRE=extract[13].replace('<td>','').replace('</td>','').replace(' ','')

		GAGNANT_QUINTE_BONUS=extract[15].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS=extract[17].replace('<td>','').replace('</td>','').replace(' ','')

		GAGNANT_QUINTE_BONUS_4sur5_1=extract[19].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS_4sur5_1=extract[21].replace('<td>','').replace('</td>','').replace(' ','')

		GAGNANT_QUINTE_BONUS_4sur5_2=extract[23].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS_4sur5_2=extract[25].replace('<td>','').replace('</td>','').replace(' ','')		

		GAGNANT_QUINTE_BONUS_4sur5_3=extract[27].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS_4sur5_3=extract[29].replace('<td>','').replace('</td>','').replace(' ','')	

		GAGNANT_QUINTE_BONUS_4sur5_4=extract[31].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS_4sur5_4=extract[33].replace('<td>','').replace('</td>','').replace(' ','')

		GAGNANT_QUINTE_BONUS_3=extract[35].replace('<td>','').replace('</td>','').replace(' ','')
		RAPPORT_QUINTE_BONUS_3=extract[37].replace('<td>','').replace('</td>','').replace(' ','')		

		query = ('UPDATE COURSE SET GAGNANT_QUINTE_ORDRE_TIRELIRE="%s", RAPPORT_QUINTE_ORDRE_TIRELIRE=%s, GAGNANT_QUINTE_ORDRE="%s", RAPPORT_QUINTE_ORDRE=%s,GAGNANT_QUINTE_DESORDRE="%s", RAPPORT_QUINTE_DESORDRE=%s,GAGNANT_QUINTE_BONUS_4sur5_1="%s", RAPPORT_QUINTE_BONUS_4sur5_1=%s, GAGNANT_QUINTE_BONUS_4sur5_2="%s", RAPPORT_QUINTE_BONUS_4sur5_2=%s, GAGNANT_QUINTE_BONUS_4sur5_3="%s", RAPPORT_QUINTE_BONUS_4sur5_3=%s,GAGNANT_QUINTE_BONUS_4sur5_4="%s", RAPPORT_QUINTE_BONUS_4sur5_4=%s,GAGNANT_QUINTE_BONUS_3="%s", RAPPORT_QUINTE_BONUS_3=%s, GAGNANT_QUINTE_BONUS="%s", RAPPORT_QUINTE_BONUS=%s WHERE URL = "%s" ' % 
					(	GAGNANT_QUINTE_ORDRE_TIRELIRE, RAPPORT_QUINTE_ORDRE_TIRELIRE.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_ORDRE, RAPPORT_QUINTE_ORDRE.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_DESORDRE,RAPPORT_QUINTE_DESORDRE.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS_4sur5_1, RAPPORT_QUINTE_BONUS_4sur5_1.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS_4sur5_2, RAPPORT_QUINTE_BONUS_4sur5_2.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS_4sur5_3, RAPPORT_QUINTE_BONUS_4sur5_3.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS_4sur5_4, RAPPORT_QUINTE_BONUS_4sur5_4.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS_3,RAPPORT_QUINTE_BONUS_3.replace(',','.').replace('€',''),
						GAGNANT_QUINTE_BONUS,RAPPORT_QUINTE_BONUS.replace(',','.').replace('€',''),
							url) )
	
		print(query)
		cursor.execute(query)
		connnexion.commit()






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
			extract=re.search(r'.*?(<strong>.*?<span class="boost-region course-infos-header-boosters-list")', ligneEnreg).group(1)
			extract2=extract.replace('<strong>','¤').replace('</strong>','¤').replace('</li>','¤').replace('<li>','¤')
			
			extract_split=extract2.split('¤')
			print(extract_split)
			#print(extract_split[1]) # Type de course
			#print(extract_split[5]) # GAIN
			#print(extract_split[8]) # Distance
			#print(extract_split[10]) #Nbre de partant

			#course = [extract_split[1],extract_split[3],extract_split[5],extract_split[7]]
			course = [extract_split[1],extract_split[5],extract_split[8],extract_split[10]]

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

