BookingAnalysis is a Python library at a very early stage of development. Its main purpose is to automatize common operations performed with booking reservations related data, like modifying booking features, aggregate a DataFrame of bookings into different grouping time windows, and make YoY, YTD comparisons both numerically and visually, or creating booking paces.

At this stage of development, the library is just composed of a **Booking class** with inherits from pandas Series, and functions to rearrange and aggregate data.
For now, its most interesting functionality is the method **expand**, which rearranges a Booking instance into a DataFrame of stay days, from which the rearrangement functions operate.

Most of the aforementioned features are still pending.
