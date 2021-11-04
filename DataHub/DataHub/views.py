from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib.staticfiles.templatetags.staticfiles import static
from django.templatetags.static import static

import csv
import pandas as pd
import math
import calendar
from django.contrib.staticfiles import finders

from django.contrib.staticfiles.storage import staticfiles_storage
import os
from django.templatetags.static import static
from django.conf import settings

def home(request):
    # if request.method == 'POST':
    csvFile = static('KaDo_small.csv')
    #myDataframe = pd.read_csv(csvFile, header=0)
    # print ("------------STATS CLIENT-------------")
    clientID = 931482751
    # clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
    # print ("Client ID : ", clientID)
    # print ("---------------GENERAL---------------")
    url = staticfiles_storage.url('myfile.txt')
    p = staticfiles_storage.path('myfile.txt')
    # urlv2 = static('myfile.txt')
    # os.path.isfile(urlv2) # False
    # file_path = os.path.join(settings.STATIC_ROOT, 'myfile.txt')
    # PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    file_ = open(os.path.join(settings.STATIC_ROOT, 'myfile.txt'))
    content = file_.readlines()
    return HttpResponse("Client ID : aze" + str(content))
