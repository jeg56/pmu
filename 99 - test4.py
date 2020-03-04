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
from Package.recalculTps import *
import sys
from reporting import *
from Package.MAJCourse_du_jours import *
from sklearn.linear_model import LinearRegression
from scipy import stats

initialiseTrueskill_RG('courses/30112017/R1/C1')