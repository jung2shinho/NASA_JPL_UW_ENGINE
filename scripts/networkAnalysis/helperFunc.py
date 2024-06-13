import pywt
import numpy as np
import os
import pandas as pd

# HELPER FUNCTIONS
def get_paths(eventDate):
    main_directory = os.getcwd() 
    event_directory = main_directory + '/data/GMD and GIC' + '/event_' + str(eventDate) + '/GIC'
    output_directory = os.path.join(main_directory,'output', str(eventDate),'correlations_' + str(eventDate))
    return main_directory, event_directory, output_directory

def get_loc_df(path):
    # Location Dataframe for Devices (e.g Latitude / Longitude )
    loc_df = pd.read_csv(path) # create df for locations based on device ID
    print(loc_df)
    # Adjust Dataset by making Longitude Negative (indicating West)
    device_IDs = loc_df['Device ID'] # Series
    loc_df.rename(columns={' Latitude': 'Latitude'}, inplace=True) # Change column title to remove extra space
    loc_df.rename(columns={' Longitude': 'Longitude'}, inplace=True) # Change column title to remove extra space
    loc_df['Longitude'] = loc_df['Longitude'] * -1  # create negative for western hemisphere
    latitude_dict = pd.Series(loc_df['Latitude'].values, index=loc_df['Device ID']).to_dict()

    return loc_df, latitude_dict

# This function calculates the maximum level of decomposition that can be achieved using Stationary Wavelet Transform (SWT) for a given input data length
def determine_max_level(data_length, wavelet='db4'):
    return pywt.swt_max_level(data_length)


# This function computes the stationary wavelet transform of a given dataset using a specified wavelet
def modwt(data, wavelet, level):
    return pywt.swt(data, wavelet, level=level, start_level=0)

# This function calculates the cross-correlation between two sets of wavelet coefficients.
# The wavelet coefficient is calculated by MODWT and represents the components of the original signal on different frequency scales.
# Here, wt1 and wt2 represent the wavelet coefficients of the two signals on the same scale
# and the function calculates and returns the correlation coefficients of these coefficients on each scale.
def wavelet_cross_correlation(wt1, wt2):
    corrs = []
    for coeff1, coeff2 in zip(wt1, wt2):
        corr = np.corrcoef(coeff1[0], coeff2[0])[0, 1]
        corrs.append(corr)
    return corrs

# This function calculates the cross-correlation of two time series in the sliding window.
# This is often used to study how the correlation of time series changes at different points in time
def sliding_window_cross_correlation(wt1, wt2, window_size=30):

    assert len(wt1) == len(wt2)
    sliding_corrs = []

    for start in range(len(wt1) - window_size + 1):
        end = start + window_size
        window_corr = np.corrcoef(wt1[start:end], wt2[start:end])[0, 1]
        sliding_corrs.append(window_corr)

    return sliding_corrs

# The first function is to obtain a one-time correlation on different scales of the wavelet transform,
# while the second function is to obtain a continuous correlation of the time varying window
def make_length_even(data):
    return data if len(data) % 2 == 0 else np.append(data, data[-1])


# Helper function to look up latitude and longitude by device ID
def lookup_lat_long(device_id, dataframe):
    device_info = dataframe[dataframe['Device ID'] == int(device_id)]
    if not device_info.empty:
        latitude = device_info['Latitude'].iloc[0]
        longitude = device_info['Longitude'].iloc[0]
        return latitude, longitude
    else:
        return None, None


def get_edge_color(value,colors):
    index = int(value * len(colors))
    index = min(index, len(colors) - 1)  # Ensure index doesn't exceed array bounds
    return colors[index]