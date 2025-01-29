Recreation of NYC congestion toll system in python.
There will be 3 parts of the application: EZPass registry, EZPass scanner, and EZPass toll calcculator
Instructions:
1) use EZPass registry to register license plate number for the car and residency status in the database.
2) use EZPass Scanner to simulate scanning EZPass transponders of cars. If license plate is not in the right format, an error log is created to record the failed plate number.
    If license plate is not found in the plate_db, the license plate will be marked for 'Mail-in' toll price ($13.5 for peak hours and $3.3 for off-peak hours).
3) Use the EZPass calculator to load the 'Toll_zone_log.csv' to calculate the toll for the scanned cars.
    The calculations ignored vehicle types and weekday weekend difference (for now).
    peak hours from 5AM to 9PM = $9 toll; off-peak is from 9PM to 5AM = $3 toll.
    Residents of Manhattan will enjoy 50% discount after the first 10 times entry of the toll zone within a month.

A Sample Toll_zone_log is provided to test the calculations