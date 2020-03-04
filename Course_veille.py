from Package.downloadWebPMU import *
from Package.coursePMU import *
from Package.classmentTrueskill import *
from Package.recalculTps import *
import codecs
import datetime
import os
from Package.coursePMU_Rapport import *

def recupere_Resulat_Course_Veille():
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	date_veille=datetime.date.today()+ datetime.timedelta(-1)
	date_veille_formate=date_veille.strftime('%d%m%Y')

	cursor.execute(""" select URL from COURSE where DATE='""" + date_veille_formate +"""' order by url """)
	rows = cursor.fetchall()

	for i in range(0,len(rows)):	
		url=rows[i][0]
		print(url)
		file_rapport=downloadWebPMUCourseV2(url)
		course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')
		participantResultatV2(url,course)		
		calculTrueskill(url)
		initialiseTrueskill_Driver(url)
		calculTrueskill_Driver(url)
		recalculTpsEcartPrec(url)
		recalculTpsRedKm(url)
		#os.remove('../02 - Page Web/'+row[0].replace('/','_')+'.html')

		courseRapport(url,file_rapport)



def recupere_Resulat_Course_Veille_date(date_veille_formate):
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 



	cursor.execute(""" select URL from COURSE where DATE='""" + date_veille_formate +"""' order by url """)
	rows = cursor.fetchall()

	for i in range(0,len(rows)):	
		url=rows[i][0]
		print(url)
		file_rapport=downloadWebPMUCourseV2(url)
		course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')
		participantResultatV2(url,course)		
		calculTrueskill(url)
		initialiseTrueskill_Driver(url)
		calculTrueskill_Driver(url)
		recalculTpsEcartPrec(url)
		recalculTpsRedKm(url)
		#os.remove('../02 - Page Web/'+row[0].replace('/','_')+'.html')

		courseRapport(url,file_rapport)

