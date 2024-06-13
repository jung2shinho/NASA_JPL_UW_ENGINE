import dash
from dash import dcc
import dash_bootstrap_components as dbc

import os
dash.register_page(__name__, path='/ML')

main_dir = os.getcwd()

with open(main_dir + '/data/text/ml_text.txt','r',encoding='utf-8') as file:
   file_content = file.read()


layout = dbc.Container(
   [
      dcc.Markdown(file_content)
   ],
)
