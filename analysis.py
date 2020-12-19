# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 19:36:58 2020

@author: marti
"""

import numpy as np
import pandas as pd
from BookingData import Booking
from rearrangements import get_stay_df
from rearrangements import group_stay_df
from datetime import date, datetime as dt
from dateutil.relativedelta import relativedelta

bookings = pd.read_pickle('bookings_df_sample.pkl')

daily_data = group_stay_df(bookings, group_vars = ['meal'])
daily_data_bad = daily_data.drop("revenue", axis = 1)

daily_data_bad_type = daily_data.astype({'adr': int})

class StayDataFrame(pd.DataFrame):
    
    def __init__(self, *args, **kwargs):
        
        pd.DataFrame.__init__(self, *args, **kwargs)

          # check if DataFrame includes mandatory variables
        required_fields = ['stay_date', 
                                  'roomnights', 
                                  'adr', 
                                  'revenue']
           
        if (any(map(lambda x: x not in self.columns, required_fields))):
               raise ValueError("DataFrame must contain the following variables:\n- 'stay_date'\n- 'roomnights'\n- 'adr'\n- 'revenue'")
               
          # check data dtypes
        df_dtypes = list(self[required_fields].dtypes)
        required_dtypes = [np.dtype('<M8[ns]'), np.dtype('int64'), np.dtype('float64'), np.dtype('float64')]
           
        if df_dtypes != required_dtypes:
            raise ValueError('Data types for required columns must be\n -stay_date: datetime\n -roomnights: int\n -adr: float\n -revenue: float')
            
    
    def get_grouper(self, group_vars, freq):
        
        grouping_list = [pd.Grouper(key = 'stay_date', freq = freq)] 
        if group_vars is not None:
            grouping_list.extend(group_vars)
            
        return grouping_list
            
    
    def group_data(self,  freq = "1D", group_vars = None, status = None):
                   
    
        """Aggregates DataFrame with enough info to create a Booking class from 
        each row, into an aggregated version of a stay date DataFrame, with aggregated 
        revenue, roomnights and ADR, with additional levels of aggregation at user
        discretion
        
        Args: 
            df (DataFrame): DataFrame with info enough to create Booking objects from its rows
            freq (str): date frequency from wich the aggregation will be performed 
            group_vars (list): other columns in the DataFrame for additional levels of aggregation
            status (list): booking status to include in DataFrame (by default includes every estatus)
            
        Returns:
            DataFrame: a DataFrame with aggregated adr, roomnights and revenue
        """
       
        grouping_list = self.get_grouper(group_vars = group_vars, freq = freq)    
    
        # aggregates df    
        grouped_df = self.groupby(grouping_list).agg(
            roomnights = ('roomnights', 'sum'), 
            revenue    = ('revenue', 'sum'))\
            .reset_index()

        # computes DataFrame afterwards because it's a ratio
        grouped_df['adr'] = grouped_df['revenue'] / grouped_df['roomnights']
     
        return StayDataFrame(grouped_df)
    
    def compute_yoy(self, start_date, end_date):
        
            # TODO: ALTERNATIVE WITH shift
    
        start_date = dt.strptime(start_date, "%Y-%m-%d")
        end_date = dt.strptime(end_date, "%Y-%m-%d")
    
        start_date_py = start_date - relativedelta(years = 1)
        end_date_py = end_date - relativedelta(years = 1)
    
        
        df_current_year = self.loc[(self.stay_date >= start_date) & (self.stay_date <= end_date)].copy()
        df_previous_year = self.loc[(self.stay_date >= start_date_py) & (self.stay_date <= end_date_py)].copy()
    
    
        df_previous_year['stay_date'] = df_previous_year.stay_date.apply(lambda x: x + relativedelta(years = 1))
    
        df_previous_year.rename(columns = {'adr': 'adr_py',
                                       'revenue': 'revenue_py', 
                                       'roomnights': 'roomnights_py'}, 
                            inplace = True)
                                       
        
        merging_keys = list(pd.DataFrame(self).drop(['roomnights', 'adr', 'revenue'], axis = 1).columns)
       
            
        df = pd.merge(df_current_year, df_previous_year, how = "left", on = merging_keys)
    
        df['roomnights_diff'] = df.roomnights / df.roomnights_py - 1
        df['adr_diff'] = df.adr / df.adr_py - 1
        df['revenue_diff'] = df.revenue / df.revenue_py - 1
        
        return StayDataFrame(df)
    
        
       # @property
       # def _constructor(self):
       #     return StayDataFrame
    



