
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
from Course_veille import *
from sklearn.datasets import make_friedman1
from scipy import stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.formula.api as smf
from statsmodels.stats.outliers_influence import summary_table
from matplotlib.pyplot import *
import math
from Package.downloadWebPMU import *

pagePMU = codecs.open('../02 - Page Web/listeProgramme.html', 'r','utf-8')
listCourse=listeCoursePMU2(pagePMU)
print(listCourse)