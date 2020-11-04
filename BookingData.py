import pandas as pd
from datetime import timedelta
from datetime import date


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
        
        # checks data contains required fields
        if any(map(lambda x: x not in self.index, booking_indexes)) or (not (("revenue" in self.index) ^ ("adr" in self.index))):  
            raise ValueError("Series must contain the following index values:\n -booking_id\n -booking_date\n -checkin_date\n -checkout_date\n And either 'revenue' or 'adr'. But not both")
       
        # checks date types
        if any(map(lambda x: type(x) != date, [self.booking_date, self.checkin_date, self.checkout_date])):
                raise TypeError("All date related fields must be of type date")
       
                
        # compute additional booking data from the given data
        self['los'] = self.get_los()
        
        if 'adr' not in self.index:
            if self.revenue != float:
                raise TypeError("'revenue' must be of type float")
            self['adr'] = self.get_adr()
            
        if 'revenue' not in self.index:
            if self.adr != float:
                raise TypeError("'adr' must be of type float")
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