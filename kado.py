import csv
import pandas as pd
import numpy as np
import math
import calendar


#Nombre total d'articles dans le dataframe
def totalArticles (dataframe): 
	index = dataframe.index
	total = len (index)
	sumPrice = dataframe['PRIX_NET'].sum()
	return total, sumPrice

#nombre de commandes dans un dataframe
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





def main () :
	csvFIle = 'KaDo_small.csv'
	#csvFIle = 'KaDo.csv'
	myDataframe = pd.read_csv(csvFIle, header=0)
	print ("------------STATS CLIENT-------------")
	clientID = 931482751
	clientDataframe = myDataframe[myDataframe['CLI_ID'] == clientID]
	print ("Client ID : ", clientID)
	print ("---------------GENERAL---------------")

	clientTotal, clientSumPrice = totalArticles (clientDataframe)
	print ("Total d'articles commandés : ", clientTotal)
	print ("Total dépensé : ", round(clientSumPrice, 2), "€")

	bestMois, totalBestMois = bestMonth (clientDataframe)
	print ("Mois de prédilections : ", bestMois, " - ", totalBestMois, " articles commandées")

	clientMaxArticle, clientMaxPrice, maxArticleOccurences = mostExpansive (clientDataframe)
	print ("Article le plus chère : ", clientMaxArticle, " - ", round(clientMaxPrice, 2), "€ - ", maxArticleOccurences, "achats")
	clientMinArticle, clientMinPrice, minArticleOccurences = lessExpansive (clientDataframe)
	print ("Article le moins chère : ", clientMinArticle, " - ", round(clientMinPrice, 2), "€ - ", minArticleOccurences, "achats")

	nombreCommandes = totalCommandes (clientDataframe)
	print ("Nombre de commandes : ", nombreCommandes)
	clientMeanPrice = meanPrice (clientDataframe)
	print ("Prix moyen des articles commandées : ", round(clientMeanPrice, 2), "€")
	nbParCommande = meanCommandes (clientDataframe)
	print ("Nombre d'article par commande en moyenne : ", round(nbParCommande, 2))


	print ("---------MEILLEURE COMMANDE---------")
	###MEILLEURE COMMANDE###
	#print (clientDataframe['TICKET_ID'].value_counts())
	bestCommande = getBestCommande (clientDataframe)
	bestCommandeDf = commandeDataframe (clientDataframe, bestCommande)
	nbBestCommande = clientDataframe['TICKET_ID'].value_counts()[bestCommande]
	priceBestCommande = bestCommandeDf['PRIX_NET'].sum()
	monthBestCommande = bestCommandeDf['MOIS_VENTE'].iloc[0]
	monthBestCommande = calendar.month_name[int(monthBestCommande)]
	print ("Plus grosse commande : ", bestCommande, " -  Mois : ", monthBestCommande)
	print (nbBestCommande, " articles - ", priceBestCommande, "€")


	print ("--------MEILLEURES CATEGORIES--------")
	bestFamille, totalBestFamille = mostOccurences (clientDataframe, 'FAMILLE')
	print ("Famille la plus commandée : ", bestFamille, " - ", totalBestFamille, " articles")

	bestUnivers, totalBestUnivers = mostOccurences (clientDataframe, 'UNIVERS')
	print ("Univers le plus commandé : ", bestUnivers, " - ", totalBestUnivers, " articles")

	bestMaille, totalBestMaille = mostOccurences (clientDataframe, 'MAILLE')
	print ("Maille la plus commandée : ", bestMaille, " - ", totalBestMaille, " articles")

	bestArticle, totalBestArticle = mostOccurences (clientDataframe, 'LIBELLE')
	print ("Univers le plus commandé : ", bestArticle, " - ", totalBestArticle, " articles")




main ()