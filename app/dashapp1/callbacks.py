from datetime import datetime as dt

import pandas_datareader as pdr
import pandas as pd 
import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, plot, iplot
import plotly.express as px
from dash.dependencies import Input
from dash.dependencies import Output


"""def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
    def update_graph(selected_dropdown_value):
        df = pdr.get_data_yahoo(selected_dropdown_value, start=dt(2017, 1, 1), end=dt.now())
        return {
            'data': [{
                'x': df.index,
                'y': df.Close
            }],
            'layout': {'margin': {'l': 40, 'r': 0, 't': 20, 'b': 30}}
        }"""
##################################
def register_callbacks(dashapp):
    @dashapp.callback(Output('my-graph', 'figure'),
        [Input('interval-component', 'interval')])
    def update_graph(interval):

        df = pd.read_csv("/home/turan/Documents/repos/financial/data/result.csv", 
                    names=['index','date','hi','lo','close','open','high','low',
                             'real_hi','real_lo', 'pred_1', 'calc_1', 'rsi', 'rsi_t'],
                    parse_dates=['date'])

        df.loc[df.hi < 0.10, 'hi'] = np.nan
        df.loc[df.lo < 0.12, 'lo'] = np.nan
        df.loc[df.hi > 0.10, 'hi'] = df.loc[df.hi > 0.10, 'close']
        df.loc[df.lo > 0.12, 'lo'] = df.loc[df.lo > 0.12, 'close']
        df.loc[df.real_hi < 0.10, 'real_hi'] = np.nan
        df.loc[df.real_lo < 0.12, 'real_lo'] = np.nan
        df.loc[df.real_hi > 0.10, 'real_hi'] = df.loc[df.real_hi > 0.10, 'close']
        df.loc[df.real_lo > 0.12, 'real_lo'] = df.loc[df.real_lo > 0.12, 'close']

        data = df.tail(720)

        # Initialize figure with subplots
        fig = make_subplots(
            rows=2, cols=1,
            row_heights=[0.8, 0.2],
            shared_xaxes=True,
            subplot_titles=("Price and Signals", "RSI")
            #specs=[[{"secondary_y": True}]]
        )

        fig.add_trace(go.Scatter(x=data.date, 
                            y=data.close, 
                            mode='lines',  
                            marker=dict(size=6, color='blue'),
                            name='Close'),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=data.date, 
                            y=data['real_hi'], 
                            mode='markers', 
                            marker=dict(size=12,color='green',symbol='triangle-up-dot'), 
                            name='Hi'),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=data.date,
                            y=data['real_lo'],
                            mode='markers', 
                            marker=dict(size=12, color='red', symbol='triangle-down-dot'), 
                            name='Lo'),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=data.date, 
                            y=data['hi'], 
                            mode='markers', 
                            marker=dict(size=12,color='green',symbol='triangle-up-open'), 
                            name='Hi'),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=data.date,
                            y=data['lo'],
                            mode='markers', 
                            marker=dict(size=12, color='red', symbol='triangle-down-open'), 
                            name='Lo'),
                     row=1, col=1)
        fig.add_trace(go.Scatter(x=data.date, 
                            y=data.rsi, 
                            mode='lines',  
                            marker=dict(size=6, color='black'),
                            name='RSI'),
                     row=2, col=1)

        # Set theme, margin, and annotation in layout
        fig.update_layout(
            #template="plotly_dark",
            margin=dict(r=10, t=125, b=40, l=60),
            #height=700, width=1000,
            title=dict(text="USDTRY Predictions and Close Price"),
                      paper_bgcolor = '#fff',
                      plot_bgcolor  = '#fff',
                      yaxis = dict(showgrid=True, zeroline=True, gridcolor='rgb(204, 255, 255)')
            
        )
        return fig