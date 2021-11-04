from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib.staticfiles.templatetags.staticfiles import static
from django.templatetags.static import static

import csv
import pandas as pd
import math
import calendar
from django.contrib.staticfiles import finders

def home(request):
    # if request.method == 'POST':
    csvFile = static('KaDo_small.csv')
    #myDataframe = pd.read_csv(csvFile, header=0)
    # print ("------------STATS CLIENT-------------")
    clientID = 931482751
    # clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
    # print ("Client ID : ", clientID)
    # print ("---------------GENERAL---------------")

    return HttpResponse("Client ID : ", clientID)

