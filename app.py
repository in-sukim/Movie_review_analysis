from review_prepare import daum
from get_plot import reivew_analysis
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

app = Dash(__name__)
app.layout = html.Div([
    html.H1('영화 리뷰 분석 서비스',style = {'textAlign' : 'center'}),
    html.Br(),
    html.Div([dcc.Input(id="input1", type="text", placeholder="", style={'marginRight':'10px'},debounce = True)],style=dict(display='flex', justifyContent='center')),
    dcc.Graph(id="graph", config={'displayModeBar': False})
        
    ])


@app.callback(
    Output("graph", "figure"),
    Input("input1", "value")
)
def retrun_plot(input1):
    if input1 is None:
        raise PreventUpdate
    else:
        return reivew_analysis(input1, 1).create_plot()

if __name__ == "__main__":
    app.run_server(debug=True)