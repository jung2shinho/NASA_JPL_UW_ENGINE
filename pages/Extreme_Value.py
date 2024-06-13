import dash
from dash import dcc
import dash_bootstrap_components as dbc
import re
import os

# Register page
dash.register_page(__name__, path='/eva')

# Get main directory
main_dir = os.getcwd()

# Read text file
with open(main_dir + '/data/text/eva_text.txt','r',encoding='utf-8') as file:
   file_content = file.read()

# Construct Layout
layout = dbc.Container(
   [
      dcc.Markdown(file_content)
   ]      
)
