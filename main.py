

from math import sqrt
from dash import html, dash, Input, Output, ALL, State
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import dash_cytoscape as cyto

#backend----------------------------------------------------------------------------------------
#is a squeare matrix a valid transition matrix?
#m is of the form [[],[],] contains row vectors
def valid_square_matrix(m):
    #check rows
    n = 0
    for i in m:
        if sum(i) == 1:
            n+=1
    if n == len(m):
        return True
    else:
        return False


#front end-------------------------------------------------------------------------------------
app = dash.Dash(external_stylesheets=[dbc.themes.QUARTZ])
app.title = 'Markov chains playgrounds'
colors = {
    'text' :'#FFFFFF'}
select_size_tm = dbc.Select(
    id="select_size_tm",
    value = 2,
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
                dbc.Input(id={'type': 'input_tm',
                            'index': str(i)+str(j)},
                                type="number",
                                # inputmode= 'numeric',
                                min=0,
                                max = 1,
                                step = 0.05
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
    #prevent_initial_call= True
)
def show_input_numbers_tm(value):
    return [transition_matrix_fe(int(value))]

@app.callback(
    [Output('Alert','children'),
    Output('Alert','color')],
    [Input({'type': 'input_tm','index':ALL}, 'value')],
    prevent_initial_call= True
    )

def valid_tm(values):
    if None in values:
        # print(values)
        return ['Error: Insert all values in the transition matrix','danger']
    else:
        temp_list = []
        n = int(sqrt(len(values)))
        print(n)
        for i in range(n):
            temp_list.append(values[i*n:((i+1)*n)])
        print(temp_list)
        if valid_square_matrix(temp_list):
            return ['Valid transition matrix: all rows are probability distributions','success'] 
        else:
            return ['Not all rows form a probability distribution',['danger']]

@app.callback(
    [Output({'type': 'input_tm','index':ALL}, 'value')],
    [Input('generate_random_inputs','n_clicks')],
    [State('select_size_tm','value')],
    prevent_initial_call =True
    
)
def generate_random(n_clicks,state):
    
    return [[0.1,0.9,0.2,0.8]]


app.layout =  html.Div(children=[
    html.Center(children = [
        html.H1(children='''Markov chains playgrounds''',
                className="display-3",
                style = {
                        'color' :colors['text'] 
                        })]),
    html.H3('1. Select the number of elements in the markov chain',
        className="display-5"),
    select_size_tm,
    html.H3('2. Input the values in the transition matrix',
        className="display-5"),
    html.P('Or select them at random'),
    dbc.Button("Generate the transition matrix randomly",
            color="warning", 
            className="me-1",
            id='generate_random_inputs'),
    html.Div(id = 'transition_matrix_fe'),
    dbc.Alert("Insert values", color="primary",
            # className="me-1",
            id='Alert'),
    html.Div(children = [graph_1],
            style={"border":"2px white solid"}),

    
    
    ])




if __name__ == '__main__':
    app.run_server(debug=True)