import pandas as pd
from BookingData import Booking

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


def group_stay_df(df,  freq = "1D", group_vars = None, status = None):
    
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