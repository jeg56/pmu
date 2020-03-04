from Package.downloadWebPMU import *
from Package.classmentTrueskill import *
import codecs
import datetime
import os
from Package.coursePMU import *
from reporting import *
from Course_veille import *
from Course_a_venir import *

#----------------------------------------------------------------------------------------------------------
#Connexion a la base de données
try:
	connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
except:
	print ('une erreur est survenue lors de la connection de la base')
	exit(1)
#----------------------------------------------------------------------------------------------------------

cursor = connnexion.cursor() 
query=( "select  distinct url "
" from participant "
" where driver is null") 

cursor.execute(	query )

rows = cursor.fetchall()

for row in rows:
	print(row[0])
	downloadWebPMUCourseV2(row[0])
	course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')

	topFlag=0
	ligneEnreg=""
	champs_num=[]
	champs_name=[]
	champs_sex=[]
	champs_driver=[]

	for line in course:
    	# recherche du debut de la zone cible
		if re.search(r'<table class="participants-table participants-table--arrivee-definitive">', line):
			topFlag=1

		if topFlag==1:
			ligneEnreg+=line.strip()

		if re.search(r'</table>', line) and topFlag==1:
			topFlag=0

	listParticipant=re.findall(r'.*?((<tr class="participants-tbody-tr)(.*?)(</tr>))', ligneEnreg)

	for j in range(len(listParticipant)):
		#On recupere le n° du cheval
		#print(listParticipant[j])    
		listNum=re.findall(r'.*?((<span class="participants-num">)(.*?)(</span>))', str(listParticipant[j]))
		champs_num.append(listNum[0][2].replace(' title=','').replace('"',''))
	    
		listName=re.findall(r'.*?((<p class="participants-name")(.*?)(>))', str(listParticipant[j]))
		champs_name.append(listName[0][2].replace(' title=','').replace('"',''))

		listDriver=re.findall(r'.*?((<span class="participants-driver)(.*?)(>))', str(listParticipant[j]))
		if listDriver :
			champs_driver.append(listDriver[0][2].replace(' title=','').replace('"',''))
		else:
			listDriver=re.findall(r'.*?((<span class="participants-jokey)(.*?)(>))', str(listParticipant[j]))
			if listDriver :
				champs_driver.append(listDriver[0][2].replace(' title=','').replace('"',''))
			else :
				champs_driver.append('')

	for j in range(len(listParticipant)):
		print(str(champs_num[j])+'-'+str(champs_name[j])+'-'+str(champs_driver[j]))

		query = ('UPDATE PARTICIPANT SET DRIVER="%s" WHERE URL = "%s" and NUMERO = %s' % 
				(reTraiteInfos(champs_driver[j]),row[0],champs_num[j]))

		print(query)
		cursor.execute(query)
		connnexion.commit()
