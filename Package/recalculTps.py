import codecs
import datetime
import os
from fractions import Fraction
import sqlite3
import re

def recalculTpsEcartPrec(URL):
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base : recalculTpsEcartPrec -' + er.message)
		exit(1)

	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	query=( "select distinct A.URL, cast(case when length(B.PLACE)=1 then '0'||B.PLACE else B.PLACE end as integer) as POSITION,A.TPS_COURSE,B.distance_prec,B.PLACE "
	"from course A, participant B "
	"where A.URL=B.URL and B.URL='"+URL+"' and (B.PLACE=1 or B.distance_prec <>'') "
	"order by  A.URL, POSITION ") 

	print(query)

	cursor.execute(query)
	rows = cursor.fetchall()


	if len(rows)>1 :
		for row in rows:

			ecart_Prec=row[3].replace(" de ", " ")
			if row[4]==1:
				Tps=row[2]
			elif re.search(r'longueur', ecart_Prec):
				if(len(ecart_Prec.split(' '))>2):
					Tps+=Fraction(ecart_Prec.split(' ')[0])*4+Fraction(ecart_Prec.split(' ')[2])
				else:
					Tps+=Fraction(ecart_Prec.split(' ')[0])*4
			elif re.search(r'nez', ecart_Prec):
				Tps+=0.1
			elif ecart_Prec=='Courte tête':
				Tps+=0.5
			elif re.search(r'tête', ecart_Prec):
				Tps+=1
			elif  ecart_Prec=='Courte encolure':
				Tps+=2
			elif ecart_Prec=='Encolure':
				Tps+=2
			elif  ecart_Prec=='Dead heat':
				Tps+=1
			elif ecart_Prec=='Loin':
				Tps+=44
			else:
				print('--------------------------------------------------------------------------------------------------------------------------------------------')
				mail('Erreur','Erreur ecart précédent')

			if row[2]== 0 :
				query = ("UPDATE PARTICIPANT SET TEMPS=%s WHERE URL = '%s' and PLACE = '%s' ;" % 
					(-1,row[0],row[4]))
			else :
				query = ("UPDATE PARTICIPANT SET TEMPS=%s WHERE URL = '%s' and PLACE = '%s' ;" % 
					(Tps,row[0],row[4]))

			print(query)
			cursor.execute(query)
			connnexion.commit()
		connnexion.close()



def recalculTpsRedKm(URL):
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base : recalculTpsRedKm -' + er.message)
		exit(1)

	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	query=( "select distinct B.NOM, B.NUMERO, "
		"case when B.RED_KM=-1 then 1000 else A.DISTANCE end as DISTANCE, B.RED_KM "
	"from course A, participant B "
	"where A.URL=B.URL and B.URL='"+URL+"' and B.RED_KM is not null ") 

	print(query)

	cursor.execute(query)
	rows = cursor.fetchall()

	if len(rows)>1 :
		for row in rows:
			query="update PARTICIPANT set TEMPS="+ str(row[2]*row[3]/1000) + " Where URL='"+URL+"' and NUMERO="+str(row[1])+" and upper(NOM) = upper('"+str(row[0])+"');"
			print(query)
			cursor.execute(query)
			connnexion.commit()
		connnexion.close()

