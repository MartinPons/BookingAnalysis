from BookingData import Booking
from rearrangements import get_stay_df, group_stay_df
import unittest
import numpy as np
import pandas as pd
from datetime import timedelta
from datetime import date, datetime as dt
from dateutil.relativedelta import relativedelta

bookings = pd.read_pickle('hotel_bookings.pkl')

before = dt.now()
daily_data = group_stay_df(bookings, group_vars = ['hotel'])
after = dt.now()

interval = after - before
print("Time elapsed:", round(interval.seconds / 60, 2), "minutes")


# QUE OBJETO ES EL ORIGEN DE yOy?

# UNA SOLA FUNCIÓN BASTA O HAY QUE CREAR VARIAS PARA DIFERENTES INTERVALOS
# DE TIEMPO?

# TENDRIA QUE COGER EN BASE A DIAS PARA HACER FECHAS EXACTAS. EN ALGUN MOMENTO
# TIENE QUE COGER DAILY DATA


before = dt.now()
pr = Booking(bookings.iloc[12]).expand()
after = dt.now()

(after - before).seconds

daily_data.resample('M', on = "stay_date")[['roomnights', 'revenue']].sum()

daily_data.stay_date.dt.datetime()


def compute_yoy(df, start_date, end_date, freq = None, group_vars = None):
   
    # TODO: ALTERNATIVE WITH shift
    
    start_date = dt.strptime(start_date, "%Y-%m-%d")
    end_date = dt.strptime(end_date, "%Y-%m-%d")
    
    start_date_py = start_date - relativedelta(years = 1)
    end_date_py = end_date - relativedelta(years = 1)
    
        
    if group_vars is not None and freq is not None:
        grouping_list = [pd.Grouper(key = 'stay_date', freq = freq)] 
        grouping_list.extend(group_vars)
        
        df = df.groupby(grouping_list).agg(roomnights = ('roomnights', 'sum'), 
                                           revenue    = ('adr', 'sum'))\
        .reset_index()
        
        df['adr'] = df.roomnights - df.revenue
    
   #  df['stay_date'] = df.stay_date.apply(lambda x: x.date())
    
    df_current_year = df.loc[(df.stay_date >= start_date) & (df.stay_date <= end_date)].copy()
    df_previous_year = df.loc[(df.stay_date >= start_date_py) & (df.stay_date <= end_date_py)].copy()
    
    
    df_previous_year['stay_date'] = df_previous_year.stay_date.apply(lambda x: x + relativedelta(years = 1))
    
    df_previous_year.rename(columns = {'adr': 'adr_py',
                                       'revenue': 'revenue_py', 
                                       'roomnights': 'roomnights_py'}, 
                            inplace = True)
                                       
    merging_keys = ['stay_date']
    
    if group_vars is not None:
        merging_keys.extend(group_vars)
  
    df = pd.merge(df_current_year, df_previous_year, how = "left", on = merging_keys)
    
    df['roomnights_diff'] = df.roomnights / df.roomnights_py - 1
    df['adr_diff'] = df.adr / df.adr_py - 1
    df['revenue_diff'] = df.revenue / df.revenue_py - 1
    
    return df
    

