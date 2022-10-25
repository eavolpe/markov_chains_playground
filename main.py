

from dash import html, dash, Input, Output, dash_table
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import dash_cytoscape as cyto

app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])
app.title = 'Markov chains playgrounds'
colors = {
    'text' :'#FFFFFF'}
select_size_tm = dbc.Select(
    id="select_size_tm",
    options=[
        {"label": "Two element markov chain", "value": 2},
        {"label": "Three element markov chain", "value": 3},
    ],
)

def transition_matrix_fe(dim):
    div_children = []
    for i in range(dim):
        temp_row =[]
        for j in range(dim):
            temp_row.append(dbc.Col(
                dbc.Input(id="transition_matrix_"+str(j)+str(i), 
                                # type="number",
                                # inputmode= 'numeric',
                                min=1,
                                max = 0,
                                step = 0.1
                                )))
        div_children.append(dbc.Row(children = temp_row))
    return html.Div(div_children)





graph_1 =   cyto.Cytoscape(
        id='cytoscape-two-nodes',
        layout={'name': 'preset'},
        style={'width': '100%', 'height': '400px'},
        elements=[
            {'data': {'id': 'one', 'label': 'Node 1'}, 'position': {'x': 75, 'y': 75}},
            {'data': {'id': 'two', 'label': 'Node 2'}, 'position': {'x': 200, 'y': 200}},
            {'data': {'source': 'one', 'target': 'two'}}
        ]
    )


@app.callback(
    [Output('transition_matrix_fe','children')],
    [Input('select_size_tm','value')],
    prevent_initial_call= True
)
def show_input_numbers_tm(value):
    return [transition_matrix_fe(int(value))]

app.layout =  html.Div(children=[
    html.Center(children = [
        html.H1(children='''Markov chains playgrounds''',
                className="display-3",
                style = {
                        'color' :colors['text'] 
                        })]),
    select_size_tm,
    html.Div(id = 'transition_matrix_fe'),
    html.Div(children = [graph_1],
    style={"border":"2px white solid"}

    )
    
    ])




if __name__ == '__main__':
    app.run_server(debug=True)