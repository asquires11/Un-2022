import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import dash_table

app = dash.Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

fig = go.Figure()

# vader results
df = pd.read_csv('Vader_results_1.csv')

df = df.rename(columns={'Unnamed: 0': 'thing'})

df_date = pd.read_csv(
    'US_COMPOUND_SENTIMENT_AND_DATE.csv')

top_hashtag = pd.read_csv(
    'tophashtag.csv')

sentiment_scores = pd.read_csv(
    'sentiment_scores.csv')

# build app
# _________________________________________________


app.layout = html.Div(
    children=[
        html.Div([
            html.Br(),
            html.H3('COVID-19 AND EDUCATION',
                    style={'color': '#7fafdf', 'margin-left': '5%', 'fontFamily': 'Playfair Display'},className='app-header--title')

        ]),

        html.Br(),

        html.Div([
            dbc.Row(
                [

                    dbc.Col(md=3, children=[

                        dbc.Card(
                            dbc.CardBody([
                                dbc.Tabs(id="tabs", active_tab="tab_1",

                                         children=[

                                             dbc.Tab(tab_id="tab_1", label="Country",
                                                     style={'fontFamily': 'HelveticaNeue', 'color': "#7fafdf"},
                                                     children=[
                                                         dbc.Container([
                                                             html.Br(),
                                                             html.H5('Choose a Country:',
                                                                     style={'fontFamily': 'Open Sans',
                                                                            'color': "#7fafdf", 'margin-left': '5%'}),
                                                             html.Br(),
                                                             html.Div(style={'fontColor': '#7fafdf'}, children=
                                                             dcc.Dropdown(
                                                                 id='demo-dropdown',
                                                                 options=[
                                                                     {'label': 'United States', 'value': 'US'},
                                                                     {'label': 'China', 'value': 'CHN'}
                                                                 ],
                                                                 value='US',
                                                                 style={'height': '35px', 'position': 'relative',
                                                                        'backgroundColor': '#1f2630',
                                                                        'fontColor': '#7fafdf',
                                                                        'font': {'color': 'white'}}
                                                             ),
                                                                      ),
                                                             html.Br(),

                                                             html.Div(id='output-panel',
                                                                      style={'backgroundColor': '#1f2630'}),

                                                         ], style={'color': '#1f2630'}, fluid=True),
                                                     ]),
                                             dbc.Tab(tab_id="tab_2", label="Hashtags", children=[
                                                 dbc.Container([

                                                     html.Br(),
                                                     html.P("Top 20 Hashtags:",
                                                            style={'fontFamily': 'HelveticaNeue', 'color': '#7fafdf',
                                                                   'margin-left': '5%'}),
                                                     html.Div(
                                                         id='Table',

                                                     )

                                                 ], fluid=True)
                                             ])
                                         ])
                            ], style={'backgroundColor': '#252e3f', 'height': '650px', 'fontFamily': 'HelveticaNeue',
                                      'fontColor': '#7fafdf'},

                            ), style={'backgroundColor': '#252e3f', 'height': '690px', 'margin-left': '5%'}),

                    ]),

                    dbc.Col(html.Div(dbc.Card(
                        dbc.CardBody([
                            dcc.Graph(id='sentiment-dates', style={'backgroundColor': '#fdfe2', 'height': '650px'}),

                        ]), style={'backgroundColor': '#252e3f'}

                    )), md=9)

                ]
            )
        ]
        ),

    ],
    style={'backgroundColor': '#1f2630', 'width': '100%', 'height': '900px'}
)


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_output(value):
    return 'You have selected "{}"'.format(value)


@app.callback(
    dash.dependencies.Output('sentiment-dates', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value')])
def update_graph(value):
    dff = df_date[df_date['country'] == value]

    fig = px.line(dff, x='date', y='compound')

    fig.update_traces(mode='lines+markers', line_color='#2cfec1')

    fig.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                     tickfont=dict(family='HelveticaNeue', color='#2cfec1', size=14))

    fig.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                     tickfont=dict(family='HelveticaNeue', color='#2cfec1', size=14))

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       bgcolor='rgba(0, 0,0,0)')

    fig.update_layout(height=650, margin={'l': 100, 'b': 50, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                      paper_bgcolor='#1f2630', title_text='Compound Sentiment of Tweets by Date', title_x=0.5,
                      font=dict(family='HelveticaNeue',
                                size=12,
                                color='#2cfec1'), xaxis_title='Date',
                      yaxis_title='Compound Sentiment Score')

    return fig


@app.callback(
    # Button: switch to Tab 2
    Output("tabs", "active_tab"),
    [Input("button_tab_1", "n_clicks")])
def tab_resources(click):
    if click:
        return "tab_2"


@app.callback(

    Output('Table', 'children'),
    [Input('demo-dropdown', 'value')])
def update_table(value):
    dft = top_hashtag[top_hashtag['Country'] == value]
    return html.Div(dash_table.DataTable(
        id='Table',

        columns=[{'id': c, 'name': c} for c in dft.columns],

        page_size=50

    ))





# run app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=False)
