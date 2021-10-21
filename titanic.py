import csv
import pandas as pd
import numpy as np
import math

dataframe = pd.read_csv('titanic.csv', header=0)
index = dataframe.index
total = len (index)
ageNotNull = dataframe["age"].notnull().sum()
ageNull = dataframe["age"].isnull().sum()



meanAge = dataframe["age"].mean()
meanPrix = dataframe["fare"].mean()


suvivorDataframe = dataframe[dataframe['survived'] == 1]

suvivorMeanAge = suvivorDataframe["age"].mean()
suvivorMeanPrix = suvivorDataframe["fare"].mean()


print ('Total passagers : ' + str(total))
print ('age ' + str(ageNotNull) +' non-null ' + str(ageNull) + ' null')
print ('Age moyen : ' + str(round(meanAge, 2)))
print ('Age moyen des survivants: ' + str(round(suvivorMeanAge, 2)))
print ('Prix moyen du ticket: ' + str(round(meanPrix, 2)))
print ('Prix moyen du ticket des survivants: ' + str(round(suvivorMeanPrix, 2)))


womanDataframe = dataframe[dataframe['sex'] == 'female']
manDataframe = dataframe[dataframe['sex'] == 'male']

womanMeanAge = womanDataframe["age"].mean()
manMeanAge = manDataframe["age"].mean()
print ('Age moyen femmes: ' + str(round(womanMeanAge, 2)))
print ('Age moyen hommes: ' + str(round(manMeanAge, 2)))


womanSurviedPercentage= womanDataframe['survived'].value_counts(normalize=True) * 100
print ("woman survied percentage: " + str (round (womanSurviedPercentage [1], 2)))
manSurviedPercentage= manDataframe['survived'].value_counts(normalize=True) * 100
print ("man survied percentage: " + str (round (manSurviedPercentage [1], 2)))


totalAgeDataframe = pd.cut(x=dataframe["age"], bins=[0,10,20,30,40,50,60,70,80,90,100], labels=["0's","10's","20's","30's","40's","50's","60's","70's","80's","90's"])
print (totalAgeDataframe)

survivorAgeDataframe = pd.cut(x=suvivorDataframe["age"], bins=[0,10,20,30,40,50,60,70,80,90,100], labels=["0's","10's","20's","30's","40's","50's","60's","70's","80's","90's"])
print (survivorAgeDataframe)

print(totalAgeDataframe.value_counts())
print(survivorAgeDataframe.value_counts())

#ageDataframe = pd.concat([totalAgeDataframe, survivorAgeDataframe], axis=1)
print (ageDataframe)
print (ageDataframe['age'].value_counts())