import pandas as pd
import plotly.graph_objs as go
import os
from datetime import datetime, timedelta


main_directory = os.getcwd() 
curr_directory = main_directory + '/data/GMD and GIC'


def aeIndex(eventDate=20130531):
    event_directory = curr_directory + '/event_' + str(eventDate)
    # Read the AE Index from Kyoto Insititude
    with open(os.path.join(event_directory,str(eventDate) + '_AEINDEX.txt'), 'r') as file:
        # Read the content of the file
        data = file.read()

    lines = data.strip() # strip leading or trailing whitespace
    lines = lines.split() # array
    # print(lines)
    aeIndex = []

    # Create datetime object
    start_datetime = datetime.strptime(str(eventDate), '%Y%m%d')


    for string in lines:
        if string.isdigit():
            aeIndex.append(int(string))

    # Extract last HRly Mean from WDC-like data
    aeIndex = [x for i, x in enumerate(aeIndex) if (i + 1) % 61 != 0]
    print(len(aeIndex))


    # Create datetime_array for x axis
    datetime_array = []
    # Iterate over the range of minutes
    for minutes in range(len(aeIndex)):
        # Calculate the timedelta for the current iteration
        time_delta = timedelta(minutes=minutes)

        # Calculate the new datetime by adding the timedelta to the start datetime
        new_datetime = start_datetime + time_delta

        # Append the new datetime to the list
        datetime_array.append(new_datetime)

    # Create trace
    trace = go.Scatter(
        x=datetime_array,
        y=aeIndex,
        mode='lines',
        name='Geomagnetic Data'
    )

    width=1000

    # Create layout
    layout = go.Layout(
        title='24 HR AE INDEX for ' + start_datetime.strftime("%Y-%m-%d"),
        xaxis=dict(title='UT'),
        yaxis=dict(title='AE INDEX'),
        # width=width,
        # height=width/2,  # Set the aspect ratio to 2:1
        hovermode='x unified'
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)

    # Save the plot as an HTML file
    fig.write_html(main_directory + '/output/' + str(eventDate) + '/correlations_' + str(eventDate) + "/" + str(eventDate) +'_AEINDEX.html')

    return fig
