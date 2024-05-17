import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import filedialog
import tkinter as tk
import tkinter.filedialog as fd
import chardet

def read_csv():
    # Read the csv file with encoding detection
    root = tk.Tk()
    root.withdraw()
    file_path = fd.askopenfilename()

    # Detect file encoding
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    encoding = result['encoding']

    df = pd.read_csv(file_path, encoding=encoding)
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

    return source_destination_counts_sorted

def draw_network_graph(df):
    G = nx.DiGraph()

    for _, row in df.iterrows():
        G.add_edge(row['Source'], row['Destination'], weight=row['Count'])

    pos = nx.spring_layout(G, k=0.5)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)

    # edges
    edges = G.edges(data=True)
    nx.draw_networkx_edges(G, pos, edgelist=edges, width=[edge[2]['weight'] / 10 for edge in edges])

    # labels
    nx.draw_networkx_labels(G, pos, font_size=12, font_family='sans-serif')

    plt.title("Network Graph of Packet Connections")
    plt.axis('off')
    plt.show()

def main():
    # Process the CSV to get the Source-Destination relationships
    df = process_csv()

    # Draw the network graph
    draw_network_graph(df)

if __name__ == "__main__":
    main()
