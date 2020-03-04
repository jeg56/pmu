import xlsxwriter
import sqlite3
import datetime
from Package.mail import *
from Package.manageFile import *
import matplotlib.pyplot as plt
import itertools
import pandas as pd
from PIL import Image

def course_a_potentiel(date):
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base : course_a_potentiel')
		exit(1)
	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	query=( "select A.url,B.heure_Depart,A.max_Course,A.min_Course,A.moy_Course,A.NB_CHEVAUX_PARTICIPANT "
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
			"course B where A.URL=B.URL order by A.NB_CHEVAUX_PARTICIPANT desc")
	print(query)
	cursor.execute(	query )
	
	rows = cursor.fetchall()

	workbook = xlsxwriter.Workbook('../05 - Documents/STATS/SELECT_'+date+'.xlsx')
	worksheet = workbook.add_worksheet()
	
	ligne=0
	worksheet.write(ligne, 0,'date')
	worksheet.write(ligne, 1,'url')
	worksheet.write(ligne, 2,'Course')
	worksheet.write(ligne, 3,'Heure')
	worksheet.write(ligne, 4,'Max prof calc')
	worksheet.write(ligne, 5,'Min prof calc (hors 1ere X)')
	worksheet.write(ligne, 6,'Moy prof calc')
	worksheet.write(ligne, 7,'Nb chev prof calc')

		# Add the standard url link format.
	url_format = workbook.add_format({
	    'font_color': 'blue',
	    'underline':  1
	})


	for row in rows:
		ligne+=1
		RC=str(row[0]).replace('/','_')[-5:]
		worksheet.write(ligne, 0,date)
		worksheet.write_string(ligne, 1,str(row[0]))
		lien=("internal:'%s'!A1" %(RC))
		worksheet.write_url(ligne, 2,lien,url_format,RC)
		worksheet.write(ligne, 3,str(row[1]))
		worksheet.write(ligne, 4,str(row[2]))
		worksheet.write(ligne, 5,str(row[3]))
		worksheet.write(ligne, 6,str(row[4]))
		worksheet.write(ligne, 7,str(row[5]))

	for j in range(len(rows)):
		cursor2 = connnexion.cursor() 
		query =("Select TEMP.TYPE,TEMP.URL,TEMP.GAIN,TEMP.DISTANCE, "
				"TEMP.NOM,TEMP.numero,TEMP.prono_equidia,TEMP.mu_avant,TEMP.mu_avant_driver,C.MOY_TEMPS,C.NB "
				"from "
				"(select A.Type, "
				"		A.url, "
				"		A.GAIN,A.DISTANCE, "
				"		B.NOM,B.numero,B.prono_equidia,B.mu_avant,B.mu_avant_driver "
				"from COURSE A, PARTICIPANT B "
				"where A.URL=B.URL and A.ETAT is null and  B.url='"+str(rows[j][0])+"'"
				") TEMP left join "
				"(select A.TYPE as TYPE,B.nom as NOM,count(*) as NB,avg(TEMPS) as MOY_TEMPS "
				"from COURSE A, PARTICIPANT B "
				"where A.URL=B.URL and A.ETAT is null and trim(B.Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','') and TEMPS<>-1 and TEMPS is not null "
				"group by A.TYPE,B.nom  "
				"union "
				"select A.TYPE as TYPE,B.nom as NOM,count(*) as NB,avg(TEMPS) as MOY_TEMPS "
				"from COURSE A, PARTICIPANT B "
				"where A.URL=B.URL and A.ETAT is null and trim(B.Finisher) not in ('-','DAI','DGP','Drb','Arr','Tbé','Di','Pot','NP','') and TEMPS is null "
				"group by A.TYPE,B.nom ) C "
				"on  TEMP.TYPE=C.TYPE  and TEMP.NOM=C.NOM "
				"order by TEMP.mu_avant desc")

		print('---->'+query)
		cursor2.execute(query )
		rows2 = cursor2.fetchall()

		worksheet = workbook.add_worksheet(str(rows[j][0].replace('/','_')[-5:]))
		
		ligne=0
		worksheet.write(ligne, 0,'TYPE')
		worksheet.write(ligne, 1,'URL')
		worksheet.write(ligne, 2,'GAIN')
		worksheet.write(ligne, 3,'DISTANCE')
		worksheet.write(ligne, 4,'NOM')
		worksheet.write(ligne, 5,'NUMERO')
		worksheet.write(ligne, 6,'PRONO EQUIDIA')
		worksheet.write(ligne, 7,'MU CHEVAL')
		worksheet.write(ligne, 8,'MU DRIVER')
		worksheet.write(ligne, 9,'MOYENNE TEMPS')
		worksheet.write(ligne, 10,'NB')

		for row2 in rows2:
			ligne+=1
			worksheet.write(ligne, 0,str(row2[0]))
			worksheet.write(ligne, 1,str(row2[1].replace('/','_')[-5:]))
			worksheet.write(ligne, 2,str(row2[2]))
			worksheet.write(ligne, 3,str(row2[3]))
			worksheet.write(ligne, 4,str(row2[4]))
			worksheet.write(ligne, 5,str(row2[5]))
			worksheet.write(ligne, 6,str(row2[6]))
			worksheet.write(ligne, 7,str(row2[7]))
			worksheet.write(ligne, 8,str(row2[8]))
			worksheet.write(ligne, 9,str(row2[9]))
			worksheet.write(ligne, 10,str(row2[10]))
			
		query=(" select COURSE_JOURS.URL,COURSE_JOURS.NUMERO||'-'||COURSE_JOURS.NOM,HISTO.DATE_COURSE,HISTO.MU_AVANT,HISTO.DISTANCE,HISTO.TEMPS,COURSE_JOURS.DISTANCE From "
			"(select URL,TYPE,NOM,NUMERO,DISTANCE "
			"from A_VERIF_PRONOS "
			"where URL='"+row2[1]+"' "
			") COURSE_JOURS, "
			"(select TYPE,NOM,DATE_COURSE,MU_AVANT,DISTANCE,TEMPS "
			"from A_VERIF_PRONOS "
			")HISTO "
		"Where COURSE_JOURS.TYPE=HISTO.TYPE and COURSE_JOURS.NOM=HISTO.NOM "
		"order by COURSE_JOURS.URL,COURSE_JOURS.NOM,HISTO.DISTANCE" )
		
		print(query)
		cursor.execute(query)
		rows3 = cursor.fetchall()

		if len(rows3)>0:
			marker=itertools.cycle(( 'o', '*','s'))

			val1=[]
			val2=[]
			val3=[]
			val4=[]
			val5=[]
			val6=[]
			i=0
			prec=''

			plt.close('all')

			fig = plt.figure()
			ax = fig.add_subplot(111)

			min=500
			max=0



			for row3 in rows3:
				if(row3[5] != None and min>row3[5] ):
						min=row3[5]
				if(row3[5] != None and max<row3[5]):
						max=row3[5]

				if i==0 or row3[1]==prec:
					url=row3[0]
					i=+1
					val1.append(row3[0])
					val2.append(row3[1])
					val3.append(row3[2])
					val4.append(row3[3])
					val5.append(row3[4])
					val6.append(row3[5])
					prec=row3[1]
				else :
					ax.plot(val5,val6,marker=next(marker),label=val2[0])
					val1=[]
					val2=[]
					val3=[]
					val4=[]
					val5=[]
					val6=[]
					
					val1.append(row3[0])
					val2.append(row3[1])
					val3.append(row3[2])
					val4.append(row3[3])
					val5.append(row3[4])
					val6.append(row3[5])

					prec=row3[1]

			ax.plot(val5,val6,marker=next(marker),label=val2[0])
			ax.plot([row3[6],row3[6]],[min,max],linestyle='--', color='red', linewidth=1)
			plt.title(url)
			ax.grid(True)
			plt.xlabel('Distance')
			plt.ylabel('Temps')

			ax.annotate('figure pixels',
			            xy=(2750,80), xycoords='figure pixels')


			plt.subplots_adjust(bottom=0.1, right=0.6, top=0.9)

			ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', ncol=1)
			#plt.show()
			plt.savefig('../05 - Documents/STATS/'+str(row3[0].replace('/','_')[-5:])+'.png')

			worksheet.insert_image('M1', '../05 - Documents/STATS/'+str(row3[0].replace('/','_')[-5:])+'.png')

	workbook.close()
	#mail2("Statistique PMU :Select "+date ,'STATS/SELECT_'+date+'.xlsx')
	dir = "../05 - Documents/STATS/"
	test=os.listdir(dir)
	
	for item in test:
	    if item.endswith(".png"):
	    	os.remove(str(dir+item))

	connnexion.close()	    	


	

def calculRapport(date):
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
			"where url like '%"+date+"%' ")

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
		DATE_COURSE=str(date[4:8]+'-'+date[2:4]+'-'+date[0:2])
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

			connnexion.execute(queryUpdate)
			connnexion.commit()




def AnalysePronos(date):
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
		query2=("select url, "
					"sum(trueskill_5) as trueskill_5, "
					"sum(trueskill_3) as trueskill_3, "
					"sum(trueskill) as trueskill, "
					"sum(equidia_5) as equidia_5, "
					"sum(equidia_3) as equidia_3, "
					"sum(equidia) as equidia "
				"from ( "
						"select url,numero,place,prono_equidia,prono_trueskill, "
						"case when prono_trueskill<=5 and place <= 5 then 1 else 0 end as trueskill_5, "
						"case when prono_trueskill<=3 and place <= 5 then 1 else 0 end as trueskill_3, "
						"case when prono_trueskill=place and place <= 3 then 1 else 0 end as trueskill, "
						"case when prono_equidia<=5 and place <= 5 then 1 else 0 end as equidia_5, "
						"case when prono_equidia<=3 and place <= 5 then 1 else 0 end as equidia_3, "
						"case when prono_equidia=place and place <= 3 then 1 else 0 end as equidia "
						"from participant "
						"where url ='"+str(row[0])+"' "
						"order by place  "
				") "
				)
		print (query2)
		cursor.execute(	query2 )
		rows2 = cursor.fetchall()
		for row2 in rows2:
			queryUpdate =("update COURSE "
						"set TRUESKILL_5= "+str(row2[1])+", "
						"	TRUESKILL_3= "+str(row2[2])+", "
						"	TRUESKILL= "+str(row2[3])+", "
						"	EQUIDIA_5= "+str(row2[4])+", "
						"	EQUIDIA_3= "+str(row2[5])+", "
						"	EQUIDIA= "+str(row2[6])+" "
						"where URL= '"+str(row2[0])+"' " )
			connnexion.execute(queryUpdate)
			connnexion.commit()


		# envoi stat descriptive
		cursor = connnexion.cursor() 
		query=( "select url, trueskill_5,trueskill_3,trueskill,equidia_5,equidia_3,equidia,Type,gain,distance,meteo_libelle,meteo_vent,meteo_temperature "
				"from course "
				"where url like '%"+date+"%' "
				"order by trueskill_5 desc") 

		cursor.execute(	query )
		rows = cursor.fetchall()

		
		workbook = xlsxwriter.Workbook('../05 - Documents/STATS/PRONOS_'+date+'.xlsx')

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
				"where url like '%"+date+"%' "
				"order by equidia_5 desc") 

		cursor.execute(	query )
		rows = cursor.fetchall()


	#--------------------------------------------------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------------------------------------------------
	#--------------------------------------------------------------------------------------------------------------------------

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
		"from PARTICIPANT where RAPPORT1 is not  null and URL like '%"+date+"%') A, "
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
		"where A.url=B.URL ")
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

	print(df_confusion)

	for z in range(6):
		worksheet.write(z+2,9,df_confusion.iloc[z,0],integer)
		worksheet.write(z+2,10,df_confusion.iloc[z,1],integer)
		worksheet.write(z+2,11,df_confusion.iloc[z,2],integer)
		worksheet.write(z+2,12,df_confusion.iloc[z,3],integer)
		worksheet.write(z+2,13,df_confusion.iloc[z,4],integer)
		worksheet.write(z+2,14,df_confusion.iloc[z,5],integer)


	workbook.close()
	#mail2("Statistique PMU : Pronos "+date ,'STATS/PRONOS_'+date+'.xlsx')

