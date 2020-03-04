# -*- coding: UTF8 -*-

from Package.downloadWebPMU import *
from Package.coursePMU import *
from Package.alimBDD import *
from Package.classmentTrueskill import *
import re

from regression import *
import time
import os
import datetime
import codecs

def initialise_Course_a_Venir():
	#----------------------------------------------------------------------------------------------------------
	print('----------------'+ str(datetime.date.today()+ datetime.timedelta(1)))

	# recupère la page Web des courses de demain
	print('On télecharge la page Web globale des courses de demain')
	pagePMU=downloadWebPMUpage()
	

	print('On recupère la page Web détail des courses de demain')
	listCourse=listeCoursePMU2(pagePMU)

	#print (len(listCourse))	      

	# recupère le détail de la course qui aura lieu
	for i in range(0,len(listCourse)):
		print(listCourse[i][3])
		#course=downloadWebPMUCourse(listCourse[i][2])
		course,pronos=downloadWebPMUCourseV3(listCourse[i][3])
		course = codecs.open('../02 - Page Web/course.html', 'r','utf-8')

		#Alimentre table COURSE : meteo,vents 
		infosCourse=infosCourseAVenir(course)
		alimCourseBDD1(listCourse[i],infosCourse)

		#Déclare les lignes PARTICIPANT
		#participantCourseAVenirV2(listCourse[i][2])
		participantCourseAVenirV3(listCourse[i][3])
		initialiseTrueskill(listCourse[i][3])
		initialiseTrueskill_Driver(listCourse[i][3])

		regression(listCourse[i][3])

		date_demain=datetime.date.today()+ datetime.timedelta(1)
		date_demain=date_demain.strftime('%d%m%Y')
		calculRapport(date_demain)

		#os.remove('../02 - Page Web/'+listCourse[i][2].replace('/','_')+'.html')

