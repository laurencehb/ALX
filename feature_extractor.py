# -*- coding: utf-8 -*-
"""
Created on Sat Jul 04 11:01:11 2015

@author: xcallens
"""
import numpy as np
import pandas as pd

pd.set_option('display.max_columns', None)

      
#fares = pd.read_csv("D:\Data\DSSP\Data Camp 3\dreamteamgitlocalrep\AirFares2012Q1to2013Q2.csv", sep = ';')
        
import numpy as np
import pandas as pd
import os

 
class FeatureExtractor(object):
    def __init__(self):
        pass
 
    def fit(self, X_df, y_array):
        pass
 
    def transform(self, X_df):
        X_encoded = X_df
        
        #uncomment the line below in the submission
        path = os.path.dirname(__file__)
        
        #special_days=pd.read_csv("D:\Data\DSSP\Data Camp 3\dreamteamgitlocalrep\data_specialdays.csv", sep = ';')
        #distance=pd.read_csv("D:\Data\DSSP\Data Camp 3\dreamteamgitlocalrep\Distance.csv", sep = ';')
        special_days=pd.read_csv(os.path.join(path, "data_specialdays.csv"), sep = ';')
        distance=pd.read_csv(os.path.join(path, "Distance.csv"), sep = ';')
        

        X_encoded = X_encoded.merge(special_days, how='left', left_on=['DateOfDeparture'], right_on=['DateOfDeparture'], sort=False)
        X_encoded = X_encoded.merge(distance, how='left', left_on=['Departure','Arrival'], right_on=['Departure','Arrival'], sort=False)
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Departure'], prefix='d'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['Arrival'], prefix='a'))
        X_encoded = X_encoded.drop('Departure', axis=1)
        X_encoded = X_encoded.drop('Arrival', axis=1)     
        
        X_encoded['DateOfDeparture'] = pd.to_datetime(X_encoded['DateOfDeparture'])
        X_encoded['year'] = X_encoded['DateOfDeparture'].dt.year
        X_encoded['weekday'] = X_encoded['DateOfDeparture'].dt.weekday
        X_encoded['week'] = X_encoded['DateOfDeparture'].dt.week
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['year'], prefix='y'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['weekday'], prefix='wd'))
        X_encoded = X_encoded.join(pd.get_dummies(X_encoded['week'], prefix='w'))
        
        
        #fares = pd.read_csv("D:\Data\DSSP\Data Camp 3\dreamteamgitlocalrep\AirFares2012Q1to2013Q2.csv", sep = ';')
        fares = pd.read_csv(os.path.join(path,"AirFares2012Q1to2013Q2.csv"), sep = ';')        
        
        X_fares = fares [['ORIGIN', 'DEST', 'Quarter', 'TotalPax','TotalFare', 'AverageFare', 'Year']]
#        X_encoded = X_encoded.merge(X_fares, how='left',
#                   left_on=['Departure', 'Arrival','quarter','year'], 
#                   right_on=['ORIGIN','DEST','Quarter','Year'], sort=False)
                   
                   
        X_encoded = X_encoded.drop('weekday', axis=1)
        X_encoded = X_encoded.drop('week', axis=1)
        X_encoded = X_encoded.drop('year', axis=1)
        #X_encoded = X_encoded.drop('std_wtd', axis=1)
        X_encoded = X_encoded.drop('WeeksToDeparture', axis=1)        

        
        ### Add booking curve XXXX
        X_encoded = X_encoded.drop('WeeksToDepartureMin', axis=1)
        X_encoded = X_encoded.drop('WeeksToDepartureMax', axis=1)     
        X_encoded = X_encoded.drop('WeeksToDepartureMedian', axis=1)
        
        ### Special event
        X_encoded = X_encoded.drop('NYE', axis=1)
        X_encoded = X_encoded.drop('PRESIDENTSDAY', axis=1)
        X_encoded = X_encoded.drop('EASTER', axis=1)
        X_encoded = X_encoded.drop('MEMORIALDAY', axis=1)
        X_encoded = X_encoded.drop('INDEPENDANCEDAY', axis=1)
        X_encoded = X_encoded.drop('LABOURDAY', axis=1)
        X_encoded = X_encoded.drop('HALLOWEEN', axis=1)
        X_encoded = X_encoded.drop('TGV', axis=1)
        X_encoded = X_encoded.drop('XMAS', axis=1)
        
        #data_oil = pd.read_csv("D:\Data\DSSP\Data Camp 3\dreamteamgitlocalrep\oil.csv",sep=';', decimal=',')
        data_oil = pd.read_csv(os.path.join(path,"oil.csv"),sep=';', decimal=',')
        
        X_Oil = data_oil[['DateOfDeparture','Price']]
#       X_holidays = data_holidays[['DateOfDeparture','Xmas','Xmas-1','NYD','NYD-1','Ind','Thg','Thg+1','Lab','Mem']]
        
        #X_Oil = X_Oil.set_index(['DateOfDeparture'])
#        X_holidays = X_holidays.set_index(['DateOfDeparture'])
#        X_Oil = X_Oil.join(X_holidays).reset_index()   
        
        X_Oil['DateOfDeparture'] = pd.to_datetime(X_Oil['DateOfDeparture'])
        
        #data_encoded = data_encoded.merge(X_Oil, how='left', left_on=['DateOfDeparture'], right_on=['DateOfDeparture'], sort=False)
        X_encoded = X_encoded.merge(X_Oil, how='left', left_on=['DateOfDeparture'], right_on=['DateOfDeparture'], sort=False)
                    
#        aaa=X_encoded['AverageFare']
#        ii=np.isnan(X_encoded['AverageFare'])
#        rr=np.where(ii)
#        jj=np.where(ii == True)[0]
#        X_encoded['AverageFare'][jj]=0.0
        X_encoded = X_encoded.drop('DateOfDeparture', axis=1)
        
        X_array = X_encoded.values
        #X_array = np.array(data_encoded)
        return X_array
  