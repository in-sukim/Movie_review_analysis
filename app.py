from dash import Dash, dcc, html, dash_table, callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

import json
import pandas as pd 
from modules.info_prepare import get_movie_info
import dash 
from modules.review_prepare import daum
from modules.sentiment_review import reivew_analysis


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

    html.H1(id = 'review_title',style = {'textAlign' : 'center'}),
    html.Br(),
    html.Br(),
    html.Div([dcc.Store(id="current_df")]),
    # dcc.Graph(id = "graph1", config= {'displayModeBar': False}),
    html.Div([
        dbc.Row([
            dbc.Col([dcc.Graph(id = "graph1", config= {'displayModeBar': False}),], lg=6),
            dbc.Col([dcc.Graph(id = "graph2", config= {'displayModeBar': False}),], lg=6)
            ], justify="center", align="center")
    ]),
    dash_table.DataTable(id = 'review_df',
                     columns = [
                        #  dict(id='rating', name='rating', type='text'),
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
    # Output("graph2", "figure"),
    Input('input1','value')
    
)
def movie_review(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        df = reivew_analysis(input1, 5)

        # 추가(문제 시 주석처리)
        # bar_df = df.data.value_counts('rating').to_frame('count').reindex([str(i) for i in range(11)]).fillna(0)

        # fig1 = go.Figure(
        #     go.Bar(x = bar_df.index.tolist(), 
        #            y = bar_df['count'], 
        #            hovertemplate = '평점: %{x}<br>갯수: %{y:$/0f}<extra></extra>',
        #            marker = {
        #                'color':'#4085f5',# 막대 색상 또는 리스트를 이용하여 각 막대 색상 변경가능
        #                'line':{'color':'black', 'width':3} # 막대 테두리 설정
        #                }))
        
        # pie_df = df.data.value_counts('label').to_frame('count')

        # fig2 = go.Figure(
        #     go.Pie(labels= pie_df.index.tolist(), 
        #            values= pie_df['count'],
        #            textinfo='label+percent',
        #            hovertemplate = '갯수: %{value}<extra></extra>'))

        # fig1.update_layout(margin=dict(l=120, r=120, t=120, b=120),
        #                     hovermode = 'closest',
        #                     showlegend=False,
        #                     plot_bgcolor='white',
        #                     clickmode = 'event+select')
        
        # fig2.update_layout(margin=dict(l=120, r=120, t=120, b=120),
        #             hovermode = 'closest',
        #             showlegend=False,
        #             plot_bgcolor='white',
        #             clickmode = 'event+select')
        # return '{} 영화 리뷰 분석'.format(input1),df.data.to_dict('records'), fig1, fig2
        #        
        return '{} 영화 리뷰 분석'.format(input1), df.data.to_dict('records'), df.create_plot()


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