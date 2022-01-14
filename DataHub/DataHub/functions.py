import json
import csv
from numpy import number
import pandas as pd
import math
import calendar

#dataframe to json | columns - index - records - split - table - values
def dfToJson (dataframe, thisOriant = "index") : 
	result = dataframe.to_json(orient= thisOriant)
	parsed = json.loads(result)
	return parsed


def commandesDataframe (dataframe):
    months = {1: 'Janvier', 2: 'Fevrier', 3: 'Mars', 4: 'Avril', 5: 'Mai', 6: 'Juin', 7: 'Juillet', 8: 'Aout', 9: 'Septembre', 10: 'Octobre', 11: 'Novembre', 12: 'Decembre'}

    result = dataframe.groupby(['TICKET_ID', 'MOIS_VENTE']).agg(NOMBRE_ARTICLES = ('TICKET_ID', 'size'), PRIX_TOTAL = ('PRIX_NET', 'sum'))
    result = result.reset_index(level=['TICKET_ID', 'MOIS_VENTE'])
    result['MOIS_VENTE'] = result['MOIS_VENTE'].apply(lambda x: months[x])
    return result

#Nombre total d'articles dans le dataframe
def totalArticles (dataframe): 
	index = dataframe.index
	total = len (index)
	sumPrice = dataframe['PRIX_NET'].sum()
	return total, sumPrice

#nombre de commandes dans un dataframe
def totalCommandes (dataframe): 
	return dataframe['TICKET_ID'].nunique()

#prix moyen des articles d'un dataframe
def meanPrice (dataframe): 
	return dataframe['PRIX_NET'].describe()['mean']

#nombre d'article moyen des commandes dans un dataframe
def meanCommandes (dataframe): 
	return dataframe['TICKET_ID'].value_counts().mean()

def totalArticlesByMonths (dataframe) :
	result = []
	for i in range (12) : 
		result.append((dataframe['MOIS_VENTE']== i+1).sum())
	return result

def totalArticlesMaillesInClient (dataframe) :
	resultv3 = dataframe['FAMILLE'].unique()
	return resultv3

def totalArticlesByMonthsByMailles (dataframe) :
	result = dataframe['MOIS_VENTE'].value_counts().sort_index()
	resultv2 = dataframe.groupby("MOIS_VENTE")['FAMILLE'].value_counts().to_json(orient="split")
	return resultv2

def totalPriceByMonths (dataframe) :
	result = []
	for i in range (12) :
		df = dataframe[dataframe['MOIS_VENTE'] == i+1]
		result.append((df['PRIX_NET']).sum())
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
def mostOccurence (dataframe, column) :
	mostOccurence = dataframe[column].value_counts().idxmax()
	totalMostOccurence = dataframe[column].value_counts()[mostOccurence]
	return mostOccurence, totalMostOccurence

#Article le plus acheté
def mostOccurences (dataframe, column, elements=500) :
	dfOccurences = dataframe[column].value_counts()
	dfTopOccurences = dfOccurences.head(elements)
	return dfTopOccurences


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


def getInfosArticle (dataframe, article) :
	result = dataframe[dataframe['LIBELLE'] == article]
	result = dfToJson(dataframe.iloc[0])
	article = result ['LIBELLE']
	result['total'] = dataframe.LIBELLE.value_counts()[article]
	return result

#RECOMMENDATION 1
###############################################################
# Recommandation en fonction du mois d'achat
def get_products_recommendation1(customer_dataset):
    if customer_dataset.empty:
            from datetime import datetime;
            return get_most_sell_product(datetime.now().month), customer_dataset
    else:
        return get_most_sell_product(get_last_bought_month(customer_dataset), customer_dataset)
# On recupère le mois de la  dernière commande du client
def get_last_bought_month(customer_dataset):
    return customer_dataset["MOIS_VENTE"].max()
# On recupère le produit le plus vendu en fonction d'un mois
def get_most_sell_product(month, df):
    df_month = df[df["MOIS_VENTE"] == month];
    return df_month.groupby("LIBELLE").agg({"TICKET_ID": pd.Series.nunique}).sort_values(by='TICKET_ID', ascending=False).reset_index().iloc[0][0]