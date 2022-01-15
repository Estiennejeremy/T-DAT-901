from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url, reverse
from django.template import RequestContext
from django.utils.safestring import SafeString
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage
from django.templatetags.static import static
from django.conf import settings

import os
import csv
import pandas as pd
import math
import calendar
import json
from numpy import number

from .functions import *



def home(request):
    if request.method == 'POST':
      csvFile = 'csv/KaDo_small.csv'
      file_csvFile = open(os.path.join(settings.STATIC_ROOT, csvFile))
      myDataframe = pd.read_csv(file_csvFile, header=0)  
      clientID = 0 #Init
      if request.POST.get('clientID') and 'clientID' in request.POST:
        clientID = int(request.POST.get('clientID'))
      clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
      if clientDataframe.size > 0:
        return redirect(reverse('homePageUser') + '?clientID=' + str(clientID))
      else:
        return redirect(reverse('homePage') + '?error=true')
    page = {
      'status': request.GET.get('error')
    }
    print("Result ==>", request.GET.get('error'))
    return render (request, "home.html", page)


def makePieDatas (myDataframe, myClass, myTotal) : 
  getClasses = dfToJson (mostOccurences (myDataframe, myClass, 10), "split")
  nameClasss = getClasses ['index']
  countClass = getClasses ['data']
  if (sum(countClass) < myTotal):
    nameClasss.append('AUTRE')
    countClass.append (myTotal - sum(countClass))
  return nameClasss, countClass

def homeUser(request):
    # if request.method == 'POST':
    csvFile = 'csv/KaDo_small.csv'
    file_csvFile = open(os.path.join(settings.STATIC_ROOT, csvFile))
    myDataframe = pd.read_csv(file_csvFile, header=0)  

    clientID = 0
    if request.GET.get('clientID') and 'clientID' in request.GET:
      clientID = int(request.GET.get('clientID'))
    if clientID > 0:
      clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
      clientTotal, clientSumPrice = totalArticles (clientDataframe)
      bestMois, totalBestMois = bestMonth (clientDataframe)
      clientMaxArticle, clientMaxPrice, maxArticleOccurences = mostExpansive (clientDataframe)
      clientMinArticle, clientMinPrice, minArticleOccurences = lessExpansive (clientDataframe)
      nombreCommandes = totalCommandes (clientDataframe)
      clientMeanPrice = meanPrice (clientDataframe)
      nbParCommande = meanCommandes (clientDataframe)
      bestCommande = getBestCommande (clientDataframe)
      bestCommandeDf = commandeDataframe (clientDataframe, bestCommande)
      nbBestCommande = clientDataframe['TICKET_ID'].value_counts()[bestCommande]
      priceBestCommande = bestCommandeDf['PRIX_NET'].sum()
      monthBestCommande = bestCommandeDf['MOIS_VENTE'].iloc[0]
      monthBestCommande = calendar.month_name[int(monthBestCommande)]
      mostFamilles = dfToJson (mostOccurences (clientDataframe, 'FAMILLE', 3), "split")
      mostUnivers = dfToJson (mostOccurences (clientDataframe, 'UNIVERS', 3), "split")
      mostMailles = dfToJson (mostOccurences (clientDataframe, 'MAILLE', 3), "split")
      mostArticles = dfToJson (mostOccurences (clientDataframe, 'LIBELLE', 3), "split")

      nameFamilles, countFamilles = makePieDatas (clientDataframe, "FAMILLE", clientTotal)
      nameUnivers, countUnivers = makePieDatas (clientDataframe, "UNIVERS", clientTotal)
      nameMailles, countMailles = makePieDatas (clientDataframe, "MAILLE", clientTotal)

      totalByMonth = totalArticlesByMonths (clientDataframe)
      priceByMonth = totalPriceByMonths (clientDataframe)
      totalByMonthByMaille = totalArticlesByMonthsByMailles (clientDataframe)
      totalByMailleByClient = totalArticlesMaillesInClient (clientDataframe)
     
      commandesClient = dfToJson (commandesDataframe (clientDataframe), "records")
 
      first_recommendation = get_products_first_recommendation(clientDataframe)
      first_recommendation = getInfosArticle (myDataframe, first_recommendation)
      second_recommendation = get_products_second_recommendation(myDataframe, clientDataframe)[0]
      second_recommendation = getInfosArticle (myDataframe, second_recommendation)
      third_recommendation = get_products_third_recommendation(myDataframe, clientDataframe)
      third_recommendation = getInfosArticle (myDataframe, third_recommendation)
      fourth_recommendation = get_products_fourth_recommendation(myDataframe, clientDataframe)
      fourth_recommendation = getInfosArticle (myDataframe, fourth_recommendation)

      myDatas = {
          'clientID' : clientID,
          'clientTotal': clientTotal,
          'clientSumPrice': round(clientSumPrice, 2),
          'bestMois' : bestMois,
          'totalBestMois' : totalBestMois,
          'clientMaxArticle': clientMaxArticle,
          'clientMaxPrice': clientMaxPrice,
          'maxArticleOccurences': maxArticleOccurences,
          'clientMinArticle': clientMinArticle,
          'clientMinPrice': clientMinPrice,
          'minArticleOccurences': minArticleOccurences,
          'nombreCommandes': nombreCommandes,
          'clientMeanPrice': round(clientMeanPrice, 2),
          'nbParCommande': round(nbParCommande, 2),
          'bestCommande': bestCommande,
          'nbBestCommande': nbBestCommande,
          'priceBestCommande': priceBestCommande,
          'monthBestCommande': monthBestCommande,
          'mostFamilles': mostFamilles,
          'mostUnivers': mostUnivers,
          'mostMailles': mostMailles,
          'mostArticles': mostArticles,
          'nameFamilles': nameFamilles,
          'countFamilles': countFamilles,
          'nameUnivers': nameUnivers,
          'countUnivers': countUnivers,
          'nameMailles': nameMailles,
          'countMailles': countMailles,
          'totalByMonth': SafeString(totalByMonth),
          'priceByMonth': priceByMonth,
          'totalByMonthByMaille': totalByMonthByMaille,
          'totalByMailleByClient': json.dumps(totalByMailleByClient.tolist()),
          'commandesClient': commandesClient,
          'first_recommendation': first_recommendation,
          'second_recommendation': second_recommendation,
          'third_recommendation': third_recommendation,
          'fourth_recommendation': fourth_recommendation
      }
      return render (request, "homeUserID.html", myDatas)
    else:
      return redirect(reverse('homePage') + '?error=true') # Probleme d'id client

