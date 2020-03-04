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
from Package.MAJCourse_du_jours import *

date_veille=datetime.date.today()+ datetime.timedelta(-1)
date=date_veille.strftime('%d%m%Y')

def TEST(date):
	listURL=('courses/03112017/R3/C5',
'courses/03112017/R3/C6',
'courses/03112017/R3/C7',
'courses/03112017/R5/C1',
'courses/03112017/R3/C8',
'courses/03112017/R4/C5',
'courses/03112017/R4/C6',
'courses/03112017/R4/C7',
'courses/03112017/R5/C6',
'courses/03112017/R5/C7',
'courses/03112017/R5/C8',
'courses/03112017/R1/C1',
'courses/03112017/R1/C2',
'courses/03112017/R1/C3',
'courses/03112017/R1/C4',
'courses/03112017/R1/C5',
'courses/03112017/R1/C7')

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
			"where url like '%"+str(date)+"%' ")
	
	cursor.execute(	query )
	rows = cursor.fetchall()
	prono=0




	for row in rows:
		# envoi stat descriptive
		cursor = connnexion.cursor() 
		query=( "select url, trueskill_5,trueskill_3,trueskill,equidia_5,equidia_3,equidia,Type,gain,distance,meteo_libelle,meteo_vent,meteo_temperature "
				"from course "
				"where url like '%"+date+"%' and url in "+str(listURL)+" "
				"order by trueskill_5 desc") 

		cursor.execute(	query )
		rows = cursor.fetchall()

		
		workbook = xlsxwriter.Workbook('../05 - Documents/STATS/PRONOS2_'+date+'.xlsx')

		# Add some cell formats.
		integer = workbook.add_format({'num_format': '0'})
		decimal = workbook.add_format({'num_format': '0.00'})
		percentage = workbook.add_format({'num_format': '0.0%'})

		worksheet = workbook.add_worksheet('Trueskill')
		
		ligne=0
		worksheet.write(ligne, 0,'url')
		worksheet.write(ligne, 1,'trueskill_5')
		worksheet.write(ligne, 2,'trueskill_3')
		worksheet.write(ligne, 3,'trueskill')
		worksheet.write(ligne, 4,'equidia_5')
		worksheet.write(ligne, 5,'equidia_3')
		worksheet.write(ligne, 6,'equidia')
		worksheet.write(ligne, 7,'Type')
		worksheet.write(ligne, 8,'gain')
		worksheet.write(ligne, 9,'distance')
		worksheet.write(ligne, 10,'meteo_libelle')
		worksheet.write(ligne, 11,'meteo_vent')
		worksheet.write(ligne, 12,'meteo_temperature')

		for row in rows:
			ligne+=1
			worksheet.write(ligne, 0,str(row[0].replace('/','_')[-5:]))
			worksheet.write(ligne, 1,row[1],integer)
			worksheet.write(ligne, 2,row[2],integer)
			worksheet.write(ligne, 3,row[3],integer)
			worksheet.write(ligne, 4,row[4],integer)
			worksheet.write(ligne, 5,row[5],integer)
			worksheet.write(ligne, 6,row[6],integer)
			worksheet.write(ligne, 7,str(row[7]))
			worksheet.write(ligne, 8,str(row[8]))
			worksheet.write(ligne, 9,str(row[9]))
			worksheet.write(ligne, 10,str(row[10]))
			worksheet.write(ligne, 11,str(row[11]))
			worksheet.write(ligne, 12,str(row[12]))

		ligne+=1
		worksheet.write(ligne, 1, '=SUM(B2:B'+str(ligne)+')')
		worksheet.write(ligne, 2, '=SUM(C2:C'+str(ligne)+')')
		worksheet.write(ligne, 3, '=SUM(D2:D'+str(ligne)+')')
		worksheet.write(ligne, 4, '=SUM(E2:E'+str(ligne)+')')
		worksheet.write(ligne, 5, '=SUM(F2:F'+str(ligne)+')')
		worksheet.write(ligne, 6, '=SUM(G2:G'+str(ligne)+')')

		ligne+=1
		worksheet.write(ligne, 2, 'NB si 1')
		worksheet.write(ligne, 3, '=COUNTIF(D2:D'+str(ligne-1)+',1)')
		worksheet.write(ligne, 6, '=COUNTIF(G2:G'+str(ligne-1)+',1)')
		ligne+=1
		worksheet.write(ligne, 2, 'NB si 2')
		worksheet.write(ligne, 3, '=COUNTIF(D2:D'+str(ligne-2)+',2)')
		worksheet.write(ligne, 6, '=COUNTIF(G2:G'+str(ligne-2)+',2)')
		ligne+=1
		worksheet.write(ligne, 2, 'NB si 3')
		worksheet.write(ligne, 3, '=COUNTIF(D2:D'+str(ligne-3)+',3)')
		worksheet.write(ligne, 6, '=COUNTIF(G2:G'+str(ligne-3)+',3)')


		cursor = connnexion.cursor() 
		query=( "select url, trueskill_5,trueskill_3,trueskill,equidia_5,equidia_3,equidia,Type,gain,distance,meteo_libelle,meteo_vent,meteo_temperature "
				"from course "
				"where url like '%"+date+"%' and url in "+str(listURL)+" "
				"order by equidia_5 desc") 

		cursor.execute(	query )
		rows = cursor.fetchall()

	worksheet = workbook.add_worksheet('Confusion')

	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except sqlite3.Error as er:
		print ('une erreur est survenue lors de la connection de la base' + er.message)
		exit(1)

	cursor = connnexion.cursor() 
	print('************************************************************************')
	query=("select A.PLACE, A.PRONO_EQUIDIA,A.PRONO_TRUESKILL, B.NB_CHEVAUX_PARTICIPANT "
		"From (select distinct URL, case when PLACE<=5 then PLACE  else '[Sup à 5]' end as PLACE, 	 case when PRONO_EQUIDIA<=5 then PRONO_EQUIDIA 	 else '[Sup à 5]' end as PRONO_EQUIDIA, 	case when PRONO_TRUESKILL<=5 then PRONO_TRUESKILL else '[Sup à 5]' end as PRONO_TRUESKILL "
		"from PARTICIPANT where trim(FINISHER) not in ('-','DAI','DGP','Arr','Tbé','Di','Pot','NP','') and URL like '%"+date+"%') A, "
		"(select A.url,B.heure_Depart,A.max_Course,A.min_Course,A.moy_Course,A.NB_CHEVAUX_PARTICIPANT as NB_CHEVAUX_PARTICIPANT "
		"from "
		"(select TMP.url,max(NB_COURSE_PARTICIPE) as max_Course,min(NB_COURSE_PARTICIPE) as min_Course,avg(NB_COURSE_PARTICIPE) as moy_Course,count(*) as NB_CHEVAUX_PARTICIPANT "
		" from ( 	Select A.nom,A.NB_COURSE_PARTICIPE,B.url "
					"From (	select A.nom,count(*) as NB_COURSE_PARTICIPE "
							"from participant A, "
							"	COURSE B "
							"where B.url=A.url "
							"group by A.nom, B.type "
							"having count(*)>1 ) A, "
					"participant B "
					"where A.nom=B.nom and B.url like '%"+date+"%' "
					" ) TMP "
					" group by TMP.url "
					" order by count(*) desc) A, "
		"course B where A.URL=B.URL order by A.NB_CHEVAUX_PARTICIPANT desc) B "
		"where A.url=B.URL and A.url in "+str(listURL)+"")
	print(query)
	cursor.execute(query)
	rows = cursor.fetchall()


	val1=[]
	val2=[]
	val3=[]

	for row in rows:
		val1.append(str(row[0]))
		val2.append(str(row[1]))
		val3.append(str(row[2]))

	PLACE=pd.Series(val1, name='réalité')
	Trueskill=pd.Series(val3, name='Trueskill')
	Equidia=pd.Series(val2, name='Equidia')
	df_confusion = pd.crosstab(PLACE, Trueskill)
	print(df_confusion)
	worksheet.write(0, 0,'Matrice de confusion')
	
	worksheet.write(1,0,'Réalité/Trueskill')
	worksheet.write(1,1,'1')	
	worksheet.write(1,2,'2')
	worksheet.write(1,3,'3')
	worksheet.write(1,4,'4')
	worksheet.write(1,5,'5')
	worksheet.write(1,6,']Sup à 5]')

	worksheet.write(2,0,'1')	
	worksheet.write(3,0,'2')
	worksheet.write(4,0,'3')
	worksheet.write(5,0,'4')
	worksheet.write(6,0,'5')
	worksheet.write(7,0,']Sup à 5]')


	for z in range(6):
		worksheet.write(z+2,1,df_confusion.iloc[z,0],integer)
		worksheet.write(z+2,2,df_confusion.iloc[z,1],integer)
		worksheet.write(z+2,3,df_confusion.iloc[z,2],integer)
		worksheet.write(z+2,4,df_confusion.iloc[z,3],integer)
		worksheet.write(z+2,5,df_confusion.iloc[z,4],integer)
		worksheet.write(z+2,6,df_confusion.iloc[z,5],integer)

	print('----------------------------------')

	df_confusion = pd.crosstab(PLACE, Equidia)
	
	worksheet.write(1,8,'Réalité/Equidia')
	worksheet.write(1,9,'1')	
	worksheet.write(1,10,'2')
	worksheet.write(1,11,'3')
	worksheet.write(1,12,'4')
	worksheet.write(1,13,'5')
	worksheet.write(1,14,']Sup à 5]')

	worksheet.write(2,8,'1')	
	worksheet.write(3,8,'2')
	worksheet.write(4,8,'3')
	worksheet.write(5,8,'4')
	worksheet.write(6,8,'5')
	worksheet.write(7,8,']Sup à 5]')

	for z in range(6):
		worksheet.write(z+2,9,df_confusion.iloc[z,0],integer)
		worksheet.write(z+2,10,df_confusion.iloc[z,1],integer)
		worksheet.write(z+2,11,df_confusion.iloc[z,2],integer)
		worksheet.write(z+2,12,df_confusion.iloc[z,3],integer)
		worksheet.write(z+2,13,df_confusion.iloc[z,4],integer)
		worksheet.write(z+2,14,df_confusion.iloc[z,5],integer)


	workbook.close()
	#mail2("Statistique PMU : Pronos "+date ,'STATS/PRONOS_'+date+'.xlsx')


TEST(date)