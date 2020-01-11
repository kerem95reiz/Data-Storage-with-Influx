from queue import Queue
from concurrent.futures import ThreadPoolExecutor
import threading
import time
from flask import Flask, request
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from traceback import print_exc
import requests as req
import json
import sys

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
DB_NAME = 'mydb'
MEASUREMENT = 'lat_vals'
PERIOD = 1 # 1 sec
URL = 'http://rest_api:4545'

server = Flask(__name__)
app = dash.Dash(
    __name__,
    server=server,
    routes_pathname_prefix='/dash/',
    external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([      
        dcc.Graph(
            id='real-time'
        ),
        dcc.Interval(
            id='interval-component',
            interval=1000*PERIOD,
            n_intervals=0
        )
    ]),
    html.Div([
        dcc.Graph(id="filtered"),
        html.Div([
            dcc.Dropdown(
                id='cpu-tbd',
                placeholder="Cpu"
            )]),
        html.Div([
            dcc.Dropdown(
                id='priority-tbd',
                placeholder="Priority"
            )]),
        html.Div([
            dcc.Dropdown(
                id='interval-tbd',
                placeholder="Interval"
            )])
        ,
        html.Button(id='update-button', children='Submit', n_clicks=0),
        ])
    ])

def insert_data_into_graph(data):
    # This function takes a list of two lists that consists of values for x- and y-axis respectively and inserts those values into the graph.

    # Length check
    if (len(data) != 2):
        print_exc()
        raise Exception
    # content length check
    if (len(data[0]) != len(data[1])):
        print_exc()
        raise Exception

    return {
    'data':
    [
        dict(
            x=data[0],  # latency category
            y=data[1],  # amount of bins
            mode='lines+markers',
            type="bar",
            text=None,
            marker=dict(
                size=12,
                opacity=0.8
            )
        )
    ],
    'layout':
        {
            'title': 'Latency Visualisation',
            'xaxis': {
                'title': 'Latencies'
            },
            'yaxis': {
                'title': 'Number of latencies'
            }
            ,
            'zaxis': {
                'title': 'time'
            }
    }

    }

#This updates the data of the real time graph
@app.callback(Output(component_id='real-time', component_property='figure'),
              [Input('interval-component', 'n_intervals')])
def update_data(n_clicks):
    try:
        data = periodic_reading(DB_NAME, MEASUREMENT, PERIOD)  # data as string
        data = json.loads(data.text)  # data as json
        data = _compute_categories_and_amount_of_them(data) # Prepare the data form
    except Exception:
        print_exc()
    data_with_dimensions = _put_data_into_dimensions(data)
    return insert_data_into_graph(data_with_dimensions)

def _put_data_into_dimensions(data):
    category_axis = []
    amount_of_category = []
    time_axis = []
    for data_point in data:
        for key, value in data_point.items():
            if key == 'time':
                time_axis.append(data_point[key])
            else:
                category_axis.append(key)
                amount_of_category.append(value)
    return [category_axis, amount_of_category]

# this function displays the data set based on the filter results that are entered by the user
@app.callback(Output(component_id='filtered', component_property='figure'),
              [Input(component_id='update-button', component_property='n_clicks')],
              [State(component_id='cpu-tbd', component_property='value'),
              State(component_id='priority-tbd', component_property='value'),
              State(component_id='interval-tbd', component_property='value')])
def display_filtered_data(btn_clicks, f_cpu, f_priority, f_interval):
    # this if cond. prevent sending the unfilled query to the api
    if f_cpu is None and f_interval is None and f_priority is None:
        return insert_data_into_graph([[], []])
    filters = [ { 'cpu': f_cpu }, 
                { 'priority': f_priority }, 
                {'interval' : f_interval }
            ]
    # This block deletes None value filters that are not set
    non_none_filters = []
    for filt in filters:
        for v in filt.values():
            if v is not None:
                non_none_filters.append(filt)

    # This block composes a query with chosen filter values
    filter_query = str('SELECT slot, value FROM ' + MEASUREMENT + ' WHERE ')
    for filt_ind in range(len(non_none_filters)):
        for key, val in non_none_filters[filt_ind].items():
            if filt_ind == len(non_none_filters)-1: #This condition prevents that there is an 'AND' at the end of the query
                filter_query += "".join(["{}='{}'".format(key, val)])
            else:
                filter_query += "".join(["{}='{}' AND ".format(key, val)])

    params = {
        'db_name': DB_NAME,
        'measurement': MEASUREMENT,
        'query': filter_query
    }
    try:
        data = req.get(URL+'/query', params=params) # Receive the response and then convert it to JSON
        data = json.loads(data.text)
    except Exception:
        print_exc()
        raise Exception

    data = _compute_categories_and_amount_of_them(data)
    data_with_dimensions = _put_data_into_dimensions(data)
    return insert_data_into_graph(data_with_dimensions)

# Retrieve data from the server
def periodic_reading(db_name, measurement, period):
    # InfluxDB works in nanoseconds, so time needs to be sent to db as nanoseconds as well
    current_time = time.time_ns()
    payload = {'db_name': db_name, 'measurement': measurement,
               'period': period, 'current_time': current_time}
    try:
        # TODO: After finishin filter implementation, use URL for the following request
        latest_entries = req.get(
            'http://rest_api:4545/readlastentries', params=payload)
    except Exception:
        print_exc()
        raise Exception

    return latest_entries

# This finds out what the samples are and how many samples there are in that specific range. Such [2, 5, 4, 15] -> {"10": 3, "20": 1}
def _compute_categories_and_amount_of_them(data):
    categs_and_amounts = []
    for val in data:
        temp = {}
        temp[val['slot']] = val['value']
        temp['time']=val['time']
        categs_and_amounts.append(temp)
    return categs_and_amounts

# Update the content of the filters
@app.callback([Output(component_id='cpu-tbd', component_property='options'),
              Output(component_id='priority-tbd', component_property='options'),
              Output(component_id='interval-tbd', component_property='options')],
                [Input(component_id='interval-component', component_property='n_intervals')])
def loadFilterContent(n):
    try:
        criteria = req.get(URL+'/criteria', params={'db_name': DB_NAME, 'measurement': MEASUREMENT})
        criteria = criteria.json()
    except Exception:
        print_exc()
 
    cpu = [{'label': i, 'value': i} for i in criteria['cpu']]
    priority = [{'label': i, 'value': i} for i in criteria['priority']]
    interval = [{'label': i, 'value': i} for i in criteria['interval']]

    return cpu, priority, interval

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)
