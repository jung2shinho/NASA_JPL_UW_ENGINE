# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import seaborn as sns
import os
import json
from .helperFunc import get_paths, get_loc_df
from .correlations import get_paths
import pywt
import plotly.graph_objects as go


def create_heatmap(eventDate=20131002, wavelet_transform='modwt',desired_length=1622):
    print(f"\ncreating heatmap\n")
    # Get the current working directory + desired directory
    main_dir, event_dir, output_dir = get_paths(eventDate)

    # Get loc_df
    loc_df, latitude_df = get_loc_df(event_dir + '/gic_monitors.csv')
    
    # Read or conduct the wavelet transform coefficient data
    file_path_results = output_dir + '/' + wavelet_transform + '_results_' + str(eventDate) +'.json'
    if os.path.exists(file_path_results):
        print(f"{wavelet_transform}_results_{eventDate}.json exists!")
        with open(file_path_results,'r') as file:
            wavelet_coeff = json.load(file)

    # Remove
    low_freq_coeff = {}
    high_freq_coeff = {}

    for k, v in wavelet_coeff.items():
        tupl = v[0]
        low_coeff_list = np.array(tupl[0]) # list of approximation coefficients (low-freq components)
        high_coeff_list = np.array(tupl[1]) # list of detail coefficicents (high-freq components)
        device_id = k.split('_')[-1].split('.')[0]
        lat = latitude_df[int(device_id)]
        if str(lat) in low_freq_coeff and len(low_freq_coeff) == desired_length:
            low_freq_coeff[str(lat)] += low_coeff_list
        else:
            low_freq_coeff[str(lat)] = low_coeff_list
        if str(lat) in high_freq_coeff and len(high_freq_coeff) == desired_length:
            high_freq_coeff[str(lat)] += high_coeff_list
        else:
            high_freq_coeff[str(lat)] = high_coeff_list

    low_freq_coeff = dict(sorted(low_freq_coeff.items()))
    # print(low_freq_coeff)
    high_freq_coeff= dict(sorted(high_freq_coeff.items()))
    z_data_1 = [np.abs(low_freq_coeff[key]) for key in low_freq_coeff]   # list of lists
    z_data_2 = [np.abs(high_freq_coeff[key]) for key in high_freq_coeff] # list of lists



    # Create heatmap
    heatmap_1 = go.Heatmap(
        y=list(low_freq_coeff.keys()), 
        z=z_data_1,
        colorscale='Reds'
        )
    heatmap_2 = go.Heatmap(
        y=list(high_freq_coeff.keys()), 
        z=z_data_2,
        colorscale='Reds'
        )

    # Create layout
    layout = go.Layout(
        title="Low Coefficient",
        yaxis=dict(
            title="Latitude",
            ),
        xaxis=dict(
            range=[0,60*24],
            title="Time"
        )
        )

    # Create figure for low Coefficient
    fig1 = go.Figure(data=[heatmap_1], layout=layout)

    # Create figure for High Coefficient
    fig2 = go.Figure(data=[heatmap_2], layout=layout)

    fig2.update_layout(
        title="High Coefficient"
    )

    return fig1, fig2