from dash import Dash, dcc, html, dash_table, callback, Input, Output
# from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import json
import pandas as pd 
from modules.info_prepare import get_movie_info
import dash 

# app = Dash(__name__)
dash.register_page(__name__, path = '/')
# app.layout = html.Div([
layout = html.Div([
    html.Div([
        dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'},debounce = True)
    ],style=dict(display='flex', justifyContent='center')),
    html.Div([
        html.H1(id = 'movie_title',style = {'textAlign' : 'center'}),
        dbc.Row([
            dbc.Col([html.Label('기본정보: '),html.Ul(id = 'movie_info')], width=2),
            dbc.Col([html.Label('줄거리: '), html.P(id= 'story')], style={"width": "50%"},width=6),
            dbc.Col([html.Label('출연진: '),html.Ul(id = 'crew_list')], width=2)

        ])
    ])
])

# @app.callback(
@callback(
    Output('movie_title', 'children'),
    Output('movie_info','children'),
    Output('story', 'children'),
    Output('crew_list', 'children'), 
    Input("input1", "value")
)
def movie_title_set(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        info_list, breif_story, crew_name, crew_position = get_movie_info(input1)
        # return json.dumps(crew_dict, indent = 2, ensure_ascii = False)
        return '{} 영화 정보'.format(input1), [html.Li(i) for i in info_list] ,breif_story, [html.Li(i) for i in crew_name]
# if __name__ == "__main__":
#     app.run_server(debug=True)