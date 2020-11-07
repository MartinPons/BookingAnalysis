from BookingData import Booking
from rearrangements import get_stay_df, group_stay_df
import unittest
import numpy as np
import pandas as pd
from datetime import timedelta

booking_df_sample = pd.read_pickle('bookings_df_sample.pkl')
booking_df_minisample = booking_df_sample.iloc[1:100]


class TestStayDF(unittest.TestCase):
    
    def test_stay_df_class(self):
        
        bdf = get_stay_df(booking_df_minisample)
        self.assertIsInstance(bdf, pd.DataFrame)
        
    def test_stay_df_groupvars(self):
        bdf = get_stay_df(booking_df_minisample, ['agent', 'customer_type'])
        self.assertTrue(bdf.shape[1] == 8)
        
    def test_group_df_class(self):
        gbdf = group_stay_df(booking_df_minisample)
        self.assertIsInstance(gbdf, pd.DataFrame)
        
    def test_group_df_rows(self):
        min_date = booking_df_minisample['checkin_date'].min()
        max_date = booking_df_minisample['checkout_date'].max()
        n_rows = (max_date - min_date).days
        
        gbdf = group_stay_df(booking_df_minisample)
        
        self.assertTrue(n_rows == gbdf.shape[0])
        
    def test_group_df_month(self):

        gbdf = group_stay_df(booking_df_sample, freq = "1M")
        self.assertTrue((gbdf['stay_date'][1] - gbdf['stay_date'][0]).days in [28, 29, 30, 31])


if __name__=='__main__':
    unittest.main()
    
    

