from dash import Dash, dcc, html, dash_table,callback
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json
import pandas as pd 
import dash 

from modules.sentiment_review import reivew_analysis
from modules.info_prepare import get_movie_info
from modules.review_prepare import daum


dash.register_page(__name__)
layout = html.Div([
    html.H1('영화 리뷰 분석 서비스',style = {'textAlign' : 'center'}),
    html.Br(),
    # html.Div([dcc.Store(id="current-data")]),
    # html.Div(id = 'graph_area'),
    dcc.Graph(id = "graph1", config= {'displayModeBar': False}),

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

        
    ])

# 영화제목을 입력하고 해당 영화에 대한 리뷰 수집 및, 그래프 시각화
# @app.callback(
@callback(
    # Output('current-data', 'data'),
    Output("graph1", "figure"),
    Input('search_movie_review','data')
    
)
def return_plot(data):
    if data is None:
        raise PreventUpdate
    else:
        # df = pd.DataFrame(data)
        return data.create_plot()
# def retrun_plot(input1):
#     if input1 is None:
#         raise PreventUpdate
#     else:
#         df = reivew_analysis(input1, 5)
#         return df.data.to_dict('records'),df.create_plot()
        

# 클릭한 데이터에 해당하는 리뷰 출력
@callback(
    Output('review_df', 'data'),
    Input('search_movie_review','data'),
    Input("graph1", "clickData")
)
def return_plot(data,clickData):
    if clickData is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        if clickData['points'][0]['label'] in [str(i) for i in range(10)]:
            condition = df['rating'] == clickData['points'][0]['label']
            df = df.loc[condition]
            return df.to_dict('records')
        else:
            return None
        # condition1 = df['label'] == clickData['points'][0]['label']
        # condition2 = df['rating'] == clickData['points'][0]['label']

        # df = df.loc[condition1 | condition2]
        # return df.to_dict('records')

# if __name__ == "__main__":
#     app.run_server(debug=True)