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
	articleDataframe = dataframe[dataframe['LIBELLE'] == article]
	result = dfToJson(articleDataframe.iloc[0])
	result['total'] = dataframe.LIBELLE.value_counts()[article]
	result['PRIX_NET'] = round(articleDataframe['PRIX_NET'].mean(), 2)
	return result


###############################################################
#RECOMMENDATION 1
###############################################################
# Recommandation en fonction du mois d'achat
def get_products_first_recommendation(customer_dataset):
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

###############################################################
#RECOMMENDATION 2
###############################################################
# Recommandation en fonction de la maille
def get_products_second_recommendation(df, customer_dataset):
    maille_max_dataset = get_maille_max_dataset(customer_dataset)
    maille_max = get_maille_max(maille_max_dataset)
    customer_not_bought_maille_products = get_customer_not_bought_maille_products(df, customer_dataset, maille_max)
    return get_most_five_best_prodcuts_sell(df, customer_not_bought_maille_products)
# Est-ce que c'est ca première commande ?
def is_customer_first_order(customer_dataset):
       return customer_dataset.shape[0] == 1
# Quelle sont les mailles la plus présentes parmi ses commandes ?
def get_maille_max_dataset(customer_dataset):
    mailles_count = customer_dataset.groupby("MAILLE")["TICKET_ID"].size().reset_index(name='counts')
    return mailles_count[mailles_count["counts"] == mailles_count["counts"].max()]
# Est-ce qu'il y a qu'un seul maille ?
def is_single_max_maille(maille_max_dataset):
    return True if len(maille_max_dataset) == 1 else False
# On récupère le nom de la maille la plus présente
def get_maille_max(maille_max_dataset):
	maille_max_dataset = maille_max_dataset.reset_index()
	return maille_max_dataset["MAILLE"][0]
# On récupère tous les produits d'une maille
def get_maille_products(df, maille_max):
    return df[df["MAILLE"] == maille_max]["LIBELLE"].unique()
# On récupère la liste des produits que le client n'a pas acheté dans la maille
def get_customer_not_bought_maille_products(df, customer_dataset, maille_max):
    customer_maille_bought_products = customer_dataset[customer_dataset["MAILLE"] == maille_max]["LIBELLE"].unique()
    maille_products = get_maille_products(df, maille_max)
    return list(set(get_maille_products(df, maille_max)) - set(customer_maille_bought_products))
# On récupère les 5 produits les plus vendu
def get_most_five_best_prodcuts_sell(df, customer_not_bought_maille_products):
    five_most_products_sell = df[df["LIBELLE"].isin(customer_not_bought_maille_products)].groupby("LIBELLE")["TICKET_ID"].agg(TICKET_ID = pd.Series.nunique).sort_values(by='TICKET_ID', ascending=False).head(5).reset_index()
    return five_most_products_sell["LIBELLE"].tolist()

###############################################################
#RECOMMENDATION 3
###############################################################
# Recommandation en fonction de l'attribut de l'univers
def get_products_third_recommendation(df, customer_dataset):
	univers = df['UNIVERS'].unique()
	customer_types = get_customer_types(customer_dataset)
	similar_univers = get_univers_from_type(univers, customer_dataset["UNIVERS"].tolist(), customer_types)
	products, counts =  get_most_products_sell(df, similar_univers)
	return products[counts.index(max(counts))]
## On récupère les types associés au commandes du client
def get_customer_types(customer_dataset):
	types = []
	for index, order in customer_dataset.iterrows():
		_t = order["UNIVERS"].split(" ");
		_t.pop(0)
		types = types + _t
	return types
## On récupère tous les univers correspondant au types
def get_univers_from_type(univers, customer_orders_univers, customer_types):
	res = []
	for univer in univers:
		if(univer not in customer_orders_univers):
			for _type in customer_types:
				if isinstance(univer, str) :
					if _type in univer:
						if(univer not in res):
							res.append(univer)
	return res
## On récupère le produit le plus vendu des univers
def get_most_products_sell(df, univers):
	products = []
	counts = []
	for univer in univers:
		df_univer =  df.loc[df["UNIVERS"] == univer]
		df_libelle = df_univer.groupby("LIBELLE")
		products.append(df_libelle.agg({"TICKET_ID": "count"}).sort_values(by='TICKET_ID', ascending=False)["TICKET_ID"].keys()[0])
		counts.append(df_libelle.agg({"TICKET_ID": "count"}).sort_values(by='TICKET_ID', ascending=False)["TICKET_ID"].iloc()[0])
	return products, counts


###############################################################
#RECOMMENDATION 4
###############################################################
#Recommandation en fonction des commandes similaires
def get_products_fourth_recommendation(df, customer_dataset):
    customers_with_same_product = get_customers_with_same_product(df, customer_dataset)
    most_bought_products = get_most_bought_products_from_customers_list(df, customers_with_same_product)
    return most_bought_products.index[0]
## On chercher parmis tous les autres clients qui a acheter la meme chose que le client
def get_customers_with_same_product(df, customer_dataset):
    return df.loc[df["LIBELLE"].isin(customer_dataset["LIBELLE"])]["CLI_ID"].unique()   
# On cherche parmis la liste des clients, quel sont les produits les plus acheté
# Du produit le plus acheté ou produit le moins acheté
def get_most_bought_products_from_customers_list(df, customer_list):
    return df[df['CLI_ID'].isin(customer_list)].groupby("LIBELLE").agg({"TICKET_ID": pd.Series.nunique}).sort_values(by='TICKET_ID', ascending=False)
