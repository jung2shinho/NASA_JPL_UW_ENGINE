import dash
from dash import html
import dash_bootstrap_components as dbc
import json
import os

main_dir = os.getcwd()
dash.register_page(__name__)

# Extract team info from txt file
with open(main_dir + '/data/team/teamInfo.txt','r') as file:
    team_members = json.load(file)

# Generate cards for each team member
cards = []
for member in team_members:
   card = dbc.Card(
      [
         dbc.CardImg(
            src="./static/images/" + member["image"],
            className="img-fluid rounded-start",
         ),
         
         dbc.CardBody(
            [
               html.H4(member["name"], className="card-title"),
               html.Small(
                  member["position"],
                  className="card-text text-muted",
               ),
               html.P(
                  member["bio"],
                  className="card-text",
               ),
            ]
         ),
      ],
      className="mb-3",
      style={"maxWidth": "540px"},
   )
   cards.append(card)

layout = dbc.Container(
    [
        html.H1("Our Team",className="py-1"),
        dbc.Row(
            [dbc.Col(card, width=4,style={'minWidth': '400px',}) for card in cards],
            className="mb-4 flex-wrap",
            justify="center"
        ),
    ],
   #  className="py-1",
)
