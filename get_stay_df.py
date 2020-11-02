import pandas as pd
from .Booking import Booking

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