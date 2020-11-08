## Booking Analysis

Author: Martín Pons

### Description

BookingAnalysis is a **Python package** at a very early stage of development. Its main purpose is to automatize common operations performed with booking reservations related data, like modifying booking features, aggregate a DataFrame of bookings into different time windows, make YoY, YTD comparisons both numerically and visually, or creating booking paces.

At this stage of development, the library is just composed of a **Booking class** with inherits from pandas Series, and functions to rearrange and aggregate data.
For now, its most interesting functionality is the method **expand**, which rearranges a Booking instance into a DataFrame of stay days, from which the rearrangement functions operate.

Most of the aforementioned features are still pending.

### File description

- BookingData.py: code containing the **Booking** class
- rearrangements.py: code containing functions **get_stay_df** and **group_stay_df** to rearrange and aggregate booking related DataFrames using the Booking class
- licencse.txt: terms of use
- __init__.py: package init file
- setup.py: package setup
-bookings_df_sample.pkl: booking sample data extracted from [Hotel Booking Demand Datasets](https://www.sciencedirect.com/science/article/pii/S2352340918315191), by Nuno Antonio, Ana Almeida, and Luis Nunes for Data in Brief, Volume 22, February 2019
- tests: folder with files to test the Booking class and the rearrangement functions


