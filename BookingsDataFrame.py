# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import numpy as np
import pandas as pd
from pandas import DataFrame
from datetime import datetime as dt
from datetime import timedelta
from datetime import date


bookings = pd.read_csv('hotel_bookings.csv')

bookings['los'] = bookings['stays_in_week_nights'] + bookings['stays_in_weekend_nights']

bookings['arrival_date'] = bookings.apply(lambda x: dt.strptime(str(x.arrival_date_year) + 
                                                             x.arrival_date_month +
                                                             str(x.arrival_date_day_of_month),
                                                             "%Y%B%d"), 
                                          axis = 1)

bookings['exit_date'] = bookings.apply(lambda x: x.arrival_date + timedelta(days = x.los), 
                                       axis = 1)

bookings['booking_date'] = bookings.apply(lambda x: x.arrival_date - timedelta(days = x.lead_time), 
                                          axis = 1)


class Booking(pd.Series):
    
    def __init__(self, data, booking_id, booking_date, checkin_date, checkout_date, revenue = None, adr = None, *args, **kwargs):
        
        if adr is None and revenue is None:
            raise ValueError("You must provide either a string corresponding to the index for the adr or the revenue")
            
        if adr is not None and revenue is not None:
            raise ValueError("You must only provide either a string corresponding to the index for the adr or the revenue")
    
    
        data['los'] = (data[checkout_date] - data[checkin_date]).days
           
        if revenue is not None:
            data['adr'] = data[revenue] / data['los']
            data['revenue'] = data.pop(revenue)
        
        if adr is not None:
            data['revenue'] = data[adr] * data['los']
            data['adr'] = data.pop(adr)
           
        
        # super(pd.Series, self).__init__(data, *args, **kwargs)
        pd.Series.__init__(self, data)
        
        self.rename(index = {booking_id: 'booking_id',
                             booking_date: 'booking_date', 
                             checkin_date: 'checkin_date', 
                             checkout_date: 'checkout_date'}, 
                    inplace = True)
                
    @property
    def _constructor(self):
        return Booking
    
    @property
    def _constructor_expanddim(self):
        return BookingsDataFrame
    
    
    def expand_booking(self, group_vars = None):
        # creates a range of consecutive dates taking arrival_date as first date 
        # and arrival_date + los as the last date. As we count nights not days, last day is substracted
        # exect when length of stay is 0
        
        los = self.los
        checkin_date = self.checkin_date
        
        days = pd.date_range(checkin_date, 
                             checkin_date + timedelta(days = int(los - 1 * (los > 0))))
        
        def expand_point(point):
            return np.repeat(self[point], los + (los == 0) * 1)
        
        expanded_booking = pd.DataFrame(data = {'booking_id': expand_point('booking_id'),
                                   'stay_date': days,
                                   'roomnights': np.repeat((los > 0) * 1, 
                                                           los + (los == 0) * 1), 
                                   'revenue': expand_point("adr")
                               })
        
        # Include additional columns in the data frame
        df_add_cols = pd.DataFrame()
        
        if group_vars is not None:
            for name in group_vars:
                df_add_cols[name] = expand_point(name)
                
        expanded_booking = pd.concat([expanded_booking, df_add_cols], axis = 1)
        
        return expanded_booking
        
    
class BookingsDataFrame(pd.DataFrame):
       
    def __init__(self, data, booking_id, booking_date, checkin_date, checkout_date, revenue = None, adr = None, *args, **kwargs):
        
        if adr is None and revenue is None:
            raise ValueError("You must provide either a string corresponding to the index for the adr or the revenue")
            
        if adr is not None and revenue is not None:
            raise ValueError("You must only provide either a string corresponding to the index for the adr or the revenue")

        data['los'] = data[checkout_date] - data[checkin_date]
        data['los']= data['los'].apply(lambda x: x.days)
           
        if revenue is not None:
            data['adr'] = data[revenue] / data['los']
            data['revenue'] = data.pop(revenue)
        
        if adr is not None:
            data['revenue'] = data[adr] * data['los']
            data['adr'] = data.pop(adr)
            
        pd.DataFrame.__init__(self, data, *args, **kwargs)
       
        self.rename(columns = {booking_id: 'booking_id',
                               booking_date: 'booking_date', 
                               checkin_date: 'checkin_date', 
                               checkout_date: 'checkout_date'}, 
                    inplace = True)
        
        
    # @property
    # def _constructor(self,  booking_id, booking_date, checkin_date, checkout_date, revenue = None, adr = None, *args, **kwargs):
    #     return BookingsDataFrame
    
    @property
    def _constructor_sliced(self):
        return Booking(
            booking_id = "booking_id", 
                       booking_date = "booking_date", 
                       checkin_date = "checkin_date", 
                       checkout_date = "checkout_date", 
                       revenue = "revenue")
            
# pr = BookingsDataFrame(bookings, "id", "booking_date", "arrival_date", "exit_date", adr = "adr")


def read_bookings_csv(file, booking_date, checkin_date, checkout_date, price, meal = None):
    
    bdf = pd.read_csv(file)
    
    return BookinsDataFrame(bdf, booking_date, checkin_date, checkout_date, price, meal = None)


################# VERSION 2 #######################
    
AHORA HAY QUE ESCRIBIR LOS DOCSTRINGS!!!!


class Booking(pd.Series):
    
    """The Booking class parses data from a pandas Series with specific
    inputs that shoud exist in booking data, and automatizes common operations"""
    
    def __init__(self, *args, **kwargs):
        
        """Method for initializing  a Booking object
        
        Args: 
             *args: Variable length argument list.
             **kwargs: Arbitrary keyword arguments.
             
        Attrubutes:
            None
        """
            
        pd.Series.__init__(self, *args, **kwargs)
        
        # checks whether basic booking information is in the DataFrame, with specific names
        # stops execution if not
        booking_indexes = ['booking_id', 
                           'booking_date', 
                           'checkin_date', 
                           'checkout_date',
                           'status']        
        if any(map(lambda x: x not in self.index, booking_indexes)) or (not (("revenue" in self.index) ^ ("adr" in self.index))):  
            raise ValueError("Series must contain the following index values:\n -booking_id\n -booking_date\n -checkin_date\n -checkout_date\n And either 'revenue' or 'adr'. But not both")
       
        
        # compute additional booking data from the given data
        self['los'] = self.get_los()
        
        if 'adr' not in self.index:
            self['adr'] = self.get_adr()
            
        if 'revenue' not in self.index:
            self['revenue'] = self.get_revenue()
    
    
    def get_los(self):
        
        """Computes the booking length of stay"
        
        Args:
            None
        Returns:
            int: booking lengh of stay
        """
                 
        return (self.checkout_date - self.checkin_date).days
 
    
    def get_adr(self):
        
        """Computes the booking ADR
        
        Args: 
            None
        Returns:
            float: booking ADR
        """
 
        if self.los == 0:
            return self.revenue
        else:
            return self.revenue / self.los
        
        
    def get_revenue(self):
        
         """Computes the booking revenue
        
        Args: 
            None
        Returns:
            float: booking revenue
        """
        
        if self.los == 0:
            return self.adr
        else:
            return self.adr * self.los
        
    
    def set_checkin_date(self, new_checkin_date = None, shift_days = 0, modify_kpi = "adr"):
        
        """Modifies booking checkin date by either setting a new date or adding or substracting
        days from the original date. it also modifies length of stay as a subproduct
        
        Args:
            new_checkin_date (date): new booking checkin date
            shift_dats (ind): shift in days relative to original date
            modify_kpi (str): accepts values "adr" or "revenue". The one kpi that will be modified due to los change
            
        Returns:
            None
        """
        
        # modifies date according to given argument
        if new_checkin_date is not None:
            self.checkin_date = new_checkin_date
        else:
            self.checkin_date = self.checkin_date + timedelta(days = shift_days)
            
        # los has to be modified
        self.los = self.get_los()
        
        # also modifies either revenue or adr because change in los
        if modify_kpi == "revenue":
            self.revenue = self.get_revenue()
        elif modify_kpi == "adr":
            self.adr = self.get_adr()
        else:
            raise ValueError("argument modify_kpi must be either 'revenue', or 'adr'")


    def set_checkout_date(self, new_checkout_date = None, shift_days = 0, modify_kpi = "adr"):
        
         """Modifies booking checkout date by either setting a new date or adding or substracting
        days from the original date. it also modifies length of stay as a subproduct
        
        Args:
            new_checkin_date (date): new booking checkin date
            shift_dats (ind): shift in days relative to original date
            modify_kpi (str): accepts values "adr" or "revenue". The one kpi that will be modified due to los change
            
        Returns:
            None
        """
        
        # modifies date according to given argument
        if new_checkout_date is not None:
            self.checkout_date = new_checkout_date
        else:
            self.checkout_date = self.checkout_date + timedelta(days = shift_days)
        
        # los has to be modified
        self.los = self.get_los()
      
        # also modifies either revenue or adr because change in los
        if modify_kpi == "revenue":
            self.revenue = self.get_revenue()
        elif modify_kpi == "adr":
            self.adr = self.get_adr()
        else:
            raise ValueError("argument modify_kpi must be either 'revenue', or 'adr'")
        
    def expand(self, group_vars = None):
        
        """Creates a DataFrame of stay dates from a Booking by constructing a 
        range of consecutive dates taking arrival_date as first date and 
        arrival_date + los as the last date. Adds the basic booking data to 
        the DataFrame as well as additional data selected by the user
        
        Args:
            group_vars (list): list of indexes in Bookings that the user wants to include in the DataFrame
            
        Returns:
            DataFrame: a DataFrame of stay dates
        """
        
        los = self.get_los()
        checkin_date = self.checkin_date
        
        # range of stay dates
        days = pd.date_range(checkin_date,                    
                             # for day stay bookings we want one date, not 0.
                             checkin_date + timedelta(days = int(los - 1 * (los > 0))))
          
        # empty data frame to be filled with booking columns
        expanded_booking = pd.DataFrame()
        
        expanded_booking['stay_date'] = days
        expanded_booking['booking_date'] = self.booking_date
        expanded_booking['booking_id'] = self.booking_id
        
        # one day of stay is one roomnight exept in the case of a day stay booking
        expanded_booking['roomnights'] = (los > 0) * 1
        expanded_booking['adr'] = self.adr
        expanded_booking['status'] = self.status
        
        # addition of variables selected by user to the DataFrame
        if group_vars is not None:
            for name in group_vars:
                expanded_booking[name] = self[name]
                    
        return expanded_booking 
    

rows_sample = 1000
bookings_sample = bookings.head(rows_sample)
bookings_sample.loc[:, 'id'] = range(rows_sample)

bookings_sample.rename(columns = {'arrival_date': 'checkin_date', 
                                  'exit_date': 'checkout_date',
                                  'id': 'booking_id',
                                  'reservation_status': 'status'}, 
                       inplace = True)


booking = {
    'booking_id': "B1",
    'booking_date': date(2020, 1, 1), 
    'checkin_date': date(2020, 6, 1), 
    'checkout_date': date(2020, 6, 7), 
    'adr': 149.85, 
    'meal': 'TI', 
    'status': 'confirmed'}

booking_series = pd.Series(booking)

bk1 = Booking(booking)

bk1.set_checkin_date(date(2020, 6, 5))
bk1.set_checkout_date(date(2020, 6, 10))

bk1.set_checkin_date(date(2020, 6, 2), "revenue")
bk1.set_checkin_date(date(2020, 6, 7), "revenue")



def get_stay_df(df, group_vars = None, status = None):
    
    """Transforms a DataFrame with booking information to a stay date 
    DataFrame. Each row has to include infthe basic info for it to be 
    converted in a Booking object
    
    Args:
        df (DataFrame): DataFrame with booking information 
        group_vars (list): additional vars from df to be include in the output
        status (list): booking status to include in DataFrame (by default includes every estatus)
        
    Returns:
        DataFrame: a DataFrame where each booking has been extended into one row
        for every stay day
    
    """
    
    # initiates list of DataFrames to save extended booking DataFrames
    bookings_list = []
    
    # transforms each row in the DataFrame into a extended booking DataFrame
    for row in range(df.shape[0]):
        booking = Booking(df.iloc[row])  
        
        # checks status filter
        if status is not None and booking.status not in status:
            next   
        else:
            # appends extended booking df to booking_list
            bookings_list.append(booking.expand(group_vars = group_vars))
    
    
    bookings_df = pd.concat(bookings_list, axis = 0)
    
    return bookings_df
    
get_stay_df(bookings_sample, ['meal', 'distribution_channel'])   

             
def group_stay_data(df,  freq = "1D", group_vars = None, status = None):
    
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
    
    # transforms df into a stay date DataFrame
    bookings_df = get_stay_df(df, group_vars = group_vars, status = status)
    
    # creates list with all levels of aggregation including date aggregation
    grouping_list = [pd.Grouper(key = 'stay_date', freq = freq)] 
    if group_vars is not None:
        grouping_list.extend(group_vars)
    
    # aggregates df    
    daily_df = bookings_df.groupby(grouping_list).agg(
        roomnights = ('roomnights', 'sum'), 
        revenue    = ('adr', 'sum'))\
        .reset_index()
    
    # computes DataFrame afterwards because it's a ratio
    daily_df['adr'] = daily_df['revenue'] / daily_df['roomnights']
        
    return daily_df


group_stay_data(bookings_sample)
group_stay_data(bookings_sample, group_vars = ['meal', 'is_repeated_guest'], status = ['Canceled'])


