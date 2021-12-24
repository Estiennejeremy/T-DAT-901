from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render, resolve_url, reverse
from django.template import RequestContext
#from django.contrib.staticfiles.templatetags.staticfiles import static
#from django.templatetags.static import static
from django.utils.safestring import SafeString

import csv
from numpy import number
import pandas as pd
import math
import calendar
import json
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

import os
from django.templatetags.static import static
from django.conf import settings


def dfToJson (dataframe, thisOriant = "index") : 
	result = dataframe.to_json(orient= thisOriant)
	parsed = json.loads(result)
	return parsed

def commandesDataframe (dataframe):
	result = dataframe.groupby(['TICKET_ID', 'MOIS_VENTE']).agg(NOMBRE_ARTICLES = ('TICKET_ID', 'size'), PRIX_TOTAL = ('PRIX_NET', 'sum'))
	return result.reset_index(level=['TICKET_ID', 'MOIS_VENTE'])

#Nombre total d'articles dans le dataframe
def totalArticles (dataframe): 
	index = dataframe.index
	total = len (index)
	sumPrice = dataframe['PRIX_NET'].sum()
	return total, sumPrice

#nombre de commandesdans un dataframe
def totalCommandes (dataframe): 
	return dataframe['TICKET_ID'].describe()['count']

#prix moyen des articles d'un dataframe
def meanPrice (dataframe): 
	return dataframe['PRIX_NET'].describe()['mean']

#nombre d'article moyen des commandes dans un dataframe
def meanCommandes (dataframe): 
	return dataframe['TICKET_ID'].value_counts().mean()

def totalArticlesByMonths (dataframe) : 
	result = dataframe['MOIS_VENTE'].value_counts().sort_index()
	return result

def totalArticlesMaillesInClient (dataframe) :
	resultv3 = dataframe['FAMILLE'].unique()
	return resultv3

def totalArticlesByMonthsByMailles (dataframe) :
	result = dataframe['MOIS_VENTE'].value_counts().sort_index()
	resultv2 = dataframe.groupby("MOIS_VENTE")['FAMILLE'].value_counts().to_json(orient="split")
	return resultv2

def totalPriceByMonths (dataframe) :
	result = dataframe.groupby("MOIS_VENTE").agg({"PRIX_NET": "sum"})["PRIX_NET"]
	return result

#Meilleur mois de vente
def bestMonth (dataframe) :
	bestMois = dataframe['MOIS_VENTE'].value_counts().idxmax()
	totalBestMois = dataframe['MOIS_VENTE'].value_counts()[bestMois]
	bestMois = calendar.month_name[int(bestMois)]
	return bestMois, totalBestMois


#résumé mois
def specificMonth (dataframe, month) :
	return dataframe['MOIS_VENTE'].value_counts()[month]


#Article le plus acheté
def mostOccurences (dataframe, column) :
	mostOccurence = dataframe[column].value_counts().idxmax()
	totalMostOccurence = dataframe[column].value_counts()[mostOccurence]
	return mostOccurence, totalMostOccurence

#Article le plus acheté
def Top3mostOccurences (clientDataframe, column) :
	Top3mostOccurencesVar = clientDataframe[column].value_counts(dropna=False).head(3)
	return Top3mostOccurencesVar


#Article le plus chère###
def mostExpansive(dataframe) :
	idDf = dataframe['PRIX_NET'].idxmax()
	maxPrice = dataframe['PRIX_NET'].max()
	maxArticle = dataframe ['LIBELLE'][idDf]
	articleOccurences = dataframe['LIBELLE'].value_counts()[maxArticle]
	return maxArticle, maxPrice, articleOccurences


#Article le moins chère
def lessExpansive(dataframe) :
	idDf = dataframe['PRIX_NET'].idxmin()
	minPrice = dataframe['PRIX_NET'].min()
	minArticle = dataframe ['LIBELLE'][idDf]
	articleOccurences = dataframe['LIBELLE'].value_counts()[minArticle]
	return minArticle, minPrice, articleOccurences


#Récupéer l'ID de la plus grosse commande dasn un dataframe
def getBestCommande (dataframe) : 
	 return dataframe['TICKET_ID'].value_counts().idxmax()


#Générer un dataframe à partir de l'ID d'une commande
def commandeDataframe (dataframe, commande) :
	return dataframe[dataframe['TICKET_ID'] == commande]

def homeUser(request):
    # if request.method == 'POST':
    csvFile = 'KaDo_small.csv'
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
      bestFamille, totalBestFamille = mostOccurences (clientDataframe, 'FAMILLE')
      bestUnivers, totalBestUnivers = mostOccurences (clientDataframe, 'UNIVERS')
      bestMaille, totalBestMaille = mostOccurences (clientDataframe, 'MAILLE')
      bestArticle, totalBestArticle = mostOccurences (clientDataframe, 'LIBELLE')
      totalByMonth = totalArticlesByMonths (clientDataframe)
      priceByMonth = dfToJson (totalPriceByMonths (clientDataframe))
      totalByMonthByMaille = totalArticlesByMonthsByMailles (clientDataframe)
      totalByMailleByClient = totalArticlesMaillesInClient (clientDataframe)
      #  Dev De Mehdi
      commandesClient = dfToJson (commandesDataframe (clientDataframe), "records")
      bestTop3Product = Top3mostOccurences (clientDataframe, 'LIBELLE').to_json()
      # Fin Dev Mehdi

      myDatas = {
          'clientID' : clientID,
          'clientTotal': clientTotal,
          'clientSumPrice': clientSumPrice,
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
          'bestFamille': bestFamille,
          'totalBestFamille': totalBestFamille,
          'bestUnivers': bestUnivers,
          'totalBestUnivers': totalBestUnivers,
          'bestMaille': bestMaille,
          'totalBestMaille': totalBestMaille,
          'bestArticle': bestArticle,
          'totalBestArticle': totalBestArticle,
          'totalByMonth': SafeString(totalByMonth),
          'priceByMonth': priceByMonth,
          'totalByMonthByMaille': totalByMonthByMaille,
          'totalByMailleByClient': json.dumps(totalByMailleByClient.tolist()),
          'bestTop3ProductNyClient': bestTop3Product,
          'commandesClient': commandesClient
      }
      return render (request, "homeUserID.html", myDatas)
    else:
      return redirect(reverse('homePage') + '?error=true') # Probleme d'id client

def home(request):
    if request.method == 'POST':
      csvFile = 'KaDo_small.csv'
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
