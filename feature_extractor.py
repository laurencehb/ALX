# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 14:32:47 2015

@author: lbonnet
"""

import pandas as pd
import numpy as np
import os

class FeatureExtractor(object):
    def __init__(self):
        pass

    def fit(self, X_df, y_array):
        pass


    def quarter(self, m):
        if m <= 3:
            return 1
        elif m <= 6:
            return 2
        elif m <= 9:
            return 3
        return 4
  
    def trouver_airport(self, i):
        airports = {'ATL':0, 'ORD':1, 'LAX':2, 'DFW':3, 'DEN':4, 'JFK':5, 'SFO':6, 'CLT':7, 'LAS':8, 'PHX':9, 'IAH':10, 'MIA':11, 'MCO':12, 'EWR':13, 'SEA':14, 'MSP':15, 'DTW':16, 'PHL':17, 'BOS':18, 'LGA':19}
        for airport in airports:
            if airports[airport] == i:
                return airport
        pass


    def somme(self, tab):
        n,m = tab.shape
        t = 0
        for i in range(n):
            for j in range(m):
                t += tab[i][j]
        return t
    
    def completer_trous(self, Xs):
        airports = {'ATL':0, 'ORD':1, 'LAX':2, 'DFW':3, 'DEN':4, 'JFK':5, 'SFO':6, 'CLT':7, 'LAS':8, 'PHX':9, 'IAH':10, 'MIA':11, 'MCO':12, 'EWR':13, 'SEA':14, 'MSP':15, 'DTW':16, 'PHL':17, 'BOS':18, 'LGA':19}
        nb = len(airports)
        nb_quarters = 4
        nb_years = 3
        nb_features = 8
  
        Ys = np.zeros(nb*nb*nb_quarters*nb_years*nb_features, dtype = int)
        Ys = Ys.reshape((nb* nb* nb_quarters* nb_years, nb_features))
        ll = nb* nb* nb_quarters* nb_years
        l = len(Xs)
        
        tab = np.zeros(nb*nb*nb_quarters*nb_years)
        tab = tab.reshape((nb, nb, nb_quarters, nb_years))
        total_fares = np.zeros(nb*nb)
        total_fares = total_fares.reshape((nb, nb))
        total_pax = np.zeros(nb*nb*nb_quarters*nb_years)
        total_pax = total_pax.reshape((nb, nb, nb_quarters, nb_years))
        average_fares = np.zeros(nb*nb*nb_quarters*nb_years)
        average_fares = average_fares.reshape((nb, nb, nb_quarters, nb_years))
    
        #Création du tableau de tous les trajets et remplissage
        x = 0
        for i in range(l):
            ligne = Xs[i]
            orig = airports[ligne[1]]
            dest = airports[ligne[2]]
            fares = ligne[5]
            av_fares = ligne[6]
            pax = ligne[4]
            quart = ligne[3]
            year = ligne[7]
            tab[orig][dest][quart-1][year-2011] += 1
            total_fares[orig][dest] += fares
            average_fares[orig][dest][quart-1][year-2011] = av_fares
            total_pax[orig][dest][quart-1][year-2011] = pax
            x += 1
            

        # Remplissage des trous
        x = 0
        for i in range(nb):
            for j in range(nb):
                for y in range(nb_years):
                    for q in range(nb_quarters):
                        Ys[x][0] = int(x) + 1
                        Ys[x][1] = i
                        Ys[x][2] = j
                        Ys[x][7] = int(y) + 2011
                        Ys[x][3] = int(q) + 1
                        if (tab[i][j][q][y] > 0):
                            Ys[x][4] = int(pax)
                            Ys[x][5] = int(fares)
                            Ys[x][6] = fares / pax
                        else:
                            Ys[x][5] = total_fares[i][j] / 7
                            Ys[x][4] = self.somme(total_pax[i][j][:][:]) / 7
                            Ys[x][6] = Ys[x][5] / Ys[x][4]
                        x += 1
        return Ys
    
    def transform(self, X_df):
        X_encoded = X_df
        path = os.path.dirname(__file__)
        
        airports = {'ATL':0, 'ORD':1, 'LAX':2, 'DFW':3, 'DEN':4, 'JFK':5, 'SFO':6, 'CLT':7, 'LAS':8, 'PHX':9, 'IAH':10, 'MIA':11, 'MCO':12, 'EWR':13, 'SEA':14, 'MSP':15, 'DTW':16, 'PHL':17, 'BOS':18, 'LGA':19}
        
        #uncomment the line below in the submission
        #path = os.path.dirname(__file__)
        #data_weather = pd.read_csv(os.path.join(path, "data_weather.csv"))
        #data_weather = pd.read_csv("data_weather.csv")
        
        air_fares = pd.read_csv(os.path.join(path, "AirFares2012Q1to2013Q2.csv"), sep = ';')
        tab = air_fares.values
        # On complète les quarters qui n'existe pas sur un traje par la moyenne des air_fares sur le trajet
        data_air_fares = self.completer_trous(tab)
        n = len(data_air_fares)
        m = len(data_air_fares[0])

        data_air_fares = np.c_[data_air_fares, np.ones(n, dtype = str)]

        # définition d'une clé pour le join : ORG DES Quarter Year
        for i in range(n):
            data_air_fares[i][m] = str((data_air_fares[i][1])) + ' ' + str(data_air_fares[i][2]) + ' ' + str(data_air_fares[i][3]) + ' ' + str(data_air_fares[i][7])
        data_air_fares = np.delete(data_air_fares, (0), axis=1)
        
        X_air_fares = pd.DataFrame(data_air_fares[:], columns=['ORIGIN', 'DEST', 'Quarter', 'TotalPax', 'TotalFare', 'AverageFare', 'Year', 'Ref'])
        X_air_fares = X_air_fares.drop('ORIGIN', axis=1)
        X_air_fares = X_air_fares.drop('DEST', axis=1)
        X_air_fares = X_air_fares.drop('Quarter', axis=1)
        X_air_fares = X_air_fares.drop('TotalPax', axis=1)
        X_air_fares = X_air_fares.drop('TotalFare', axis=1)
        X_air_fares = X_air_fares.drop('Year', axis=1)
       
        X_air_fares.to_csv(path_or_buf='Result.csv', sep=';')

    
        X_encoded['DateOfDeparture'] = pd.to_datetime(X_encoded['DateOfDeparture'])
        X_encoded['year'] = X_encoded['DateOfDeparture'].dt.year
        X_encoded['month'] = X_encoded['DateOfDeparture'].dt.month
        #X_encoded['day'] = X_encoded['DateOfDeparture'].dt.day
        X_encoded['weekday'] = X_encoded['DateOfDeparture'].dt.weekday
        X_encoded['week'] = X_encoded['DateOfDeparture'].dt.week
        X_encoded['n_days'] = X_encoded['DateOfDeparture'].apply(lambda date: (date - pd.to_datetime("2011-09-01")).days)

        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['year'], prefix='y'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['month'], prefix='m'))
        #X_encoded = X_encoded.join(pd.get_dummies(X_encoded['day'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['weekday'], prefix='wd'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['week'], prefix='w'))

        
        #X_weather = data_weather[['Date', 'AirPort', 'Max TemperatureC']]
        #X_weather = X_weather.rename(columns={'Date': 'DateOfDeparture', 'AirPort': 'Arrival'})
        #X_encoded = X_encoded.set_index(['DateOfDeparture', 'Arrival'])
        #X_weather = X_weather.set_index(['DateOfDeparture', 'Arrival'])
        #X_encoded = X_encoded.join(X_weather).reset_index()
        
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))
        
        X_encoded['quarter'] = X_encoded['month'].apply(lambda m: self.quarter(m))
        X_encoded['ori'] = X_encoded['Departure'].apply(lambda a: airports[a])
        X_encoded['dest'] = X_encoded['Arrival'].apply(lambda a: airports[a])

        X_encoded['Ref'] = X_encoded['ori'].apply(lambda a: str(a)) + ' ' + X_encoded['dest'].apply(lambda b: str(b)) + ' ' + X_encoded['quarter'].apply(lambda b: str(b)) + ' ' + X_encoded['year'].apply(lambda b: str(b))
        
        X_encoded = X_encoded.merge(X_air_fares, how='left',
            left_on=['Ref'], 
            right_on=['Ref'], sort=False)
        
        X_encoded = X_encoded.drop('Ref', axis=1)
        #X_encoded = X_encoded.drop('quarter', axis=1)
        #X_encoded = X_encoded.drop('ori', axis=1)
        #X_encoded = X_encoded.drop('dest', axis=1)
        
        X_encoded['AverageFare'] = X_encoded['AverageFare'].astype(float)
        
        #X_encoded = X_encoded.drop('AverageFare', axis=1)
        
        X_encoded = X_encoded.drop('Departure', axis=1)
        X_encoded = X_encoded.drop('Arrival', axis=1)
        X_encoded = X_encoded.drop('month', axis=1)
        X_encoded = X_encoded.drop('DateOfDeparture', axis=1)
        X_encoded = X_encoded.drop('year', axis=1)
        #X_encoded = X_encoded.drop('weekday', axis=1)
        #X_encoded = X_encoded.drop('week', axis=1)
        X_encoded = X_encoded.drop('std_wtd', axis=1)
        X_encoded = X_encoded.drop('WeeksToDeparture', axis=1)        
         
        #X_encoded.fillna(0)
        #print X_encoded.head()
        
        X_array = X_encoded.values
        return X_array