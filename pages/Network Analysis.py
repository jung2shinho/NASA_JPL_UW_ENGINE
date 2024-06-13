import dash
from dash import dcc
import dash_bootstrap_components as dbc

import os

# Register page
dash.register_page(__name__, path='/network_analysis')

# Get main directory
main_dir = os.getcwd()

# Open text file
with open(main_dir + '/data/text/network_text.txt','r',encoding='utf-8') as file:
   file_content = file.read()

markdown_style = {
    'width': '50%', 
    'margin': 'auto', 
    'text-align': 'center'
}

# Construct Layout
layout = dbc.Container(
   [
      dcc.Markdown(file_content)

   ]      
)
