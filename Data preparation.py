# -*- coding: utf-8 -*-
"""
Created on Sat Jul 04 13:47:42 2015

@author: xcallens
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#data = pd.read_csv("top500ondmidt.csv")
data = pd.read_csv("D:/Data/DSSP/Data Camp 3/14_15DataCamp/top500ondmidt.csv")

###index_col=["date", "loc"], 
###usecols=["date", "loc", "x"
                 
data = data[0:10000]

US_top_20 = list("ATL ORD LAX DFW DEN JFK SFO CLT LAS PHX IAH MIA MCO EWR SEA MSP DTW PHL BOS LGA".split())

departure_in_US_top_20 = np.array([departure in US_top_20 for departure in data['Departure'].values])
arrival_in_US_top_20 = np.array([arrival in US_top_20 for arrival in data['Arrival'].values])
data_US_top_20 = data[departure_in_US_top_20 & arrival_in_US_top_20]

data_US_top_20_grouped_by_date = data_US_top_20.groupby(['DateOfDeparture', 'Departure', 'Arrival','WeeksToDeparture'])

data_aggreg = data_US_top_20_grouped_by_date.agg({
        'PAX': np.sum
        }).reset_index()
data_aggreg['log_PAX'] = np.log(data_aggreg['PAX'])
data_aggreg['WeeksToDepartureMean'] = np.mean(data_aggreg['WeeksToDeparture'])
data_aggreg['WeeksToDepartureMedian'] = np.median(data_aggreg['WeeksToDeparture'])
data_aggreg['WeeksToDepartureMin'] = np.min(data_aggreg['WeeksToDeparture'])
data_aggreg['WeeksToDepartureMax'] = np.sum(data_aggreg['WeeksToDeparture'])
data_aggreg['PAXMean'] = np.mean(data_aggreg['PAX'])
data_aggreg['PAXMedian'] = np.median(data_aggreg['PAX'])
data_aggreg['PAXMin'] = np.min(data_aggreg['WeeksToDeparture'])
data_aggreg['std_wtd'] = np.std(data_aggreg['WeeksToDeparture'])

#data_aggreg['PAXMax'] = np.sum(data_aggreg['WeeksToDeparture'])

#data_aggreg['std_wtd'] = data_US_top_20_grouped_by_date.std()['WeeksToDeparture'].values
#data_aggreg['WeeksToDepartureMin'] = data_US_top_20_grouped_by_date.min()['WeeksToDeparture'].values
#data_aggreg['WeeksToDepartureMax'] = data_US_top_20_grouped_by_date.max()['WeeksToDeparture'].values
#data_aggreg['WeeksToDepartureMedian'] = data_US_top_20_grouped_by_date.median()['WeeksToDeparture'].values
#data_aggreg['WeeksToDepartureAverage'] = data_US_top_20_grouped_by_date.mean()['WeeksToDeparture'].values          
         
          
#arrayWeekToDep = data_US_top_20_grouped_by_date['WeeksToDeparture'].values
#minweek = np.amin(arrayWeekToDep)
#data_US_top_20_grouped_by_date2 = data_US_top_20_grouped_by_date.groupby(['DateOfDeparture', 'Departure', 'Arrival'])


         