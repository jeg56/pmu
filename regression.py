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

from sklearn.datasets import make_friedman1
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import summary_table
from matplotlib.pyplot import *
import math



def regression(url):
	
	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base : course_a_potentiel')
		exit(1)
	#----------------------------------------------------------------------------------------------------------
	connnexion.commit()
	cursor = connnexion.cursor() 
	query = ('UPDATE PRONOS SET NB_COURSE=null ,PRONO_REG_LINEAIRE=null,PRONO_TEMPS_REG_LINEAIRE=null WHERE URL = "%s"  ' %  (url))

	print(query)
	cursor.execute(query)
	connnexion.commit()
	#----------------------------------------------------------------------------------------------------------

	query=("Select url,type,NOM,NUMERO,MU_AVANT,SIGMA_AVANT,MU_AVANT_DRIVER,SIGMA_AVANT_DRIVER,POIDS_DRIVER,HANDICAP,DISTANCE,GAIN from VERIF_PRONOS where URL='"+ url+"' and trim(DRIVER) <>'' and trim(POIDS_DRIVER)<>''")

	print(query)
	cursor.execute(	query )

	rows = cursor.fetchall()

	PREDICT = pd.DataFrame(columns=['NOM','NUMERO','PRONO_REG_LINEAIRE','PRONO_TEMPS_REG_LINEAIRE','NB_COURSE'])

	for row in rows:
		#X_predict = pd.DataFrame(columns=['MU_AVANT', 'MU_AVANT_DRIVER', 'DISTANCE','GAIN','RAPPORT1','RAPPORT2'])
		#X_predict.loc[len(X_predict)] = [row[17],row[18],row[15],row[1],row[10],row[11]]  
		X_predict = pd.DataFrame(columns=['MU_AVANT', 'SIGMA_AVANT','MU_AVANT_DRIVER', 'SIGMA_AVANT_DRIVER','POIDS_DRIVER','HANDICAP','DISTANCE','GAIN'])
		X_predict.loc[len(X_predict)] = [row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11]]  


		cursor = connnexion.cursor() 
		print(row)
		query=("Select URL,NOM,TEMPS,MU_AVANT,SIGMA_AVANT,MU_AVANT_DRIVER,SIGMA_AVANT_DRIVER,POIDS_DRIVER,HANDICAP,DISTANCE,GAIN from VERIF_PRONOS where nom='"+ str(row[2])+"' and type='"+str(row[1])+"' and TEMPS<>-1 and TEMPS is not null ")

		print(query)
		cursor.execute(	query )
		rows2 = cursor.fetchall()

		#X = pd.DataFrame(columns=['MU_AVANT', 'MU_AVANT_DRIVER', 'DISTANCE','GAIN','RAPPORT1','RAPPORT2'])
		X = pd.DataFrame(columns=['MU_AVANT', 'SIGMA_AVANT','MU_AVANT_DRIVER', 'SIGMA_AVANT_DRIVER','POIDS_DRIVER','HANDICAP','DISTANCE','GAIN'])
		Y = pd.DataFrame(columns=['TEMPS'])

		NB_COURSE=0
		for row2 in rows2:
			NB_COURSE+=1
			Y.loc[len(Y)] = [row2[2]]
			print(str(row2[2]))
			#X.loc[len(X)] = [row2[17],row2[18],row2[15],row2[1],row2[10],row2[11]]
			MU_AVANT = row2[3] if row2[3]  else 25
			SIGMA_AVANT= row2[4] if row2[4]  else 8
			MU_AVANT_DRIVER = row2[5] if row2[5]  else 25
			SIGMA_AVANT_DRIVER = row2[6] if row2[6]  else 8
			POIDS_DRIVER = row2[7] if row2[7]  else 0
			HANDICAP = row2[8] if row2[8]  else 0

			print(str(MU_AVANT))
			print(str(SIGMA_AVANT))
			print(str(MU_AVANT_DRIVER))
			print(str(SIGMA_AVANT_DRIVER))
			print(str(POIDS_DRIVER))
			print(str(HANDICAP))
			print(str(row2[9]))
			print(str(row2[10]))

			X.loc[len(X)] = [MU_AVANT,SIGMA_AVANT,MU_AVANT_DRIVER,SIGMA_AVANT_DRIVER,POIDS_DRIVER,HANDICAP,row2[9],row2[10]]  
			print(X)
			print(Y)

		if len(rows2)>1:
			regr  = LinearRegression()
			result_regr=regr.fit(X,Y)

			y_predict = regr.predict(X_predict)

			print('------------->>>'+str(row[2])+'-'+str(row[3])+':'+str(y_predict))
			#model = smf.OLS(Y, X).fit()
			#print(model.summary())
			#print(model.conf_int(alpha=0.05, cols=None))

			#PREDICT = columns=['NOM','NUMERO','PRONO_REG_LINEAIRE','PRONO_TEMPS_REG_LINEAIRE','NB_COURSE']
			PREDICT.loc[len(PREDICT)] = [row[2],row[3],0,y_predict[0][0],NB_COURSE]  


	PREDICT_SORT=PREDICT.sort_values(by=['PRONO_TEMPS_REG_LINEAIRE'])

	index_place=0
	for i in PREDICT_SORT.index:
		index_place+=1
		PREDICT_SORT.loc[i, 'PRONO_REG_LINEAIRE'] = index_place


	print(PREDICT_SORT)
	for i in range(len(PREDICT_SORT)):
		#alimentation dans la BDD du participant
		query = ('UPDATE PRONOS SET NB_COURSE=%s ,PRONO_REG_LINEAIRE=%s ,PRONO_TEMPS_REG_LINEAIRE=%s WHERE URL = "%s" and upper(NOM) = upper("%s") and NUMERO =  %s ' % 
					(PREDICT_SORT['NB_COURSE'][i],PREDICT_SORT['PRONO_REG_LINEAIRE'][i],PREDICT_SORT['PRONO_TEMPS_REG_LINEAIRE'][i],url,PREDICT_SORT['NOM'][i],PREDICT_SORT['NUMERO'][i]))

		print(query)
		cursor.execute(query)
		connnexion.commit()








def moindre_au_carre(url):

	#----------------------------------------------------------------------------------------------------------
	#Connexion a la base de données
	try:
		connnexion = sqlite3.connect('../03 - BDD/BasePMU.db')
	except:
		print ('une erreur est survenue lors de la connection de la base : moindre_au_carre')
		exit(1)
	#----------------------------------------------------------------------------------------------------------

	cursor = connnexion.cursor() 
	query=("Select NOM,TYPE,DISTANCE from VERIF_PRONOS where URL='"+ url+"' and trim(DRIVER) <>''")
	cursor.execute(	query )
	rows = cursor.fetchall()

	for row in rows:
		X = []
		Y = []

		cursor = connnexion.cursor() 
		query=("Select NOM,TYPE,TEMPS,DISTANCE from VERIF_PRONOS where nom='"+ str(row[0])+"' and type='"+str(row[1])+"' and TEMPS<>-1 and TEMPS is not null ")
		print(query)
		cursor.execute(	query )
		rows2 = cursor.fetchall()

		for row2 in rows2:
			Y.append(row2[2])
			X.append(row2[3])
		avg_X=sum(X) / float(len(X))
		avg_Y=sum(Y) / float(len(Y))


		sum_Xi_Yi=0
		sum_Xi_avg_X_carre=0

		for i in range(len(rows2)):
			sum_Xi_Yi += (X[i]-avg_X) * (Y[i]-avg_Y)
			sum_Xi_avg_X_carre+=(X[i]-avg_X)**2

		a=sum_Xi_Yi/sum_Xi_avg_X_carre

		b = avg_Y - (a * avg_X)

		print(row[0] +'-'+str(a*row[2]+b))

#moindre_au_carre('courses/29012018/R3/C7')