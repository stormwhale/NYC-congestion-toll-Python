Recreation of NYC congestion toll system in python.
There will be 3 parts of the application: EZPass registry, EZPass scanner, and EZPass toll calcculator.
Instructions:
1) Use the EZPass registry to register vehicle plates in the database with Manhattan residency information.
1a) Plate number must be 3 letters followed by 4 digits
2) Use the EZPass scanner tool to scan vehicles with the EZPass transponder as vehicles passes the scanner.
2a) If no plate_db.csv file detect, the programm will generate a temporary file to store the plate information.
2b) If plates scanned are not in the correct format, an error log will be created to track the information. A camera module is used to take pictures of the vehicle.
2c) If plates scanned are not in the database, the vehicle is to be marked 'mail-in' to receive the mail-in toll price.
4) Use the EZPass toll calculator to pull summary or individual vehicle toll summary (coming next) 
