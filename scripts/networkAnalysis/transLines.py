import os
import plotly.io as pio
import geopandas as gpd
import pandas as pd
import plotly.graph_objects as go
from shapely.wkt import loads
from scripts.networkAnalysis.helperFunc import *
import networkx as nx

def create_transLines():
    eventDate = 20131002
    main_dir, event_dir, output_dir = get_paths(eventDate)

    loc_file_path = event_dir + '/gic_monitors.csv'
    loc_df = get_loc_df(loc_file_path)

    #**************************************************************************
    # Load & Read GeoJSON file
    file_path = main_dir + '/data/maps/U.S._Electric_Power_Transmission_Lines.geojson'
    gdf = gpd.read_file(file_path)

    # Convert timeframes to folium-friendly types
    gdf['SOURCEDATE'] = pd.to_datetime(gdf['SOURCEDATE']).dt.strftime('%Y-%m-%dT%H:%M:%S')
    gdf['VAL_DATE'] = pd.to_datetime(gdf['VAL_DATE']).dt.strftime('%Y-%m-%dT%H:%M:%S')

    #**************************************************************************
    # Creating filtered gdf
    volt_min_threshold = 200
    volt_max_threshold = 2000

    # Filter down to columns of interest
    columns_to_keep = ['SHAPE_Length','VOLTAGE','geometry',]
    df_filter = gdf[columns_to_keep]

    # Sort U.S transmission lines by voltage
    df_filter = df_filter.sort_values(by="VOLTAGE", ascending=True)
    # Filter to specified thresholds
    df_filter = df_filter[df_filter['VOLTAGE'] > volt_min_threshold]
    df_filter = df_filter[df_filter['VOLTAGE'] < volt_max_threshold]

    print(f"min Voltage threshold: {volt_min_threshold} kV")
    print(f"max Voltage threshold: {volt_max_threshold} kV")
    print(f"# of Transmission Lines (filtered): {len(df_filter)}")

    # Get list of unique voltages
    unique_voltages = df_filter['VOLTAGE'].unique()

    # Assign 'geometry' column to multilines
    multilines = df_filter['geometry']
    print(f"example of voltage given line id {gdf.iloc[68397]['VOLTAGE']}")

    # Lat/Long Grid Bounds
    lon_lower_b = -135
    lon_upper_b = -60
    lat_lower_b = 25
    lat_upper_b = 50

    # Create Color scale for U.S Transmission Lines by voltate
    hex_colors = [
        '#00ff00', '#00f51c', '#00eb39', '#00e155', '#00d771',
        '#00cd8e', '#00c3aa', '#00b9c6', '#00afc3', '#00a5bf',
        '#009bbd', '#0090bb', '#0086b9', '#007cb7', '#0072b5',
        '#0068b3', '#005fb1', '#0055af', '#004bae', '#0041ac',
        '#0037aa', '#002da8', '#0023a6', '#0019a4', '#000fa2'
    ]

    edge_colors = [
        '#ff0000', # Red
        '#ff3300', # Red-Orange
        '#ff6600', # Orange
        '#ff9900', # Orange-Yellow
        '#ffcc00', # Yellow
        '#ffff00', # Yellow
        '#ccff00', # Yellow-Green
        '#99ff00', # Green
        '#66ff00', # Green
        '#33ff00', # Green
        '#00ff00', # Green
        '#00ff33', # Green-Cyan
        '#00ff66', # Cyan-Green
        '#00ff99', # Cyan
        '#00ffcc', # Cyan
        '#00ffff', # Cyan
        '#00ccff', # Cyan-Blue
        '#0099ff', # Blue-Cyan
        '#0066ff', # Blue
        '#0033ff', # Blue
        '#0000ff', # Blue
        '#3300ff', # Blue-Indigo
        '#6600ff', # Indigo
        '#9900ff', # Indigo
        '#cc00ff', # Indigo-Violet
        '#ff00ff'  # Violet
    ]

    viridis_colors = [
        '#440154', '#440256', '#450457', '#450559', '#46075a', '#46075c', '#46085e', '#470860',
        '#470862', '#470964', '#480a66', '#480a68', '#480b6a', '#480b6c', '#490c6e', '#490c70',
        '#490d72', '#4a0d74', '#4a0e76', '#4a0e78', '#4a0f7a', '#4b107c', '#4b107e', '#4b1180',
        '#4b1182', '#4b1284', '#4c1286', '#4c1388', '#4c138a', '#4c148c', '#4d148e', '#4d1590',
        '#4d1592', '#4d1694', '#4d1696', '#4e1798', '#4e179a', '#4e189c', '#4e189e', '#4e19a0',
        '#4e19a2', '#4f1aa4', '#4f1aa6', '#4f1ba8', '#4f1baa', '#4f1cac', '#4f1cae', '#501daf',
        '#501db1', '#501eb3', '#501eb5', '#501fb7', '#501fb9', '#5020bb', '#5020bd', '#5021bf',
        '#5021c1', '#5022c3', '#5022c5', '#4f23c7', '#4f24c9', '#4f25cb', '#4f25cd', '#4f26cf',
        '#4f27d1', '#4f28d3', '#4e28d5', '#4e29d7', '#4e2ad9', '#4e2bda', '#4e2bdc', '#4e2cde',
        '#4e2ddf', '#4d2ee1', '#4d2fe3', '#4d30e4', '#4d31e6', '#4d32e7', '#4d33e9', '#4d34ea',
        '#4d35ec', '#4d36ed', '#4d37ef', '#4e38f0', '#4e39f1', '#4e3af3', '#4e3bf4', '#4e3cf5',
        '#4f3df6', '#4f3ef7', '#4f40f8', '#4f41f9', '#5042fa', '#5043fb', '#5144fc', '#5145fd',
        '#5246fe', '#5247fe', '#5348fe', '#5349fe', '#544afe', '#554bfe', '#564cfe', '#574dfd',
        '#584efe', '#5950fd', '#5a51fd', '#5b52fd', '#5c53fd', '#5d54fd', '#5e55fd', '#6056fc',
        '#6157fc', '#6258fc', '#6359fc', '#645afc', '#665bfc', '#675cfc', '#685dfc', '#6a5efb',
        '#6b5ffb', '#6c60fb', '#6e61fb', '#6f62fb', '#7163fa', '#7264fa', '#7465fa', '#7566fa',
        '#7767f9', '#7968f9', '#7a69f9', '#7c6af8', '#7e6bf8', '#7f6cf8', '#816df7', '#836ef7',
        '#856ff6', '#8770f6', '#8971f5', '#8b72f5', '#8d73f4', '#8f74f4', '#9175f3', '#9376f3',
        '#9577f2', '#9778f2', '#9979f1', '#9b7af0', '#9d7bf0', '#9f7cee', '#a17ded', '#a37eec',
        '#a57fec', '#a77feb', '#a97fea', '#ab80e9', '#ad81e8', '#ae82e7', '#b083e6', '#b283e5',
        '#b484e4', '#b685e3', '#b886e2', '#b986e1', '#bb87e0', '#bd88df', '#be89dd', '#c08adc',
        '#c28bdb', '#c38cd9', '#c58dd8', '#c78ed6', '#c88fd5', '#ca90d3', '#cb91d1', '#cd92d0',
        '#ce93ce', '#d094cc', '#d295ca', '#d396c8', '#d497c6', '#d598c4', '#d699c2', '#d79ac0',
        '#d89bbe', '#d99cbc', '#da9db9', '#db9eb7', '#dc9fb5', '#dd9fb3', '#dea0b0', '#dfa1ae',
        '#e0a2ac', '#e0a3a9', '#e1a4a7', '#e2a5a4', '#e3a6a2', '#e3a79f', '#e4a89d', '#e5a99a',
        '#e6aa97', '#e6ab95', '#e7ac92', '#e8ad8f', '#e8ae8d', '#e9af8a', '#eaa087', '#eaa185',
        '#eb9c82', '#ec9d7f', '#ec9e7d', '#ed9f7a', '#eda078', '#eea175', '#efa272', '#efa370',
        '#f0a46d', '#f0a56a', '#f1a768', '#f1a865', '#f2aa63', '#f2ab60', '#f3ac5e', '#f3ae5b',
        '#f4af59', '#f4b056', '#f5b154', '#f5b351', '#f6b44f', '#f6b64c', '#f7b749', '#f7b947',
        '#f8ba45', '#f8bc42', '#f9bd40', '#f9bf3d', '#f9c13b', '#fac338', '#fac536', '#fac733',
        '#fbc931', '#fbcb2e', '#fccc2c', '#fecd2a', '#fedf28', '#fee126', '#fee324', '#fee522',
        '#ffe720'
    ]

    # Create color dictionary for transmission Lines
    color_dict = {k:v for k,v in zip(unique_voltages,hex_colors)}
    # PLOTLY Scatter Plot Display for U.S Transmission Lines

    # Create traces for plolty
    trans_traces = []
    for idx, multiline in multilines.items():
        for line in multiline.geoms:  # Iterating over the line strings in the MultiLineString
            x_coords, y_coords = line.xy

            # Filter out coordinates based on the specified conditions
            filtered_x_coords = []
            filtered_y_coords = []
            for x, y in zip(x_coords, y_coords):
                if lon_lower_b <= x <= lon_upper_b and lat_lower_b <= y <= lat_upper_b:
                    filtered_x_coords.append(x)
                    filtered_y_coords.append(y)
            # Extract associated voltage
            voltage = gdf.iloc[idx]['VOLTAGE']
            # Append the Scatter trace with filtered coordinates
            trans_traces.append(
                go.Scatter(
                x=filtered_x_coords,
                y=filtered_y_coords,
                line=dict(width=0.5, color='gray'),
                mode='lines',
                showlegend=False,
                name=str(voltage) +' kV',
                hoverinfo='none'  # Specify that no hover text should be shown
                )
            )

    layout = go.Layout(
        title='U.S Transmission Line Voltage >'+ str(volt_min_threshold) + 'kV + Cross Correlation  // Event: ' + str(eventDate),
        xaxis=dict(scaleanchor="y", scaleratio=1,dtick=2),
        xaxis_title='Longitude',
        yaxis=dict(scaleanchor="x", scaleratio=1,dtick=2),
        yaxis_title='Latitude',
        width=900,  # You can adjust this value as needed
        height=600, # 2:3 aspect ratio: 2/3 * width
    )

    print(f"number of transmission lines traces: {len(trans_traces)}")
    # Plot using Plotly via Scatter
    fig = go.Figure(trans_traces, layout=layout)

    return fig


# def trans_intersections():
#     from shapely.geometry import LineString, Point, MultiPoint
#     from collections import defaultdict

#     line_strings = []

#     for idx, multiline in multilines.items():
#         for line in multiline.geoms: # each multline usually has only 1 line
#             line_strings.append(line)

#     # Initialize a defaultdict to store the count of intersections at each point
#     intersection_counts = defaultdict(int)

#     # Find intersections between LineStrings
#     for i, line1 in enumerate(line_strings):
#         for j in range(i + 1, len(line_strings)):  # Only check each pair once
#             line2 = line_strings[j]
#             intersection = line1.intersection(line2)
#             if isinstance(intersection, Point):
#                 intersection_counts[(intersection.x, intersection.y)] += 1
#             elif isinstance(intersection, MultiPoint):
#                 for point in intersection.geoms:
#                     intersection_counts[(point.x, point.y)] += 1

#     # Display the number of intersections at each point
#     # for point, count in intersection_counts.items():
#     #     # print(f"Intersection at {point}: {count} times")

#     intersections = list(intersection_counts.keys())

#     # Create a NetworkX graph
#     G_transmission = nx.Graph()

#     # Add nodes for intersections
#     for i, intersection in enumerate(intersections):
#         G_transmission.add_node(i, pos=intersection)

#     # Convert to Plotly graph object
#     pos = nx.get_node_attributes(G_transmission, 'pos')
#     edge_x = []
#     edge_y = []

#     for edge in G_transmission.edges():
#         x0, y0 = pos[edge[0]]
#         x1, y1 = pos[edge[1]]
#         edge_x.append(x0)
#         edge_x.append(x1)
#         edge_x.append(None)
#         edge_y.append(y0)
#         edge_y.append(y1)
#         edge_y.append(None)

#     edge_trace = go.Scatter(
#         x=edge_x, y=edge_y,
#         line=dict(width=0.5, color='#888'),
#         hoverinfo='none',
#         mode='lines')

#     node_x = []
#     node_y = []
#     for node in G_transmission.nodes():
#         x, y = pos[node]
#         node_x.append(x)
#         node_y.append(y)

#     node_trace = go.Scatter(
#         x=node_x, y=node_y,
#         mode='markers',
#         hoverinfo='text',
#         marker=dict(
#             showscale=True,
#             colorscale='YlGnBu',
#             reversescale=True,
#             color='red',
#             size=1,
#             colorbar=dict(
#                 thickness=15,
#                 title='Node Connections',
#                 xanchor='left',
#                 titleside='right'
#             ),
#             line_width=2))

#     fig = go.Figure(data=[edge_trace, node_trace, trans_traces],
#                 layout=layout)

#     fig.show()

#     print(line_strings)

#     # Create a NetworkX graph for transmission line
#     G_transmission = nx.Graph()

#     # Add nodes for intersections
#     for xy in enumerate(intersection_counts.keys()):
#         G_transmission.add_node(xy, pos=xy)

#     print(G_transmission)

#     plt.figure(figsize=(20, 10))  # create plotly figure
#     pos = nx.spring_layout(G_transmission)     # Positions for all nodes

#     nx.draw(G_transmission, pos, with_labels=True, node_color='lightblue',
#             edge_color='gray', node_size=500, alpha=0.6, font_size=8)

#     plt.title('GIC Network Cross Correlation')
#     plt.show()

#     import math
#     # Extract intersection coordinates and counts
#     intersection_coords = list(intersection_counts.keys())
#     intersection_counts_values = list(intersection_counts.values())

#     # Create a Scatter trace for intersections
#     intersection_trace = go.Scatter(
#         x=[coord[0] for coord in intersection_coords],
#         y=[coord[1] for coord in intersection_coords],
#         mode='markers',
#         marker=dict(
#             color='red',  # Color of the intersection points
#             size=[math.log(count)/2 for count in intersection_counts_values],  # Size of the marker based on the count of intersections
#             sizeref=0.25,  # Reference for scaling the marker size
#             opacity=0.5,

#         ),
#         name='Intersections',  # Name of the trace
#         showlegend=False  # Show legend for this trace
#     )

#     # Add the intersection trace to the existing figure
#     fig = go.Figure(trans_traces + [intersection_trace] + scatter_traces, layout=layout)

#     # Display Plotly figure with intersections
#     fig.show()

#     # U.S Transmission Lines Dataset via MATLAB
#     from matplotlib.patches import Patch
#     # Plot the GeoDataFrame
#     map = gdf.plot(figsize=(20, 16),linewidth=0.5)

#     # Define common voltages and corresponding colors
#     common_voltages = [0, 44, 115, 161, 169, 230, 345]
#     hex_colors = ['blue','green', 'cyan', 'yellow', 'orange', 'red']
#     legend_labels = ['<' + str(i) for i in common_voltages[1:]]

#     # Plot overlays for each common voltage
#     for voltage, color, label in zip(common_voltages, hex_colors, legend_labels):
#         overlay = gdf[gdf['VOLTAGE'] > voltage]  # Filter GeoDataFrame based on voltage
#         overlay.plot(ax=map, marker='o', color=color, markersize=5, linewidth=0.5, label=label)

#     # Create a custom legend with colored patches
#     legend_handles = [Patch(color=color, label=label) for color, label in zip(hex_colors, legend_labels)]

#     # Add legend
#     map.legend(handles=legend_handles, title='Voltage', loc='upper right')

#     # Set xy axis limits
#     map.set_xlim((-130, -65))
#     map.set_ylim((25,50))

#     # Put labels on the map
#     map.set_xlabel("Longitude")
#     map.set_ylabel("Latitude")
#     map.set_title("Major US Transmission Lines")

#     # Scatter Map Box Plot
#     trans_traces = []
#     coordinates = []

#     for multiline in multilines:
#         # Extract coordinates from each LineString within the MULTILINESTRING

#         for line in multiline.geoms:
#         lon,lat = line.xy
#         lon = np.array(lon) # convert to np
#         lat = np.array(lat) # convert to np

#         # Create a Plotly trace for the multiline string
#         trace = go.Scattermapbox(
#             mode="lines",
#             lon=lon,
#             lat=lat,
#             line=dict(width=0.5, color='blue'),
#             name=f"Trans Lines",
#             showlegend=False
#         )
#         # Append the trace to the list of traces
#         trans_traces.append(trace)

#     len(trans_traces)

#     # Create layout for the Plotly figure
#     layout = go.Layout(
#         title="U.S Transmission Lines >" + str(volt_min_threshold) + "kV & <" + str(volt_max_threshold) +"kV",
#         mapbox=dict(
#             style="carto-positron",
#             zoom=3,
#             center=dict(lat=40, lon=-98.5),
#         ),
#     )

#     # Create a Plotly figure with the traces and layout
#     fig = go.Figure(data=trans_traces,
#                     layout=layout)

#     # Show the Plotly figure
#     fig.show()

#     # Add node and edge traces to transmission trace
#     trans_traces.append(edge_trace)
#     trans_traces.append(node_trace)

#     len(trans_traces)

#     # Create the network graph
#     fig = go.Figure(data=[node_trace,edge_trace],
#                     layout=go.Layout(
#                         title='U.S Transmission Line Voltage >',
#                         mapbox=dict(
#                             style="carto-positron",  # Map style
#                             center=dict(lat=37.0902, lon=-95.7129),  # Center coordinates
#                             zoom=3,  # Zoom level
#                         ),
#                         titlefont_size=12,
#                         hovermode='closest',
#                         margin=dict(b=20, l=5, r=5, t=40),
#                         annotations=[dict(
#                             showarrow=False,
#                             xref="paper", yref="paper",
#                             x=0.005, y=-0.002)],
#                         xaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
#                         yaxis=dict(showgrid=True, zeroline=False, showticklabels=True),
#                     )
#                 )
#     fig.show()