import re
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium import webdriver
import selenium.webdriver.support.ui as ui 
from bs4 import BeautifulSoup
import sqlite3
import time
import os
from Course_a_venir import *
from Course_veille import *
from Package.mail import *
import sys
from reporting import *
from Package.MAJCourse_du_jours import *
from Package.coursePMU_Rapport import *

def programme():	
	date_du_jours=datetime.date.today()
	mail('DEBUT ','debut')
	
	print('------------ Traitement des courses a venir ------------------')
	initialise_Course_a_Venir()
	mail('Init Courses a venir','Fin Ok')

	print('------------ Traitement des courses de la veille ------------------')
	recupere_Resulat_Course_Veille()
	mail('Traitement des courses de la veille','Fin Ok')

	MAJCourse_du_jours()
	mail('MAJ Course du jours','Fin Ok')

	date_demain=datetime.date.today()+ datetime.timedelta(1)
	date_demain_formate=date_demain.strftime('%d%m%Y')
	course_a_potentiel(date_demain_formate)

	date_veille=datetime.date.today()+ datetime.timedelta(-1)
	date_veille=date_veille.strftime('%d%m%Y')
	calculRapport(date_veille)
	AnalysePronos(date_veille)
	
	
	date_du_jours_formate=date_du_jours.strftime('%d%m%Y')
	course_a_potentiel(date_du_jours_formate)
	calculRapport(date_du_jours_formate)

	mail('FIN ','fin')

programme()		