from BookingData import Booking
from get_stay_df import get_stay_df
from group_stay_df import group_stay_df
from datetime import date
from datetime import datetime as dt, timedelta
import unittest
import numpy as np
import pandas as pd

booking_df_sample = pd.read_csv('booking_df_sample.csv', 
                                parse_dates = ['booking_date', 'checkin_date', 'checkout_date'])

booking_df_sample['booking_date'] = booking_df_sample['booking_date'].apply(lambda x: x.date())
booking_df_sample['checkin_date'] = booking_df_sample['checkin_date'].apply(lambda x: x.date())
booking_df_sample['checkout_date'] = booking_df_sample['checkout_date'].apply(lambda x: x.date())

booking_adr = {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'adr': 149.85, 
    'meal': 'TI', 
    'status': 'confirmed'}

booking_revenue= {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'revenue': 1505.76, 
    'meal': 'TI', 
    'status': 'confirmed'}


booking_error_type_date = {
    'booking_id': "B1",
    'booking_date': "2020-01-01", 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'adr': 149.85, 
    'meal': 'TI', 
    'status': 'confirmed'}

booking_error_revenue = {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'revenue': "1246.56", 
    'meal': 'TI', 
    'status': 'confirmed'}


booking_error_adr = {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'revenue': "126.56", 
    'meal': 'TI', 
    'status': 'confirmed'}


 
class TypeErrorTests(unittest.TestCase):
    
    def test_booking_class(self):
        self.assertIsInstance(Booking(booking_adr), Booking)

    def test_error_date(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_type_date)) 
        
    def test_error_revenue(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_revenue))
        
    def test_error_adr(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_adr))
        
        
class TestMethods(unittest.TestCase):
    
    def test_get_los(self):
        self.assertTrue(Booking(booking_adr).get_los() == 6)
        
    def test_get_adr(self):
        self.assertTrue(Booking(booking_revenue).get_adr() == 1505.76 / 6)
        
    def test_get_revenue(self):
        self.assertTrue(Booking(booking_adr).get_revenue() == 149.85 * 6)
        
    def test_set_checkin_date_changedate(self):
        
        booking_checkin_changed = Booking(booking_adr)
        booking_checkin_changed.set_checkin_date(date(2020, 6, 2))
        
        self.assertTrue((booking_checkin_changed.get_los() == 5) &
                        (booking_checkin_changed.get_adr() == booking_checkin_changed.revenue / 5))
        
    def test_set_checkin_date_changelos(self):
        
        booking_checkin_changed = Booking(booking_adr)
        booking_checkin_changed.set_checkin_date(shift_days = 2)
        
        self.assertTrue((booking_checkin_changed.get_los() == 4) &
                        (booking_checkin_changed.get_adr() == booking_checkin_changed.revenue / 4))
        
    def test_set_checkin_date_changelosnegative(self):
        
        booking_checkin_changed = Booking(booking_adr)
        booking_checkin_changed.set_checkin_date(shift_days = -2)
        
        self.assertTrue((booking_checkin_changed.get_los() == 8) &
                        (booking_checkin_changed.get_adr() == booking_checkin_changed.revenue / 8))
   

    def test_set_checkout_date_changedate(self):
        
        booking_checkout_changed = Booking(booking_adr)
        booking_checkout_changed.set_checkout_date(date(2020, 6, 8))
        
        self.assertTrue((booking_checkout_changed.get_los() == 7) &
                        (booking_checkout_changed.get_adr() == booking_checkout_changed.revenue / 7))     
 
    def test_set_checkout_date_changelos(self):
        
        booking_checkout_changed = Booking(booking_adr)
        booking_checkout_changed.set_checkout_date(shift_days = 2)
        
        self.assertTrue((booking_checkout_changed.get_los() == 8) &
                        (booking_checkout_changed.get_adr() == booking_checkout_changed.revenue / 8))
        
    def test_set_checkout_date_changelosnegative(self):
        
        booking_checkout_changed = Booking(booking_adr)
        booking_checkout_changed.set_checkout_date(shift_days = -2)
        
        self.assertTrue((booking_checkout_changed.get_los() == 4) &
                        (booking_checkout_changed.get_adr() == booking_checkout_changed.revenue / 4))
        
        
class TestExpand(unittest.TestCase):
    
    def test_rows(self):
        booking = Booking(booking_df_sample.iloc[4])
        bdf = booking.expand()
        
        self.assertTrue(bdf.shape[0] == 2)
        
    def test_rows_daystay(self):
        booking = Booking(booking_df_sample.iloc[0])
        bdf = booking.expand()
        
        self.assertTrue(bdf.shape[0] == 1)
        
        
    
if __name__=='__main__':
    unittest.main()
    
    
    
