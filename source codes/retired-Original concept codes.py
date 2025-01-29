from datetime import date as dt
from datetime import datetime
import datetime
import pandas as pd
import os


# This is the EZ pass scanner:
def EZscanner_gui():
    def EZscanner():
        file_path = "plate_history.csv"
        file_path_exists = os.path.exists(
            file_path
        )  # checks if the file is already there

        while True:  # this ensures the entry is restricted to the format
            num = input("Scan license plate:").upper()
            if len(num) == 7 and num[:3].isalpha() and num[3:].isdigit():
                break
            else:
                print(
                    "License plate numbers have 3 alphabets followed by 4 digits only"
                )

        while True:  # this ensures the entry is only Y or N
            resident = input("Are you resident? (Y/N?)").upper()
            if resident in ["Y", "N"]:
                break
            else:
                print("Please enter only Y or N")

        time = datetime.now().strftime("%H:%M:%S")
        current_date = dt.today()
        with open("plate_history.csv", "a") as file:
            if not file_path_exists:
                file.write("license,time,date,resident\n")
            file.write("{},{},{},{}\n".format(num, time, current_date, resident))
        return print("Scan completed!")


# This is the function to calculate the toll:
# from 0500 to 2100, the price is $9
# from 2101-0459, the price is %2.25
# if residents, after the first 10 trips in a month, the toll is 50%off


# csv to pandas data frame:
def toll(csv):
    df = pd.read_csv(csv, header=0)

    # define time range for regular price:
    peak_start = datetime.strptime("05:00:00", "%H:%M:%S")
    peak_end = datetime.strptime("21:00:00", "%H:%M:%S")

    def get_toll_price(time_slot):  # this determines if the toll is $9 or $2.25
        time = datetime.strptime(time_slot, "%H:%M:%S")
        if peak_start <= time <= peak_end:
            return 9
        else:
            return 2.25

    # charge only once a day:
    df["toll_price"] = df["time"].apply(
        get_toll_price
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
    df["count"] = df.groupby(["license", "month_entry"]).cumcount() + 1

    df["toll_price"] = df.apply(
        lambda row: row["toll_price"] * 0.5
        if row["resident"] == "Y" and row["count"] > 10
        else row["toll_price"],
        axis=1,
    )
    # different modes selections:
    while True:
        mode = input("Please enter the query mode (all, monthly, select):")
        if mode in ["all", "monthly", "select"]:
            if mode == "all":
                return df.groupby(["license", "date", "time", "resident"])[
                    "toll_price"
                ].sum()
            elif mode == "monthly":
                return df.groupby(["license", "month_entry", "resident"])[
                    "toll_price"
                ].sum()
            elif mode == "select":
                while True:  # This ensures the input format is correct
                    plate_num = input(
                        "Please enter plate number(3 alphabets followed by 3 digits)"
                    ).upper()
                    if (
                        len(plate_num) == 7
                        and plate_num[:3].isalpha()
                        and plate_num[3:].isdigit()
                    ):
                        return (
                            df[df["license"] == plate_num]
                            .groupby(["license", "month_entry"])["toll_price"]
                            .sum()
                            .reset_index()
                        )
                    else:
                        print(
                            "License plate numbers have 3 alphabets followed by 4 digits only"
                        )

        else:
            print('Please select from these three modes: "all", "monthly", or "select"')
