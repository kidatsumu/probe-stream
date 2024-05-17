import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
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

# Load the data
df = read_csv()
df['Time'] = pd.to_datetime(df['Time'], unit='s')  # assuming 'Time' column is in seconds
df['Stream'] = df['Source'] + " -> " + df['Destination']

# Initialize the Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Packet Stream Visualization"),
    dcc.Graph(id='main-graph'),
    html.Label('Select Stream:'),
    dcc.Dropdown(id='stream-selector',
                 options=[{'label': stream, 'value': stream} for stream in df['Stream'].unique()],
                 multi=True),
    dcc.Graph(id='selected-stream-graph'),
    html.Div(id='packet-info')
])

# Callback to update the main graph
@app.callback(
    Output('main-graph', 'figure'),
    Input('stream-selector', 'value')
)
def update_main_graph(selected_streams):
    fig = px.scatter(df, x='Time', y='Stream', title='Packet Stream Visualization',
                     labels={'Stream': 'Packet Flow'}, height=600)

    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Stream',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(tickmode='linear', automargin=True)
    )

    return fig

# Callback to update the selected stream graph and show packet info
@app.callback(
    Output('selected-stream-graph', 'figure'),
    Output('packet-info', 'children'),
    Input('stream-selector', 'value')
)
def update_selected_stream_graph(selected_streams):
    if not selected_streams:
        return px.scatter(title='Select a stream to view details'), "Select a stream to view packet info."

    selected_sources = set()
    selected_destinations = set()

    # Collect all sources and destinations from the selected streams
    for stream in selected_streams:
        src, dst = stream.split(" -> ")
        selected_sources.add(src)
        selected_destinations.add(dst)

    # Filter dataframe to include packets where source or destination matches the selected streams
    filtered_df = df[(df['Source'].isin(selected_sources) | df['Destination'].isin(selected_destinations)) &
                     ~((df['Source'] == 'Broadcast') & (df['Destination'] == 'Broadcast'))]

    fig = px.scatter(filtered_df, x='Time', y='Stream', title='Selected Packet Streams',
                     labels={'Stream': 'Packet Flow'}, height=600)

    fig.update_layout(
        xaxis_title='Time',
        yaxis_title='Stream',
        xaxis=dict(rangeslider=dict(visible=True)),
        yaxis=dict(tickmode='linear', automargin=True)
    )

    # Display Info for the selected streams
    packet_infos = []
    for _, row in filtered_df.iterrows():
        packet_infos.append(html.P(f"Time: {row['Time']}, Source: {row['Source']}, Destination: {row['Destination']}, Info: {row['Info']}"))

    return fig, packet_infos

if __name__ == '__main__':
    app.run_server(debug=True)
