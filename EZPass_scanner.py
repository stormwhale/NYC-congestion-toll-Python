from datetime import date as dt, datetime
import os
import tkinter as tk
from tkinter import messagebox
import csv


# This is the EZ pass scanner:
def EZscanner_gui():
    # define GUI parameters:
    root = tk.Tk()
    root.geometry("800x250")
    root.title("EZPass Scanner")
    plate_num = tk.StringVar()  # for receiving plate number inputs

    def EZscanner():
        plate = plate_num.get().upper()  # Ensures all inputs are upper case
        current_date = dt.today()
        current_time = datetime.now().strftime("%H:%M:%S")

        # Determines if the scanned plate matches with the plate format:
        if len(plate) != 7 or not plate[:3].isalpha() or not plate[3:].isdigit():
            messagebox.showerror(
                "Invalid plate number",
                "Invalid plate number detected.\n Unable to scan the correct plate number.\n Capturing plate number with camera.",
            )
            plate_num.set("")
            # This is creating an error log to track all scanned plates with mismatched formats:
            if not os.path.exists("Error_log.csv"):
                with open("Error_log.csv", "w") as err:
                    err.write("License,date,time\n")
            with open("Error_log.csv", "a") as err:
                err.write("{},{},{}\n".format(plate, current_date, current_time))
            return

        # Checks if license plate database file exists:
        # It will create a temporary file if the registry is not found
        lic_data = "plate_db.csv"  # license plate database created with the EZPass registry.exe
        unreg_lic_data = "unreg_plate_db.csv"  # keeping a separate log for unregistered license plate for future review
        lic_data_exists = os.path.exists(lic_data)
        unreg_lic_data_exists = os.path.exists(unreg_lic_data)
        if not lic_data_exists:
            messagebox.showwarning(
                "Database file missing",
                "'plate_db.csv' file is missing.\n Please use EZ registry.exe to register plate numbers.\n A temporary new database file will be created.\n Toll log will assign plate as 'N' for Residency",
            )
            if not unreg_lic_data_exists:
                with open(unreg_lic_data, "w") as ureg_lic:
                    ureg_lic.write("Licence,resident\n")
            with open(unreg_lic_data, "a") as ureg_lic:
                ureg_lic.write("{},unknown\n".format(plate))
            plate_num.set("")
            # Create or writes the entry of the unregistered plate:
            if not os.path.exists("Toll_zone_log.csv"):
                with open("Toll_zone_log.csv") as toll:
                    toll.write("license,time,date,resident\n")
            with open("Toll_zone_log.csv", "a") as toll:
                toll.write(
                    "{},{},{},{}\n".format(plate, current_time, current_date, "N")
                )

        # This is logging the date and time of the scanned plate:
        with open(lic_data, "r") as lic:
            reader = csv.reader(lic)
            next(reader)
            for row in reader:
                if row[0].strip() == plate:
                    if not os.path.exists("Toll_zone_log.csv"):
                        with open("Toll_zone_log.csv", "w") as toll:
                            toll.write("license,time,date,resident\n")
                    with open("Toll_zone_log.csv", "a") as toll:
                        toll.write(
                            "{},{},{},{}\n".format(
                                plate, current_time, current_date, row[1]
                            )
                        )
                        messagebox.showinfo(
                            "Success", "Scan completed for {}!".format(plate)
                        )
                        plate_num.set("")
                        return
            messagebox.showerror(
                "Not Found",
                f"{plate} not found in database.\n Switching to optical mode to capture plate number.",
            )
            if not os.path.exists("Toll_zone_log.csv"):
                with open("Toll_zone_log.csv", "w") as toll:
                    toll.write("license,time,date,resident\n")
            with open("Toll_zone_log.csv", "a") as toll:
                toll.write(
                    "{},{},{},{}\n".format(plate, current_time, current_date, "Mail-in")
                )
                messagebox.showinfo(
                    "Success",
                    "Photo of plate {} is captured!\n Owner of the vehicle will receive mail-in toll price.".format(
                        plate
                    ),
                )
                plate_num.set("")

    scan_bar_label = tk.Label(root, text="EZPass Scanner", font="Times 20")
    scan_bar_entry = tk.Entry(
        root, text="", width=15, textvariable=plate_num, font="Times 20"
    )
    scan_btn = tk.Button(root, text="Scan", command=EZscanner, font="Times 20")
    scanner_instruction_label = tk.Label(
        root,
        text='Instructions on EZPass Scanner:\n1) If the scanned plate does not match the plate format, an error log is created.\n2) Please ensure "plate_db.csv" exists for the scanner to reference the residency status.\n3) If plate number is not found in plate database, vehicle owner will be charged with mail-in toll price.',
        justify="left",
    )

    scan_bar_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    scan_bar_entry.grid(row=1, column=0, padx=10, pady=10, sticky="n")
    scan_btn.grid(row=2, column=0, padx=40, pady=40, sticky="w")
    scanner_instruction_label.grid(row=1, column=10)

    return root.mainloop()


EZscanner_gui()
