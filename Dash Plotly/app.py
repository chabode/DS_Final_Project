import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from plotly import tools
from dash.dependencies import Input, Output
import numpy as np
# from categoryplot import dfDict, getPlot

app = dash.Dash(__name__)
server = app.server # make python obj with Dash() method

app.title = 'Bank Marketing Loan Project'; # set web title
df = pd.read_csv('bank.csv');
df_kgl = pd.read_csv('bank_kgl.csv');
data_kgl = df_kgl.drop(['range_age','range_dur','range_pdays'], axis=1)

# listGOFunc = {
#     "bar": go.Bar,
#     "violin": go.Violin,
#     "box": go.Box
# }
dfDict = {
    'bank': df,
    'bank_kgl': data_kgl,
}
#the layout/content
app.layout = html.Div(children=[
    dcc.Tabs(id="tabs", value='tab-1', 
        style={
            'fontFamily': 'system-ui'
        },
        content_style={
            'fontFamily': 'Arial',
            'borderLeft': '1px solid #d6d6d6',
            'borderRight': '1px solid #d6d6d6',
            'borderBottom': '1px solid #d6d6d6',
            'padding': '44px'
        }, 
        children=[
            dcc.Tab(label='Project Introduction', value='tab-1', children=[
                html.Div([ 
                    html.Div(id='divParagraph', children=[
                        html.H1('Overview'),
                        html.H3('Introduction of Datasets'),
                        html.P('This data is related with direct marketing campaigns of a Portuguese banking institution.'),
                        html.P('The marketing campaigns were based on phone calls and telephone calls.'),
                        html.P('Often, more than one contact to the same client was required, in order to access if the product (bank term deposit) would be (or not) subscribed'),
                        # html.P('in order to access if the product (bank term deposit) would be (or not) subscribed'),

                        html.H3('Goals :'),
                        html.P('To predict if the client will subscribe a term deposit (or not).'),

                        html.H3('Attribute Informations :'),
                        html.H4('Bank Client Data :'),
                        html.P('1. Age'),
                        html.P('2. Job'),
                        html.P('3. Marital'),
                        html.P('4. Education'),
                        html.P('5. Default'),
                        html.P('6. Balance'),
                        html.P('7. Housing'),
                        html.P('8. Loan'),
                        html.H4('Related with last contact of the current campaign :'),
                        html.P('9. Contact'),
                        html.P('10. Day'),
                        html.P('11. Month'),
                        html.P('12. Duration'),
                        html.H4('Other Attribute :'),
                        html.P('13. Campaign'),
                        html.P('14. Pdays'),
                        html.P('15. Previous'),
                        html.P('16. Poutcome'),
                    ])
                ])
            ]),
            dcc.Tab(label='Bank Dataset', value='tab-2', children=[
                html.Div([ 
                    html.Div(id='divTable', children=[
                        html.H1('Data Bank'),
                        html.H4(['Total Row : ' + str(len(data_kgl))]),
                        dcc.Graph(
                            id='tableData',
                            figure= {
                                'data': [
                                    go.Table(
                                        header=dict(
                                            values=['<b>'+ col +'</b>' for col in data_kgl.columns],
                                            font = dict(size = 14),
                                            height = 30,
                                            fill = dict(color='#a1c3d1')
                                        ),
                                        cells=dict(
                                            values=[data_kgl[col] for col in data_kgl.columns],
                                            font = dict(size = 12),
                                            height = 30,
                                            fill = dict(color='#EDFAFF'),
                                            align = ['right']
                                        )
                                    )
                                ],
                                'layout': dict(height=500,margin={'l': 0, 'b': 40, 't': 10, 'r': 0})
                            }
                        )
                    ])
                ])
            ]),
            dcc.Tab(label='Total Amount Each Categories', value='tab-3', children=[
                html.Div([
                    html.H3('Total Amount of :'),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Category : '),
                                dcc.Dropdown(
                                    id='ddl-x-plot-category',
                                    options=[{'label': 'Age', 'value': 'age'},
                                             {'label': 'Job', 'value': 'job'},
                                             {'label': 'Marital', 'value': 'marital'},
                                             {'label': 'Education', 'value': 'education'},
                                             {'label': 'Contact', 'value': 'contact'},
                                             {'label': 'Day', 'value':'day'},
                                             {'label': 'Month', 'value':'month'}                                                                                          
                                             ],
                                    value='age'
                                )
                            ]),
                        ])
                    ], style={ 'width' : '300px'}),
                    dcc.Graph(
                        id='categoricalPlot',
                        figure={
                            'data': []
                        }
                    )
                ])
            ]),
            dcc.Tab(label='Ratio Each Categories', value='tab-4', children=[
                html.Div([
                    html.H3(
                        children='Ratio Acquired and Rejected Deposits Based on Categories'
                    ),
                    html.Table([
                        html.Tr([
                            html.Td([
                                html.P('Category : '),
                                dcc.Dropdown(
                                    id='ddl-histo-column',
                                    options=[{'label': 'Age', 'value':'range_age'},
                                             {'label': 'Job', 'value':'job'},
                                             {'label': 'Marital', 'value':'marital'},
                                             {'label': 'Education', 'value': 'education'},
                                             {'label': 'Contact', 'value': 'contact'},                                            
                                             {'label': 'Day','value':'day'},
                                             {'label': 'Month', 'value':'month'},
                                             {'label': 'Duration','value':'range_dur'},
                                             {'label': 'Pdays', 'value':'range_pdays'}
                                             ],
                                    value='range_age'
                                )
                            ])
                        ])
                    ],
                        style={'width':'300px'},
                    ),
                    dcc.Graph(
                        id='histogramPlot',
                        figure={
                        }
                    )
                ])
            ]),
    ])
], 
style={
    'maxWidth': '1200px',
    'margin': '0 auto'
});

@app.callback(
    Output('categoricalPlot', 'figure'),
    [Input('ddl-x-plot-category', 'value')])
def update_category_graph(xcategory):
    dframe = data_kgl
    # dataf = dframe.groupby([xcategory,'got_loan']).sum()[ycategory].reset_index().sort_values([ycategory,'got_loan'], ascending=False)
    return {
            'data': 
            # getPlot('bank', ddljeniscategory,ddlxcategory,ddlycategory)
            [
            go.Histogram(
                x=dframe[xcategory],
                # x=dataf[xcategory],
                nbinsx=25,
                # text=dfDict[table]['deck'],
                opacity=0.7,
                # name='Total',
                # marker=dict(color='blue')
            )
            ],
            'layout': go.Layout(
                xaxis={'title': xcategory.capitalize()}, 
                yaxis={'title': 'Count'},
                margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
                legend={'x': 0, 'y': 1.2}, hovermode='closest',
                # plot_bgcolor= 'black', paper_bgcolor= 'black',
            )
    }

@app.callback(
    Output('histogramPlot','figure'),
    [
        Input('ddl-histo-column','value')
    ]
)
def update_histo_graph(ddlhisto):
    histo1 = go.Histogram(
        x=df_kgl[df_kgl['deposit']=='yes'][ddlhisto],
        nbinsx= 30,
        marker=dict(color='blue'),
        name='Acquried',
        legendgroup='acquried'
    )
    histo2 = go.Histogram(
        x=df_kgl[df_kgl['deposit']=='no'][ddlhisto],
        nbinsx= 30,
        marker=dict(color='orange'),
        name='Rejected',
        legendgroup='rejected'
    )
    return {
        'data' : [
            histo1,histo2
        ],
        'layout' : go.Layout(
            xaxis={'title':ddlhisto.capitalize()},
            yaxis={'title':'Count'},
            margin={'l':40, 'b':40, 't':10, 'r':10},
            legend={'x':1, 'y':1.2}, hovermode='closest',
        )
    }

if __name__ == '__main__':
    # run server on port 1997
    # debug=True for auto restart if code edited
    app.run_server(debug=True, port=1993) 

