import dash 
from dash import Dash, dcc, html, dash_table, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from io import BytesIO
import base64
import json
from konlpy.tag import Okt
from collections import Counter
from wordcloud import WordCloud

import pandas as pd 

from modules.info_prepare import get_movie_info
from modules.review_prepare import daum
from modules.sentiment_review import reivew_analysis

class one_run:
    def __init__(self):
        global okt

        okt = Okt()
def plot_wordcloud(data):
    d = {a: x for a, x in data.values}
    wc = WordCloud(font_path = 'AppleGothic',
                   background_color='white', 
                   width=480, 
                   height=360)
    wc.fit_words(d)
    return wc.to_image()

# app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([

    html.Div([
        dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'},debounce = True)
    ],style=dict(display='flex', justifyContent='center')),
    html.Br(),
    html.Br(),
    html.Div([
        html.H1(id = 'title_info',style = {'textAlign' : 'center'}),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([html.H3('기본정보: '),html.Ul(id = 'movie_info')], style={'margin-left': '150px'}),
            # , style={"width": "50%"}
            dbc.Col([html.H3('출연진: '),html.Ul(id = 'crew_list')], style={'margin-left': '150px'}),
            dbc.Col([html.H3('줄거리: '), html.P(id= 'story')], style={'margin-right': '120px'})

        ])
    ]),
    html.Br(),
    html.Br(),
    html.H1(id = 'review_title',style = {'textAlign' : 'center'}),
    html.Br(),
    html.Div([dcc.Store(id="current_df")]),
    # dcc.Graph(id = "graph1", config= {'displayModeBar': False}),
    html.Div([
        dbc.Row([
            dbc.Col([dcc.Graph(id = "graph1", config= {'displayModeBar': False}),], lg=6),
            # dbc.Col([dcc.Graph(id = "graph2", config= {'displayModeBar': False}),], lg=6)
            ], justify="center", align="center")
    ]),
    html.Div([
        dbc.Row([
            dbc.Col([
                dash_table.DataTable(id = 'review_df',
                                     columns = [
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
                                                         ]),
            dbc.Col([html.Img(id="image_wc")], lg=6)
            # dbc.Col([dcc.Graph(id = "graph2", config= {'displayModeBar': False}),], lg=6)
            ])
    ])
    # dash_table.DataTable(id = 'review_df',
    #                  columns = [
    #                     #  dict(id='rating', name='rating', type='text'),
    #                      dict(id='text', name='text', type='text'),
    #                      ],
    #                      editable=False,
    #                      data = [],
    #                      page_size=10,
    #                      style_data={
    #                          'whiteSpace': 'normal',
    #                          'height': 'auto'},
    #                          style_cell={'textAlign': 'center',
    #                                      'fontSize':12, 'font-family':'NanumSquareR'})
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
    # Output("graph2", "figure"),
    Input('input1','value')
    
)
def movie_review(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        df = reivew_analysis(input1, 5)
        return '{} 영화 리뷰 분석'.format(input1), df.data.to_dict('records'), df.create_plot()


@app.callback(
    Output('review_df', 'data'),
    Output('image_wc', 'src'),
    Input('current_df','data'),
    Input("graph1", "clickData"),
    Input('image_wc', 'id')
)
# def return_plot(data,clickData):
#     if clickData is None:
#         raise PreventUpdate
#     else:
#         df = pd.DataFrame(data)
#         if clickData['points'][0]['label'] in [str(i) for i in range(11)]:
#             condition = df['rating'] == clickData['points'][0]['label']
#             df = df.loc[condition]
#             return df.to_dict('records')
#         else:
#             return None
        
def return_plot(data,clickData, b):
    if clickData is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        condition1 = df['label'] == clickData['points'][0]['label']
        condition2 = df['rating'] == clickData['points'][0]['label']

        df = df.loc[condition1 | condition2]

        full = []
        for i in df['text'].map(lambda x: okt.nouns(x)).tolist():
            for j in i:
                if len(j) > 1:
                    full.append(j)
        
        counts = Counter(full)
        counts = counts.most_common(20)

        word = []
        frequency = []
        for i in counts:
            word.append(i[0])
            frequency.append(i[1])
        
        dfm = pd.DataFrame({'word': word, 'freq': frequency})
        img = BytesIO()
        plot_wordcloud(data=dfm).save(img, format='PNG')
        return df.to_dict('records'), 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    
if __name__ == "__main__":
    one_run()
    app.run_server(debug=True)