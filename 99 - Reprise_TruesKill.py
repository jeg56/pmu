from Package.downloadWebPMU import *
from Package.classmentTrueskill import *
import codecs
import datetime
import os
from Package.coursePMU import *
from reporting import *
from Course_veille import *
from Course_a_venir import *



def calculRapport(url):
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
			"from PARTICIPANT "
			"where url ='"+url+"'")

	cursor.execute(	query )
	rows = cursor.fetchall()
	prono=0
	for row in rows:
		query2=( "select url,numero,nom,MU_AVANT,case when PRONO_EQUIDIA is null then 'null' else PRONO_EQUIDIA end as PRONO_EQUIDIA, "
				"case when FINISHER is null then '' else FINISHER end as FINISHER "
				"from PARTICIPANT "
				"where url = '"+str(row[0])+"'  "
				"order by url,MU_AVANT desc ")

		cursor.execute(	query2 )
		rows2 = cursor.fetchall()
		prono=0
		
		DATE_COURSE=str(url[12:16]+'-'+url[10:12]+'-'+url[8:10])
		for row2 in rows2:
			prono+=1
			queryUpdate =("update PARTICIPANT "
						"set PRONO_TRUESKILL= "+str(prono)+" "
						"where URL= '"+str(row2[0])+"' "
						"and  NUMERO="+str(row2[1])+" " 
						"and  NOM='"+str(row2[2])+"' ")
			connnexion.execute(queryUpdate)
			connnexion.commit()

			queryUpdate =("update PRONOS "
						"set DATE_COURSE='"+str(DATE_COURSE)+"' , PRONO_TRUESKILL= "+str(prono)+",PRONO_EQUIDIA="+str(row2[4])+", FINISHER='"+str(row2[5])+"' "
						"where URL= '"+str(row2[0])+"' "
						"and  NUMERO="+str(row2[1])+" " 
						"and  NOM='"+str(row2[2])+"' ")
			print(queryUpdate)

			connnexion.execute(queryUpdate)
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
query=( "select distinct A.url "
" from COURSE A, "
" participant B "
" where A.URL=B.URL and A.ETAT is null and ( MU_AVANT IS NULL or A.URL like 'courses/20012018/R1/C3' )"
" order by date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) ") 

print(query)

cursor.execute(	query )

rows = cursor.fetchall()
	
for row in rows:
	print(row[0])
	initialiseTrueskill(row[0])
	calculTrueskill(row[0])
	print('******************************')
	initialiseTrueskill_Driver(row[0])
	calculTrueskill_Driver(row[0])
	calculRapport(row[0])
	print('******************************')

	recalculTpsEcartPrec(row[0])
	recalculTpsRedKm(row[0])
	