from BookingData import Booking
from get_stay_df import get_stay_df
from group_stay_df import group_stay_df
from datetime import date
import unittest

booking = {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'adr': 149.85, 
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

def test_booking_class():
    assert(type(Booking(booking)) == Booking)

    
class TypeErrorTests(unittest.TestCase):

    def test_error_date(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_type_date)) 
        
    def test_error_revenue(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_revenue))
        
    def test_error_adr(self):
        self.assertRaises(TypeError, lambda: Booking(booking_error_adr))
    
if __name__=='__main__':
    unittest.main()
    
