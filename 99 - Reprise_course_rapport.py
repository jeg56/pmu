from Package.downloadWebPMU import *
from Package.classmentTrueskill import *
from Package.coursePMU import *
from Package.alimBDD import *
import codecs
import datetime
import os
from reporting import *
import sqlite3
import numpy as np

import pandas as pd
from pandas_confusion import ConfusionMatrix

from Package.coursePMU_Rapport import *


#----------------------------------------------------------------------------------------------------------
#Connexion a la base de données
try:
	connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
except:
	print ('une erreur est survenue lors de la connection de la base')
	exit(1)
#----------------------------------------------------------------------------------------------------------

cursor = connnexion.cursor() 
query=( "select distinct url "
"from PRONOS "
"where (DATE_COURSE<'2017-11-26' or (DATE_COURSE='2017-11-26' and url >='courses/26112017/R2/C6'))  "
" order by DATE_COURSE desc") 

cursor.execute(	query )

rows = cursor.fetchall()

for row in rows:
	print(row[0])
	file_rapport={}
	file_rapport=downloadWebPMURapport(row[0])


#	file_rapport['SIMPLE'] = codecs.open('../02 - Page Web/rapport_SIMPLE.html', 'r','utf-8')
#	file_rapport['COUPLE']= codecs.open('../02 - Page Web/rapport_COUPLE.html', 'r','utf-8')
#	file_rapport['COUPLE_ORDRE']= codecs.open('../02 - Page Web/rapport_COUPLE_ORDRE.html', 'r','utf-8')
#	file_rapport['TRIO']= codecs.open('../02 - Page Web/rapport_TRIO.html', 'r','utf-8')
#	file_rapport['DEUX_SUR_QUATRE']= codecs.open('../02 - Page Web/rapport_DEUX_SUR_QUATRE.html', 'r','utf-8')
#	file_rapport['MULTI']= codecs.open('../02 - Page Web/rapport_MULTI.html', 'r','utf-8')
#	file_rapport['MINI_MULTI']= codecs.open('../02 - Page Web/rapport_MULTI.html', 'r','utf-8')
#	file_rapport['TIERCE']= codecs.open('../02 - Page Web/rapport_TIERCE.html', 'r','utf-8')
#	file_rapport['QUARTE_PLUS']= codecs.open('../02 - Page Web/rapport_QUARTE_PLUS.html', 'r','utf-8')
#	file_rapport['QUINTE_PLUS']= codecs.open('../02 - Page Web/rapport_QUINTE_PLUS.html', 'r','utf-8')

	courseRapport(row[0],file_rapport)



	
