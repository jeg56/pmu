from __future__ import print_function
import sqlite3
import datetime
from Package.manageFile import *
import subprocess
import codecs
import Package.trueskill

def initialiseTrueskill(url):
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	query = (" Select TABLE1.URL, " 
				"TABLE1.NOM, " 
							"TABLE1.TYPE, " 
							"TABLE1.DATE_COURSE, " 
							"case when TABLE2.MU_APRES is null then '25' " 
							"	else TABLE2.MU_APRES end as MU_AVANT, " 
							"case when TABLE2.SIGMA_APRES is null then 8.333333 " 
							"	else TABLE2.SIGMA_APRES end as SIGMA_AVANT " 
					"From " 
							"( select A.URL,A.TYPE,B.NOM, " 
								"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
								"from COURSE A, " 
								"	PARTICIPANT B " 
								"where A.URL=B.URL AND	" 
								"	A.URL='" +url +"' " 
							") TABLE1 " 
					"left join " 
							"( select A.URL,A.TYPE,B.NOM,B.MU_APRES,B.SIGMA_APRES, " 
								"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
								"from COURSE A, " 
								"	PARTICIPANT B " 
								"where A.URL=B.URL And A.URL<>'" +url +"' and trim(B.Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','') "  
								"group by  A.URL,A.TYPE,B.NOM,B.MU_AVANT,B.SIGMA_AVANT " 
								"having max(date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) ) " 
							") TABLE2 " 
					"on 	TABLE1.NOM=TABLE2.NOM and " 
							"TABLE1.TYPE=TABLE2.TYPE And " 
							"TABLE1.DATE_COURSE>TABLE2.DATE_COURSE " 
					"order by TABLE1.URL,TABLE1.NOM,TABLE2.DATE_COURSE ||  substr(TABLE2.URL,length(TABLE2.URL),1)  ")
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print(query)
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')

	cursor.execute (query)
	rows = cursor.fetchall()
	for row in rows:
		queryUpdate =("update PARTICIPANT "
					"set MU_AVANT= '"+str(row[4])+"', " 
						"SIGMA_AVANT= '"+str(row[5])+"' "
					"where URL= '"+str(row[0])+"' And "
							"Nom= '"+str(row[1])+"' " )
		print(queryUpdate)
		connnexion.execute(queryUpdate)
		connnexion.commit()

		queryUpdate =("update PRONOS "
					"set MU= '"+str(row[4])+"' " 
					"where URL= '"+str(row[0])+"' And "
							"Nom= '"+str(row[1])+"' " )
		print(queryUpdate)
		connnexion.execute(queryUpdate)
		connnexion.commit()




	
	
def calculTrueskill(url):
	class Player(object):
		pass
	listPlayer=[]
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base: calculTrueskill')
		exit(1)
	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	query=(	"select NOM,PLACE,MU_AVANT,SIGMA_AVANT "
			"from PARTICIPANT "
			"where URL='"+url+"' and PLACE is not null "
			"and trim(Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','')" )
	cursor.execute(query)
	rows = cursor.fetchall()
	
	for ligne in rows:
		print(ligne)
		play =str(ligne[0])
		play = Player()
		play.skill = (ligne[2], ligne[3])
		play.rank = ligne[1]
		play.nom = ligne[0]
		play.url = url
		listPlayer.append(play)

	if len(rows)>1:
		Package.trueskill.AdjustPlayers(listPlayer)

		for play in listPlayer:
			updateSql=("update PARTICIPANT "
							"set MU_APRES={0[0]:.5f} , "
							"SIGMA_APRES={0[1]:.5f} "
						"where URL='{1}' and NOM='{2}' ".format(play.skill,play.url,play.nom))
			
			connnexion.execute(updateSql)
			connnexion.commit()

#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------


def initialiseTrueskill_Driver(url):
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	query = (" Select TABLE1.URL, " 
			"TABLE1.DRIVER, " 
						"TABLE1.TYPE, " 
						"TABLE1.DATE_COURSE, " 
						"case when TABLE2.MU_APRES_DRIVER is null then '25' " 
						"	else TABLE2.MU_APRES_DRIVER end as MU_AVANT_DRIVER, " 
						"case when TABLE2.SIGMA_APRES_DRIVER is null then 8.333333 " 
						"	else TABLE2.SIGMA_APRES_DRIVER end as SIGMA_AVANT_DRIVER " 
				"From " 
						"( select A.URL,A.TYPE,B.DRIVER, " 
							"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
							"from COURSE A, " 
							"	PARTICIPANT B " 
							"where A.URL=B.URL AND	" 
							"	A.URL='" +url +"' and B.DRIVER is not null and trim(B.DRIVER)<>'' " 
						") TABLE1 " 
				"left join " 
						"( select A.URL,A.TYPE,B.DRIVER,B.MU_APRES_DRIVER,B.SIGMA_APRES_DRIVER, " 
							"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
							"from COURSE A, " 
							"	PARTICIPANT B " 
							"where A.URL=B.URL And A.URL<>'" +url +"' and trim(B.Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','') "  
							"and B.DRIVER is not null "
							"group by A.TYPE,B.DRIVER,B.MU_APRES_DRIVER,B.SIGMA_APRES_DRIVER " 
							"having max(date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) ) " 
						") TABLE2 " 
				"on  TABLE1.DRIVER=TABLE2.DRIVER and TABLE1.TYPE=TABLE2.TYPE And TABLE1.DATE_COURSE|| substr(TABLE1.URL,length(TABLE1.URL),1)>=TABLE2.DATE_COURSE ||  substr(TABLE2.URL,length(TABLE2.URL),1) " 
				"order by TABLE1.URL,TABLE1.DRIVER,TABLE2.DATE_COURSE ||  substr(TABLE2.URL,length(TABLE2.URL),1) desc ")

	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print(query)
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')

	cursor.execute (query)
	rows = cursor.fetchall()
	driverPrec='Init'
	for row in rows:
		if driverPrec=='Init' or row[1]!=driverPrec:
			
			queryUpdate =("update PARTICIPANT "
					"set MU_AVANT_DRIVER= '"+str(row[4])+"', " 
						"SIGMA_AVANT_DRIVER= '"+str(row[5])+"' "
					"where URL= '"+str(row[0])+"' And "
							"DRIVER= '"+str(row[1])+"' " )
			driverPrec=row[1]
			print(queryUpdate)
			connnexion.execute(queryUpdate)
			connnexion.commit()
		else :
			driverPrec=row[1]
	connnexion.close()


def calculTrueskill_Driver(url):
	class Player(object):
		pass
	listPlayer=[]
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base : calculTrueskill_Driver')
		exit(1)
	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	cursor.execute(	"select DRIVER,PLACE,MU_AVANT_DRIVER,SIGMA_AVANT_DRIVER "
					"from PARTICIPANT "
					"where URL='"+url+"' and PLACE is not null and DRIVER is not null and trim(DRIVER)<>''  "
					"and trim(Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','')")
	rows = cursor.fetchall()
	
	for ligne in rows:
		print(ligne)
		play =str(ligne[0])
		play = Player()
		play.skill = (ligne[2], ligne[3])
		play.rank = ligne[1]
		play.DRIVER = ligne[0]
		play.url = url
		listPlayer.append(play)

	if len(rows)>1:
		Package.trueskill.AdjustPlayers(listPlayer)

		for play in listPlayer:
			updateSql=("update PARTICIPANT "
							"set MU_APRES_DRIVER={0[0]:.5f} , "
							"SIGMA_APRES_DRIVER={0[1]:.5f} "
						"where URL='{1}' and DRIVER='{2}' ".format(play.skill,play.url,play.DRIVER))

			print(updateSql)
			connnexion.execute(updateSql)
			connnexion.commit()
		connnexion.close()


#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------------------


def initialiseTrueskill_RG(url):
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 

	query = (" Select TABLE1.URL, " 
				"TABLE1.NOM, " 
							"TABLE1.TYPE, " 
							"TABLE1.DATE_COURSE, " 
							"case when TABLE2.MU_APRES is null then '25' " 
							"	else TABLE2.MU_APRES end as MU_AVANT, " 
							"case when TABLE2.SIGMA_APRES is null then 8.333333 " 
							"	else TABLE2.SIGMA_APRES end as SIGMA_AVANT " 
					"From " 
							"( select A.URL,A.TYPE,B.NOM, " 
								"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
								"from COURSE A, " 
								"	PARTICIPANT B " 
								"where A.URL=B.URL AND	" 
								"	A.URL='" +url +"' " 
							") TABLE1 " 
					"left join " 
							"( select A.URL,A.TYPE,B.NOM,B.MU_APRES,B.SIGMA_APRES, " 
								"date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) as DATE_COURSE " 
								"from COURSE A, " 
								"	PARTICIPANT B " 
								"where A.URL=B.URL And A.URL<>'" +url +"' and trim(B.Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','') "  
								"group by  A.URL,A.TYPE,B.NOM,B.MU_AVANT,B.SIGMA_AVANT " 
								"having max(date ( substr(A.DATE,length(A.DATE)-3,4) ||'-'||substr(A.DATE,length(A.DATE)-5,2) ||'-'|| substr(A.DATE,1,2) ) ) " 
							") TABLE2 " 
					"on 	TABLE1.NOM=TABLE2.NOM and " 
							"TABLE1.TYPE=TABLE2.TYPE And " 
							"TABLE1.DATE_COURSE>TABLE2.DATE_COURSE " 
					"order by TABLE1.URL,TABLE1.NOM,TABLE2.DATE_COURSE ||  substr(TABLE2.URL,length(TABLE2.URL),1)  ")
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print(query)
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')
	print('------------------------------------------------------------------------------------------------------')

	cursor.execute (query)
	rows = cursor.fetchall()
	for row in rows:
		queryUpdate =("update PARTICIPANT "
					"set MU_RG_AVANT= '"+str(row[4])+"', " 
						"SIGMA_RG_AVANT= '"+str(row[5])+"' "
					"where URL= '"+str(row[0])+"' And "
							"Nom= '"+str(row[1])+"' " )
		print(queryUpdate)
		connnexion.execute(queryUpdate)
		connnexion.commit()


