import dash
from dash import dcc, html, Output, Input, callback, dash_table
import pandas as pd
from datetime import datetime
import dash_bootstrap_components as dbc
import os


from scripts.networkAnalysis.correlations import correlations
from scripts.networkAnalysis.aeIndex import aeIndex
from scripts.networkAnalysis.heatmap import create_heatmap
from scripts.networkAnalysis.transLines import create_transLines
from scripts.networkAnalysis.helperFunc import *

# Register page
dash.register_page(__name__, path='/simulation')

# Initial Inputs
year = '2013'
day = '02'
month = '10'
eventDate = year + month + day

windowSize = 30
correlation_threshold = 0.95

# Establish paths
main_directory = os.getcwd()
output_directory = main_directory + '/output/' + str(eventDate)
data_directory = main_directory + '/data/GMD and GIC/'
event_directory = data_directory + '/event_' + str(eventDate)
# Create Default
defaultEvent = datetime(int(year),int(month),int(day)).strftime('%Y %b %d')
# List events based on data folder
# events = [datetime.strptime(event[-8:], '%Y%m%d').strftime('%Y %b %d') for event in os.listdir(data_directory) if event.startswith('event_')]

# List of files at event directory
files = os.listdir(event_directory +'/GIC')

# Example of GIC TABLE
df_gic = pd.read_csv(os.path.join(event_directory + '/GIC',files[0]))



# Get main directory
main_dir = os.getcwd()

file_content = ""
# Open Simulation File
with open(main_dir + '/data/text/simulation_text.txt','r',encoding='utf-8') as file:
   file_content = file.read()

# minimum size of plotly
min_width = "350px"

# Create page layout
layout = dbc.Container([
      # TITLE
      dbc.Row(
         html.H1('Network Analysis - Simulation'),
         style={'textAlign':'center'}
      ),
      html.Hr(), # breaklines
      dcc.Markdown(file_content),

      html.Hr(), # breakline
      html.P(f"* Using Global Cross-Correlation Threshold: {correlation_threshold}"),

      # EXAMPLE OF GEOMAGNETIC EVENT PLOTS
      dbc.Row(
         # HEADING
         [dbc.Col([
            html.H1(
               id='header',
               children='Geomagnetic Event',
               style={
                     'textAlign': 'center'
               }
            ),
         ],
         className='col-md-8'
         ),

         dbc.Col(
            # DROPDOWN MENU
            [dcc.Dropdown(
               id='eventDropdown',
               value=defaultEvent, # initial value
               options=[{'label': defaultEvent, 'value': defaultEvent} 
               ]
            )],
         className='col-md-4'
         )
         ],
         style={'padding':'0.5rem'}
      ),


      # Example of GIC TABLE 

      # ROW of PLOTS
      dbc.Row([
         dbc.Col([
            html.H4('Time Frame'),
            dcc.RangeSlider(
               id='range-slider',
               value=[0,1440],
               min=0,
               max=60*24,   # minutes in a day
               step=60*4,   # hourly step
               marks={i: str(i) for i in range(0,60*24+1,60*4)}
            ),
            html.H4('Window Size'),
            dcc.Slider(
               id='window-slider',
               min=15,
               max=45,
               step=30,
               value=15,
               marks={i: str(i) for i in range(15,46,30)}
             ),
         ],
         style={"text-align":"center"},
         className='col-md-4'
         ),
         

         # FIGURE 2: TIME BASED CROSS CORRELATION
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
                  dcc.Graph(
                     id='timeBasedCorrelations',
                  )]
            ),
            html.Div(id='output-graph')
            ],
            style={"min-width": min_width}
         ),

         # FIGURE 3: Wavelet HEATMAP
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
                  dcc.Graph(
                     id='wavelet-heatmap-low',
                  )]
            ),
            html.Div(id='output-graph'),
            ],
            style={"min-width": min_width}
         ),

         # FIGURE 3: Wavelet HEATMAP
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
                  dcc.Graph(
                     id='wavelet-heatmap-high',
                  )]
            ),
            html.Div(id='output-graph'),
            ],
            style={"min-width": min_width}
         ),

         # FIGURE 4: Centrality Graph
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
                  dcc.Graph(
                     id='centrality-graph',
                     # figure=fig1,
                  )]
            ),
            html.Div(id='output-graph'),
            ],
            style={"min-width": min_width}
         ),
         # FIGURE 1: AE INDEX  
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
                  dcc.Graph(
                     id='aeIndex',
                     # figure=fig1,
                  )]
            ),
            html.Div(id='output-graph'),
            ],
            style={"min-width": min_width}
            ),
         # FIGURE 5: U.S Trans Lines
         dbc.Col([
            dcc.Loading( # Loading component wrapper
               id="loading-1",
               type="default",
               children=[
   
                  # figs=create_transLines()
                  ]
            ),
            html.Div(id='output-graph'),
            ],
            style={"min-width": min_width}
         )],
         style={"display": "flex", "flexWrap": "wrap"}  # allows wrapping
      ),

      html.Hr(), # breakline
      
      # TOGGLE ARROW - DESCRIPTION
      html.Div([
         html.Button(html.I(className="bi bi-alarm"), id='toggle-button', className="toggle-button"),
         html.Div([
            html.Div(id='toggle-div', children=[
                  html.H3('This is a toggleable div')
            ], style={'display': 'none'})
         ]),
      ])
   ],
)

# Callback for dropdown user input
@callback(
   [Output(component_id="timeBasedCorrelations", component_property="figure"),
   Output(component_id="aeIndex", component_property="figure"),
   Output(component_id="centrality-graph", component_property="figure"),
   Output(component_id="wavelet-heatmap-low",component_property="figure"),
   Output(component_id="wavelet-heatmap-high",component_property="figure")],
   [Input(component_id='eventDropdown', component_property="value"),
    Input(component_id="window-slider",component_property="value"),
    Input(component_id="range-slider", component_property="value")]
)

def update_graph(user_selected_date, user_window_size, rangeSlider_value):
   print("**********UPDATING GRAPHS***********")
   print(user_selected_date)
   # Change date to format
   user_selected_date = datetime.strptime(user_selected_date, "%Y %b %d").strftime("%Y%m%d")
   # Create Plotly figure using correlations.py
   fig1, fig4 = correlations(user_selected_date, user_window_size,'modwt',rangeSlider_value[0],rangeSlider_value[1])
   fig2 = aeIndex(user_selected_date)
   fig3,fig5 = create_heatmap(user_selected_date,'modwt',1622)

   return fig1, fig2, fig4, fig3, fig5


# Callback for dropdown
@callback(
    Output('toggle-div', 'style'),
    [Input('toggle-button', 'n_clicks')]
)
def toggle_div(n_clicks):
    if n_clicks is None:
        return {'display': 'none'}
    elif n_clicks % 2 == 0:
        return {'display': 'none'}
    else:
        return {'display': 'block'}

