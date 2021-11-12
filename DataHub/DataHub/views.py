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


def allMonths (dataframe) : 
	return dataframe['MOIS_VENTE'].value_counts()


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

def home(request):
    # if request.method == 'POST':
    csvFile = 'KaDo_small.csv'
    file_csvFile = open(os.path.join(settings.STATIC_ROOT, csvFile))
    myDataframe = pd.read_csv(file_csvFile, header=0)  
    print ("------------STATS CLIENT-------------")
    htmlStr = "------------STATS CLIENT------------- <br/>";
    clientID = 931482751
    clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
    print ("Client ID : " +  str(clientID))
    htmlStr += "Client ID : " + str(clientID) + "<br/>";
    
    print ("---------------GENERAL---------------")
    htmlStr += "---------------GENERAL---------------"+ "<br/>";
    clientTotal, clientSumPrice = totalArticles (clientDataframe)
    print ("Total d'articles commandés : ", clientTotal)
    print ("Total dépensé : " + str(round(clientSumPrice, 2)) + "€")
    htmlStr += "Total d'articles commandés : " + str(clientTotal) + "<br/>";
    htmlStr += "Total dépensé : " + str(round(clientSumPrice, 2)) + "€"+ "<br/>";
    bestMois, totalBestMois = bestMonth (clientDataframe)
    print ("Mois de prédilections : ", bestMois, " - ", totalBestMois, " articles commandées")
    htmlStr += "Mois de prédilections : " + str(bestMois) + " - " + str(totalBestMois) + " articles commandées"+ "<br/>";
    clientMaxArticle, clientMaxPrice, maxArticleOccurences = mostExpansive (clientDataframe)
    print ("Article le plus chère : ", clientMaxArticle, " - ", round(clientMaxPrice, 2), "€ - ", maxArticleOccurences, "achats")
    htmlStr += "Article le plus chère : " + str(clientMaxArticle) + " - " + str(round(clientMaxPrice, 2)) + "€ - " + str(maxArticleOccurences) + "achats"+ "<br/>";
    clientMinArticle, clientMinPrice, minArticleOccurences = lessExpansive (clientDataframe)
    print ("Article le moins chère : ", clientMinArticle, " - ", round(clientMinPrice, 2), "€ - ", minArticleOccurences, "achats")
    htmlStr += "Article le moins chère : " + clientMinArticle + " - " + str(round(clientMinPrice, 2)) + "€ - " + str(minArticleOccurences) + "achats"+ "<br/>";
    nombreCommandes = totalCommandes (clientDataframe)
    print ("Nombre de commandes : ", nombreCommandes)
    htmlStr += "Nombre de commandes : " + str(nombreCommandes)+ "<br/>";
    clientMeanPrice = meanPrice (clientDataframe)
    print ("Prix moyen des articles commandées : ", round(clientMeanPrice, 2), "€")
    htmlStr += "Prix moyen des articles commandées : " + str(round(clientMeanPrice, 2)) + "€"+ "<br/>";
    nbParCommande = meanCommandes (clientDataframe)
    print ("Nombre d'article par commande en moyenne : ", round(nbParCommande, 2))
    htmlStr += "Nombre d'article par commande en moyenne : " + str(round(nbParCommande, 2))+ "<br/>";

    print ("---------MEILLEURE COMMANDE---------")
    htmlStr += "---------MEILLEURE COMMANDE---------"+ "<br/>";
    ###MEILLEURE COMMANDE###
    #print (clientDataframe['TICKET_ID'].value_counts())
    bestCommande = getBestCommande (clientDataframe)
    bestCommandeDf = commandeDataframe (clientDataframe, bestCommande)
    nbBestCommande = clientDataframe['TICKET_ID'].value_counts()[bestCommande]
    priceBestCommande = bestCommandeDf['PRIX_NET'].sum()
    monthBestCommande = bestCommandeDf['MOIS_VENTE'].iloc[0]
    monthBestCommande = calendar.month_name[int(monthBestCommande)]
    print ("Plus grosse commande : ", bestCommande, " -  Mois : ", monthBestCommande)
    htmlStr += "Plus grosse commande : " + str(bestCommande) + " -  Mois : " +  str(monthBestCommande)+ "<br/>";
    print (str(nbBestCommande), " articles - ", str(priceBestCommande), "€")
    htmlStr += str(nbBestCommande) + " articles - " + str(priceBestCommande) + "€"+ "<br/>";
    print ("--------MEILLEURES CATEGORIES--------")
    htmlStr += "--------MEILLEURES CATEGORIES--------"+ "<br/>";
    bestFamille, totalBestFamille = mostOccurences (clientDataframe, 'FAMILLE')
    print ("Famille la plus commandée : ", bestFamille, " - ", totalBestFamille, " articles")
    htmlStr += "Famille la plus commandée : " + bestFamille + " - " + str(totalBestFamille) + " articles"+ "<br/>";
    bestUnivers, totalBestUnivers = mostOccurences (clientDataframe, 'UNIVERS')
    print ("Univers le plus commandé : ", bestUnivers, " - ", totalBestUnivers, " articles")
    htmlStr += "Univers le plus commandé : " + str(bestUnivers) + " - " + str(totalBestUnivers) + " articles"+ "<br/>";
    bestMaille, totalBestMaille = mostOccurences (clientDataframe, 'MAILLE')
    print ("Maille la plus commandée : ", bestMaille, " - ", totalBestMaille, " articles")
    htmlStr += "Maille la plus commandée : " + str(bestMaille) + " - " + str(totalBestMaille) + " articles"+ "<br/>";
    bestArticle, totalBestArticle = mostOccurences (clientDataframe, 'LIBELLE')
    print ("Univers le plus commandé : ", bestArticle, " - ", totalBestArticle, " articles")
    htmlStr += "Univers le plus commandé : " + str(bestArticle) + " - " + str(totalBestArticle) + " articles"+ "<br/>";

    return HttpResponse(htmlStr)
