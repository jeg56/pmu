import sqlite3, pandas as pd
con = sqlite3.connect('../03 - BDD/BasePMU.db')
df = pd.io.sql.read_sql("select * from A_VERIF_PRONOS", con)
con.close()
import numpy as np

values = df[ df.URL == "courses/16092017/R5/C1"].copy()

#Affichage 
#print(df.describe())

#grouped_data=df.groupby(['NOM', 'DRIVER'])
#print(grouped_data['NOM'].describe().unstack())

val=df['MU_AVANT'].aggregate([np.median, np.std, np.mean,np.min]).reset_index()

#values = df[ df.MU_AVANT != "25"].copy()
values =df.query('MU_AVANT != 25')
grouped_data = values.groupby(['TYPE'])
val=grouped_data['MU_AVANT'].describe().unstack()



descr = df['MU_AVANT'].aggregate([np.median, np.std, np.mean]).reset_index()



stat_des = df.describe(d)
print(stat_des)


