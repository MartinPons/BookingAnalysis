import numpy as np
import pandas as pd
from datetime import timedelta, datetime as dt

booking_df_sample = pd.read_pickle('bookings_df_sample.pkl')
bookings = pd.read_csv('hotel_bookings.csv')


# arrival_date
bookings["checkin_date"] = bookings["arrival_date_year"].astype(str) + bookings["arrival_date_month"] + bookings["arrival_date_day_of_month"].astype(str)
bookings["checkin_date"] = bookings["checkin_date"].apply(lambda x: dt.strptime(x, "%Y%B%d"))

# length_of_stay as the sum of stays in weekdays and stays in weekends
bookings['los'] = bookings['stays_in_weekend_nights'] + bookings['stays_in_week_nights']

# intervals for lenght_of_stay
bookings['los_int'] = pd.cut(bookings.los, bins = range(1,30, 2))

# departure date
bookings['checkout_date'] = bookings.apply(lambda x: x.checkin_date + timedelta(days = x.los), axis = 1)

# booking date
bookings['booking_date'] = bookings.apply(lambda x: x.checkin_date - timedelta(days = x.lead_time), axis = 1)
bookings['booking_month'] = bookings['booking_date'].apply(lambda x: x.strftime('%b'))

# revenue = adr * length of stay
bookings['revenue'] = [los * adr if los > 0 else adr for los, adr in zip(bookings['los'], bookings['adr'])]

# lead_time_weeks
bookings['lead_time_weeks'] = bookings['lead_time'].apply(lambda x: x // 7)

# weekday check in and check out
bookings['weekday_checkin'] = bookings['checkin_date'].dt.weekday
bookings['weekday_checkout'] = bookings['checkout_date'].dt.weekday


# creation of variable group
bookings['group'] = bookings.market_segment == "Groups"

bookings['booking_id'] = bookings.groupby('hotel').cumcount()
bookings.rename(columns = {'reservation_status':'status'}, inplace = True)
bookings['booking_date'] = bookings.booking_date.apply(lambda x: x.date())
bookings['checkin_date'] = bookings.checkin_date.apply(lambda x: x.date())
bookings['checkout_date'] = bookings.checkout_date.apply(lambda x: x.date())

Booking(bookings.iloc[0])

bookings.to_pickle('hotel_bookings.pkl')
    
    