# This is the function to calculate the toll:
# from 0500 to 2100, the price is $9
# from 2101-0459, the price is %2.25
# if residents, after the first 10 trips in a month, the toll is 50%off
# Mail-in price = $13.5
from datetime import date as dt, datetime
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog
import os
import csv

# csv to pandas data frame:
file_path = ""


# Make a function that defines and checks the csv file that is loaded:
def load_file():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Load_toll_log", filetypes=(("csv files", "*.csv"),)
    )

    def check_file(file_path):
        required_headers = ["license", "time", "date", "resident"]

        try:
            with open(file_path) as file:
                reader = csv.reader(file)
                header = next(reader)
                header = [col.strip() for col in header]
                for row in header:
                    if header == required_headers and len(row) == len(required_headers):
                        return True

        except Exception as e:
            messagebox.showerror("Format Error", f"The loaded File has {e} error")
            return False

    if file_path:
        if check_file(file_path):
            messagebox.showinfo(
                "File loaded",
                "File loaded successfully!\nPlease choose different modes from below.",
            )
            toll(file_path)
        else:
            messagebox.showerror(
                "Error",
                "File format is incorrect. Please ensure the file is 'Toll_zone_log.csv.",
            )
            return


def toll(file_path):
    df = pd.read_csv(file_path, header=0)

    # define time range for regular price:
    peak_start = datetime.strptime("05:00:00", "%H:%M:%S")
    peak_end = datetime.strptime("21:00:00", "%H:%M:%S")

    def get_toll_price(row):  # this determines if the toll is $9 or $2.25
        time = datetime.strptime(row["time"], "%H:%M:%S")
        if row["resident"] == "Mail-in":
            if peak_start <= time <= peak_end:
                return 13.5
            else:
                return 3.3
        else:
            if peak_start <= time <= peak_end:
                return 9
            else:
                return 2.25

    # charge only once a day:
    df["toll_price"] = df.apply(
        get_toll_price,
        axis=1,  # axis=1 for rows, axis =0 for columns
    )  # This calculates the toll based on time of the day

    df.sort_values(["license", "date", "time"], ascending=True, inplace=True)
    df["charge_once_a_day"] = df.duplicated(
        subset=["license", "date"], keep="first"
    )  # create a helper column to distiguish multiple entries in one day
    df.loc[df["charge_once_a_day"] == True, "toll_price"] = (
        0  # change the toll price for all "True", which are duplicates to 0 toll
    )

    # Giving 50% discount to residents who enter manhattan more than 10 times in a month. The discount starts at the eleventh entry:
    df["date"] = pd.to_datetime(
        df["date"], format="%Y-%m-%d"
    )  # making sure the date is in the right format
    df["month_entry"] = pd.to_datetime(df["date"]).dt.to_period(
        "M"
    )  # This extracts the year and month of the date
    df.sort_values(["license", "month_entry"], inplace=True)  # arrange the dataframe
    df["count"] = (
        df.groupby(["license", "month_entry"]).cumcount() + 1
    )  # Creates a helper column to count the number of entry within a month

    df["toll_price"] = df.apply(
        lambda row: row["toll_price"] * 0.5
        if row["resident"] == "Y" and row["count"] > 10
        else row["toll_price"],
        axis=1,
    )

    return df


# different modes selections:
def all_data():
    if file_path:
        result = (
            toll(file_path)
            .groupby(["license", "date", "time", "resident"])["toll_price"]
            .sum()
            .reset_index()
        )
        load_text.delete(1.0, tk.END)
        load_text.insert(tk.END, result)
    else:
        messagebox.showwarning("Missing toll file", "Please load toll_log_.csv first.")


def monthly():
    if file_path:
        result = (
            toll(file_path)
            .groupby(["license", "month_entry", "resident"])["toll_price"]
            .sum()
            .reset_index()
        )
        load_text.delete(1.0, tk.END)
        load_text.insert(tk.END, result)
    else:
        messagebox.showwarning("Missing toll file", "Please load toll_log_.csv first.")


def select():
    plate_num = plate_entry.get().upper()
    # Checks entry format:
    if len(plate_num) != 7 and not plate_num[:3].isalpha() and plate_num[3:].isdigit():
        messagebox.showwarning(
            "Entry error",
            "License plate numbers have 3 alphabets followed by 4 digits only",
        )
        return

    df = toll(file_path)
    # Checks if any plate number match with the entry number:
    result = df[df["license"] == plate_num]

    if result.empty:
        messagebox.showwarning(
            "Not found", "License plate number not found in database"
        )
        return

    result = (
        result.groupby(["license", "month_entry"])["toll_price"].sum().reset_index()
    )
    load_text.delete(1.0, tk.END)
    load_text.insert(tk.END, result)


def EZPass_calculator():
    # GUI function:
    root = tk.Tk()
    root.geometry("680x600")
    root.title("EZPass calculator")

    load_btn = tk.Button(
        root, text="Load Toll_zone_log.csv", command=load_file, font="Times 10"
    )
    all_btn = tk.Button(root, text="Display all toll data", command=all_data)
    monthly_btn = tk.Button(root, text="Monthly Statment", command=monthly)
    select_btn = tk.Button(root, text="Search Plate Number", command=select)

    global load_text
    load_text = tk.Text(root, width=80, height=28)

    # Entry area for plate search:
    global plate_entry
    plate_entry = tk.Entry(root, width=20)
    plate_entry_label = tk.Label(root, text="Please enter plate number:")

    # positions:
    load_btn.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="e")

    all_btn.grid(row=2, column=1, padx=5, pady=10, sticky="ew")
    monthly_btn.grid(row=2, column=2, padx=5, pady=10, sticky="ew")
    select_btn.grid(row=2, column=3, padx=5, pady=10, sticky="ew")
    plate_entry.grid(row=3, column=4, padx=5, pady=5, sticky="e")
    plate_entry_label.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    load_text.grid(row=4, column=0, padx=10, pady=5, columnspan=5, sticky="nsew")
    load_btn.grid(row=0, column=0, padx=10, pady=10)
    root.mainloop()


EZPass_calculator()
