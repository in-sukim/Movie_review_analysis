from dash import Dash, dcc, html, dash_table, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

import json
import pandas as pd 
from modules.info_prepare import get_movie_info
import dash 
from modules.review_prepare import daum
from modules.get_plot import reivew_analysis


# app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app = Dash(__name__)

app.layout = html.Div([

    html.Div([
        dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'},debounce = True)
    ],style=dict(display='flex', justifyContent='center')),

    html.Div([
        html.H1(id = 'title_info',style = {'textAlign' : 'center'}),
        dbc.Row([
            dbc.Col([html.H4('기본정보: '),html.Ul(id = 'movie_info')], width=2),
            dbc.Col([html.H4('줄거리: '), html.P(id= 'story')], style={"width": "50%"},width=6),
            dbc.Col([html.H4('출연진: '),html.Ul(id = 'crew_list')], width=2)

        ])
    ]),

    html.H1(id = 'review_title',style = {'textAlign' : 'center'}),
    html.Br(),
    html.Div([dcc.Store(id="current_df")]),
    dcc.Graph(id = "graph1", config= {'displayModeBar': False}),
    # dbc.Row([
    #     dbc.Col([
    #         dash_table.DataTable(id = 'review_df',
    #                              columns = [
    #                                  dict(id='rating', name='rating', type='text'),
    #                                  dict(id='text', name='text', type='text')],
    #                              editable=False,
    #                              data = [],
    #                              page_size=10,
    #                              style_data={
    #                                  'whiteSpace': 'normal',
    #                                  'height': 'auto'},
    #                              style_cell={'textAlign': 'center',
    #                                          'fontSize':12, 'font-family':'NanumSquareR'})
    #     ]),
    #     dbc.Col([
    #         dcc.Graph(id = 'wordcloud', config = {'displayModeBar': False})
    #     ])
    # ])
    dash_table.DataTable(id = 'review_df',
                     columns = [
                         dict(id='rating', name='rating', type='text'),
                         dict(id='text', name='text', type='text'),
                         ],
                         editable=False,
                         data = [],
                         page_size=10,
                         style_data={
                             'whiteSpace': 'normal',
                             'height': 'auto'},
                             style_cell={'textAlign': 'center',
                                         'fontSize':12, 'font-family':'NanumSquareR'})
    # html.Div([
    #     html.Div([
    #         html.Div(dcc.Link(
    #                 f"{page['name']} - {page['path']}", href=page["relative_path"]
    #             ))
    #         for page in dash.page_registry.values()]
    #         ),dash.page_container])
])

@app.callback(
    Output('title_info', 'children'),
    Output('movie_info','children'),
    Output('story', 'children'),
    Output('crew_list', 'children'), 
    Input("input1", "value")
)
def movie_info(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        info_list, breif_story, crew_name, crew_position = get_movie_info(input1)
        return '{} 영화 정보'.format(input1), [html.Li(i) for i in info_list] ,breif_story, [html.Li(i) for i in crew_name]
    

@app.callback(
    Output('review_title', 'children'),
    Output('current_df', 'data'),
    Output("graph1", "figure"),
    Input('input1','value')
    
)
def movie_review(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        df = reivew_analysis(input1, 5)
        return '{} 영화 리뷰 분석'.format(input1),df.data.to_dict('records'),df.create_plot()

@app.callback(
    Output('review_df', 'data'),
    Input('current_df','data'),
    Input("graph1", "clickData")
)
def return_plot(data,clickData):
    if clickData is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        if clickData['points'][0]['label'] in [str(i) for i in range(11)]:
            condition = df['rating'] == clickData['points'][0]['label']
            df = df.loc[condition]
            return df.to_dict('records')
        else:
            return None
        
# def return_plot(data,clickData):
#     if clickData is None:
#         raise PreventUpdate
#     else:
#         df = pd.DataFrame(data)
#         condition1 = df['label'] == clickData['points'][0]['label']
#         condition2 = df['rating'] == clickData['points'][0]['label']

#         df = df.loc[condition1 | condition2]
#         return df.to_dict('records')
    
if __name__ == "__main__":
    app.run_server(debug=True)