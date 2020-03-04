import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
import itertools

#----------------------------------------------------------------------------------------------------------
#Connexion a la base de données
try:
	connnexion = sqlite3.connect('../../03 - BDD/BasePMU.db')
except:
	print ('une erreur est survenue lors de la connection de la base : course_a_potentiel')
	exit(1)
#----------------------------------------------------------------------------------------------------------

fig = plt.figure()
ax = fig.gca(projection='3d')
marker=itertools.cycle(( 'o', '*','s'))

cursor = connnexion.cursor() 
url='courses/01102017/R2/C6'
query=(" select COURSE_JOURS.URL,COURSE_JOURS.NUMERO||'-'||COURSE_JOURS.NOM,round(julianday('now') - julianday(HISTO.DATE_COURSE)) ,HISTO.MU_AVANT,HISTO.DISTANCE,HISTO.TEMPS,HISTO.VITESSE,COURSE_JOURS.DISTANCE From "
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
			z = val5
			x = val3	
			y = val6
			print(str(x) +'-'+ str(y)+'-'+ str(z))			
			ax.plot(x, y, z, marker=next(marker),label=val2[0])
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

			prec=row[1]
mpl.rcParams['legend.fontsize'] = 10
#ax.plot([0,0],[row[7],row[7]],[min,max],linestyle='--', color='red', linewidth=3)
print(row[7])
plt.subplots_adjust(bottom=0.1, right=0.6, top=0.9)
ax.legend(bbox_to_anchor=(1.01, 1), loc='upper left', ncol=1)

ax.set_xlabel('Date course')
ax.set_ylabel('Temps')
ax.set_zlabel('Distance')
plt.show()
