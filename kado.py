import csv
import pandas as pd
import numpy as np
import math


csvFIle = 'KaDo_small.csv'
#csvFIle = 'KaDo.csv'

dataframe = pd.read_csv(csvFIle, header=0)

index = dataframe.index
total = len (index)
#print (total)

meanPrix = dataframe["PRIX_NET"].mean()
#print (meanPrix)

#print (dataframe['MOIS_VENTE'].value_counts())
#print (dataframe['FAMILLE'].value_counts())
#print (dataframe['UNIVERS'].value_counts())
#print (dataframe['MAILLE'].value_counts())
#print (dataframe['CLI_ID'].value_counts())

userDataframe = dataframe[dataframe['CLI_ID'] == 931482751]

print (userDataframe)
print (userDataframe['MOIS_VENTE'].value_counts())
print (userDataframe['FAMILLE'].value_counts())
#print (userDataframe['UNIVERS'].value_counts())
#print (userDataframe['MAILLE'].value_counts())