import sqlite3

def alimCourseBDD1(data1,data2):
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base')
		exit(1)


	cursor = connnexion.cursor()
	print('data1'+str(data1))
	print('data2'+str(data2))

	connnexion.execute("delete from COURSE where URL='{0}'".format(data1[3]))
	print(len(data2))
	if(len(data2)==5):
		query=("insert into COURSE (HIPPODROME,NOM,DATE,URL,TYPE,GAIN,DISTANCE,NBRE_PARTANT,HEURE_DEPART) values ('{0}','{1}','{2}','{3}','{4}',{5},{6},{7},'{8}')"
		.format(data1[0],
			data1[1],
			data1[2],
			data1[3],
			data2[0],
			data2[1].replace(' ','').replace('€',''),
			data2[2].replace(' ','').replace('m',''),
			data2[3].replace(' ','').replace('partants',''),
			data2[4].replace(' ','').replace('Départ','')
			)
		)  
	else:
		query=("insert into COURSE (HIPPODROME,NOM,DATE,URL,TYPE,GAIN,DISTANCE,NBRE_PARTANT,HEURE_DEPART,METEO,METEO_LIBELLE,METEO_TEMPERATURE,METEO_VENT) values ('{0}','{1}','{2}','{3}','{4}',{5},{6},{7},'{8}','{9}','{10}',{11},{12})"
			.format(data1[0],
				data1[1],
				data1[2],
				data1[3],
				data2[0],
				data2[1].replace(' ','').replace('€',''),
				data2[2].replace(' ','').replace('m',''),
				data2[3].replace(' ','').replace('partants',''),
				data2[4].replace(' ','').replace('Départ',''),
				data2[5].replace(' ',''),
				data2[6].replace("'",'"'),
				data2[7].replace(' ','').replace('°C',''),
				data2[8].replace(' ','').replace('km/h','')
				)
			)  
	print(query)
	connnexion.execute(query) 
    # Sauvegarde
	connnexion.commit()




def alimCourseBDD(data1,data2):
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base')
		exit(1)


	cursor = connnexion.cursor()
	print('data1'+str(data1))
	print('data2'+str(data2))

	connnexion.execute("delete from COURSE where URL='{0}'".format(data1[2]))
	query=("insert into COURSE (NOM,DATE,URL,TYPE,GAIN,DISTANCE,NBRE_PARTANT,HEURE_DEPART,METEO,METEO_LIBELLE,METEO_TEMPERATURE,METEO_VENT) values ('{0}','{1}','{2}','{3}',{4},{5},{6},'{7}','{8}','{9}',{10},{11})"
		.format(data1[0],
			data1[1],
			data1[2],
			data2[0],
			data2[1].replace(' ','').replace('€',''),
			data2[2].replace(' ','').replace('m',''),
			data2[3].replace(' ','').replace('partants',''),
			data2[4].replace(' ','').replace('Départ',''),
			data2[5].replace(' ',''),
			data2[6].replace("'",'"'),
			data2[7].replace(' ','').replace('°C',''),
			data2[8].replace(' ','').replace('km/h','')
			)
		)  
	print(query)
	connnexion.execute(query) 
    # Sauvegarde
	connnexion.commit()


