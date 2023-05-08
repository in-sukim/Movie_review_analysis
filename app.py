from review_prepare import daum
from get_plot import reivew_analysis
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import json
import pandas as pd 

app = Dash(__name__)
app.layout = html.Div([
    html.H1('영화 리뷰 분석 서비스',style = {'textAlign' : 'center'}),
    html.Br(),
    html.Div([dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'},debounce = True),
              dcc.Store(id="current-data")],
              style=dict(display='flex', justifyContent='center')),
    dcc.Graph(id = "graph1", config= {'displayModeBar': False}),
    # dcc.Graph(id = "graph2", config = {'displayModeBar': False}), 
    # html.Div(html.Pre(id = 'graph_area'))
    dash_table.DataTable(id = 'review_df',
                     columns = [
                         dict(id='rating', name='rating', type='text'),
                         dict(id='text', name='text', type='text'),
                        #  dict(id='label', name='label', type='text')
                         ],
                         editable=False,
                        #  row_selectable="multi",
                        #  selected_rows = [],
                        #  is_focused=True,
                         data = [],
                         page_size=10,
                         style_data={
                             'whiteSpace': 'normal',
                             'height': 'auto'},
                             style_cell={'textAlign': 'center',
                                         'fontSize':12, 'font-family':'NanumSquareR'})

        
    ])

# 영화제목을 입력하고 해당 영화에 대한 리뷰 수집 및, 그래프 시각화
@app.callback(
    Output('current-data', 'data'),
    Output("graph1", "figure"),
    Input("input1", "value")
)
def retrun_plot(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        df = reivew_analysis(input1, 5)
        return df.data.to_dict('records'), df.create_plot()

# 클릭한 데이터에 해당하는 리뷰 출력
@app.callback(
    # Output("graph_area", "children"),
    Output('review_df', 'data'),
    Input('current-data','data'),
    Input("graph1", "clickData")
)
def return_plot(data,clickData):
    if clickData is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(data)
        condition1 = df['label'] == clickData['points'][0]['label']
        condition2 = df['rating'] == clickData['points'][0]['label']

        df = df.loc[condition1 | condition2]
        return df.to_dict('records')
        # return json.dumps(df.to_dict('records'), indent = 2, ensure_ascii = False)

if __name__ == "__main__":
    app.run_server(debug=True)