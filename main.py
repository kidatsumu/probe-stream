import pandas as pd
from tkinter import filedialog
import tkinter as tk
import tkinter.filedialog as fd

def read_csv():
    # Read the csv file
    root = tk.Tk()
    root.withdraw()
    file_path = fd.askopenfilename()
    df = pd.read_csv(file_path)
    return df

def output_csv(df):
    # Output the csv file
    root = tk.Tk()
    root.withdraw()
    file_path = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    df.to_csv(file_path, index=False)

def process_csv():
    # Read the CSV file
    data = read_csv()

    # Group by Source and Destination to count the number of occurrences
    source_destination_counts = data.groupby(['Source', 'Destination']).size().reset_index(name='Count')

    # Sort the results by Source and then by Count (descending)
    source_destination_counts_sorted = source_destination_counts.sort_values(['Source', 'Count'], ascending=[True, False])

    # Output the results to a new CSV file
    output_csv(source_destination_counts_sorted)

# Run the process
process_csv()
