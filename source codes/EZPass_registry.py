from datetime import datetime as dt
import datetime
import os
import tkinter as tk
from tkinter import messagebox
import csv


def register_gui():
    root = tk.Tk()
    root.title("EZPass registry")
    root.geometry("600x200")
    plate_num = tk.StringVar()
    resident = tk.StringVar()

    def EZ_register():
        plate = plate_num.get().upper()
        res = resident.get().upper()
        # This ensures the plate numbers are in the correct format
        if len(plate) != 7 or not plate[:3].isalpha() or not plate[3:].isdigit():
            messagebox.showerror(
                "Invalid input",
                "License plateshould be in 3 letters followed by 4 digits",
            )
            plate_num.set("")
            return

        # this ensures the entry is only Y or N
        if res not in ["Y", "N"]:
            messagebox.showerror(
                "Invalid input", "Please enter Y/N for residency in Manhattan"
            )
            resident.set("")
            return

        file_path = "plate_db.csv"
        file_path_exists = os.path.exists(file_path)
        # Write csv file for all plate numbers:
        with open(file_path, "a") as file:
            if not file_path_exists:
                file.write("license,resident\n")  # Write header in new file
            elif file_path_exists:
                with open(file_path, "r") as x:
                    reader = csv.reader(x)
                    next(reader)  # skip header row
                    for row in reader:
                        if row[0] == plate:
                            messagebox.showerror(
                                "Duplicate Entry",
                                f"Duplicate entry detected for {plate}",
                            )
                            plate_num.set("")
                            resident.set("")
                            return
            file.write("{},{}\n".format(plate, res))

        messagebox.showinfo(
            "Entry Accepted!",
            f"Plate: {plate} is registered as {'Resident' if res == 'Y' else 'Non-resident'}",
        )
        # Resets the input box
        plate_num.set("")
        resident.set("")

    plate_num_label = tk.Label(
        root, text="Plate Numer(3 letters and 4 digits)", font="Times 13"
    )
    plate_num_entry = tk.Entry(root, textvariable=plate_num, width=15, font="Times 13")
    resident_label = tk.Label(
        root, text="Are You Manhattan resident(Y/N)?", font="Times 13"
    )
    resident_entry = tk.Entry(root, textvariable=resident, width=5, font="Times 13")
    instructions_label = tk.Label(
        root,
        text="Instructions:\n1) 'plate_db.csv' file will be created upon entry.\n2) It will be used as a reference for the scanner tool and calculator.",
        justify="left",
        wraplength=150,
    )

    sub_btn = tk.Button(root, text="Enter", command=EZ_register)

    plate_num_label.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="e")
    plate_num_entry.grid(row=0, column=2, padx=10, pady=10, sticky="w")
    resident_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="e")
    resident_entry.grid(row=1, column=2, padx=10, pady=10, sticky="w")
    instructions_label.grid(row=0, column=3, padx=5, pady=5, sticky="w")
    sub_btn.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    return root.mainloop()


register_gui()
