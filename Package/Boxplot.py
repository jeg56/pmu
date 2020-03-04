import matplotlib.pyplot as plt
import numpy as np
import sqlite3


#----------------------------------------------------------------------------------------------------------
#Connexion a la base de données
try:
	connnexion = sqlite3.connect('../../03 - BDD/BasePMU.db')
except:
	print ('une erreur est survenue lors de la connection de la base : course_a_potentiel')
	exit(1)
#----------------------------------------------------------------------------------------------------------

cursor = connnexion.cursor() 
url='courses/01102017/R2/C4'
query=(" select COURSE_JOURS.URL,COURSE_JOURS.NUMERO||'-'||COURSE_JOURS.NOM,HISTO.DATE_COURSE,HISTO.MU_AVANT,HISTO.DISTANCE,HISTO.TEMPS,HISTO.VITESSE,COURSE_JOURS.DISTANCE From "
	"(select URL,TYPE,NOM,NUMERO,DISTANCE "
	"from A_VERIF_PRONOS "
	"where URL='"+url+"' "
	") COURSE_JOURS, "
	"(select TYPE,NOM,DATE_COURSE,MU_AVANT,DISTANCE,TEMPS,VITESSE "
	"from A_VERIF_PRONOS "
	")HISTO "
"Where COURSE_JOURS.TYPE=HISTO.TYPE and COURSE_JOURS.NOM=HISTO.NOM "
"and HISTO.VITESSE is not null "
"order by COURSE_JOURS.URL,COURSE_JOURS.NOM,HISTO.DISTANCE" )

cursor.execute(	query )
print(query)
rows= cursor.fetchall()

if len(rows)>0:
	data=[]
	val1=[]
	val2=[]
	val3=[]
	val4=[]
	val5=[]
	val6=[]
	val7=[]
	i=0
	prec=''

	min=500
	max=0
	for row in rows:
		if(min>row[5]):
				min=row[5]
		if(max<row[5]):
				max=row[5]

		if i==0 or row[1]==prec:
			url=row[0]
			i=+1
			val1.append(row[0])
			val2.append(row[1])
			val3.append(row[2])
			val4.append(row[3])
			val5.append(row[4])
			val6.append(row[5])
			val7.append(row[6])
			prec=row[1]
		else :
			val1=[]
			val2=[]
			val3=[]
			val4=[]
			val5=[]
			val6=[]
			val7=[]
			val1.append(row[0])
			val2.append(row[1])
			val3.append(row[2])
			val4.append(row[3])
			val5.append(row[4])
			val6.append(row[5])
			val7.append(row[6])
			data.append(val6)
			prec=row[1]


print(val5)
print(val6)



plt.figure()

plt.boxplot(data)

plt.show()