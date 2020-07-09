import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np
import dash_table as dt

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

fig = go.Figure()

# vader results
df = pd.read_csv('Vader_results_1.csv')

df = df.rename(columns={'Unnamed: 0': 'thing'})

df_date=pd.read_csv('compound_date.csv')
#df_date = pd.read_csv(
   # 'US_COMPOUND_SENTIMENT_AND_DATE.csv')

sentiment_scores = pd.read_csv(
    'sentiment_scores.csv')

top_hashtag = pd.read_csv('tophashtag_final.csv')

bigrams = pd.read_csv('bigrams.csv')

states = top_hashtag.Country.unique().tolist()

# build app
# _________________________________________________


app.layout = html.Div(
    children=[
        html.Div([
            html.Br(),
            html.H4('COVID-19 AND EDUCATION',
                    style={'color': '#7fafdf', 'margin-left': '5%'}, className='app-header--title'),
            html.P(
                    id="description",
                    children="† Deaths are classified using the International Classification of Diseases, \
                    Tenth Revision (ICD–10). Drug-poisoning deaths are defined as having ICD–10 underlying \
                    cause-of-death codes X40–X44 (unintentional), X60–X64 (suicide), X85 (homicide), or Y10–Y14 \
                    (undetermined intent).",
                ),

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
                                                     style={  # 'fontFamily': 'Helvetica Neue',
                                                         'color': "#7fafdf"},
                                                     children=[
                                                         dbc.Container([
                                                             html.Br(),
                                                             html.H5('Choose a Country:',
                                                                     style={
                                                                         'color': "#7fafdf", 'margin-left': '5%'}),
                                                             html.Br(),
                                                             html.Div(style={'fontColor': '#7fafdf'}, children=
                                                             dcc.Dropdown(
                                                                 id='demo-dropdown',
                                                                 options=[
                                                                     {'label': 'United States', 'value': 'US'},
                                                                     {'label': 'China', 'value': 'CHN'},
                                                                     {'label': 'Nigeria','value':'Nigeria'},
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
                                                     html.H5("Top 20 Hashtags:",
                                                             style={  # 'fontFamily': 'HelveticaNeue',
                                                                 'color': '#7fafdf',
                                                                 'margin-left': '5%'}),
                                                     html.Br(),
                                                     html.Div(
                                                         # id='Table',

                                                         children=[
                                                             # dcc.Dropdown(
                                                             # id='filter_dropdown',
                                                             # options=[{'label':st, 'value':st} for st in states],
                                                             # value = states[0]
                                                             # ),
                                                             dt.DataTable(id='table-container',
                                                                          columns=[{'id': c, 'name': c} for c in
                                                                                   top_hashtag.columns[:2].values],
                                                                          fixed_rows={'headers': True},
                                                                          style_table=dict(overflowX='auto',
                                                                                           minWidth='100%'),
                                                                          style_cell_conditional=[
                                                                              {'if': {'column_id': 'Hashtag'},
                                                                               'width': '50%'}],
                                                                          style_cell={'minWidth': '5px', 'width': '8px',
                                                                                      'maxWidth': '10px',
                                                                                      'height': 'auto',
                                                                                      'color': '#7fafdf',
                                                                                      'backgroundColor': '#1f2630',
                                                                                      'textAlign': 'center',
                                                                                      'fontFamily': 'Helvetica Neue'}
                                                                          )
                                                         ]

                                                     )

                                                 ], fluid=True)
                                             ])
                                         ])
                            ], style={'backgroundColor': '#252e3f', 'height': '650px',  # 'fontFamily': 'HelveticaNeue',
                                      'fontColor': '#7fafdf'},

                            ), style={'backgroundColor': '#252e3f', 'height': '690px', 'margin-left': '5%'}),

                    ]),

                    dbc.Col(html.Div(dbc.Card(
                        dbc.CardBody([

                            # html.Img(
                            # src=app.get_asset_url("Rplot03.png"),),
                            # html.Br(),

                            # dcc.Graph(id='sentiment-dates', style={'backgroundColor': '#fdfe2', 'height': '650px'}),

                            # html.Br(),

                            dbc.Tabs(className="nav nav-pills", children=[

                                dbc.Tab(tab_id="tab_4", label="Bigrams",
                                        style={  # 'fontFamily': 'Helvetica Neue',
                                            'color': "#7fafdf"},
                                        children=[
                                            dbc.Container([
                                                html.Br(),
                                                html.H5('How Many Bigrams would you like to see:',
                                                        style={
                                                            'color': "#7fafdf", 'margin-left': '5%'}),
                                                html.Br(),
                                                html.Div(style={'fontColor': '#7fafdf'}, children=
                                                dcc.Dropdown(
                                                    id='number-dropdown',
                                                    options=[
                                                        {'label': 10, 'value': 10},
                                                        {'label': '20', 'value': 20},
                                                        {'label': '30', 'value': 30},
                                                        {'label': '40', 'value': 40},
                                                    ],
                                                    value=10,
                                                    style={'height': '35px', 'position': 'relative',
                                                           'backgroundColor': '#1f2630',
                                                           'fontColor': '#7fafdf',
                                                           'font': {'color': 'white'}}
                                                ),

                                                         ),
                                                html.Br(),

                                                dcc.Graph(id='bigrams',
                                                          style={'backgroundColor': '#fdfe2', 'height': '485px'}),

                                            ], style={'color': '#1f2630'}, fluid=True),
                                        ]),

                                dbc.Tab(label="Dates",
                                        children=[

                                            html.Br(),
                                            dcc.Graph(id="sentiment-dates",
                                                      style={'backgroundColor': '#fdfe2', 'height': '650px'}),
                                        ],
                                        ),
                                # dbc.Tab(
                                # dcc.Graph(id='bigrams', style={'backgroundColor': '#fdfe2', 'height': '650px'}),
                                # label='Bigrams'),
                                dbc.Tab(html.Iframe(
                                    id='nodes_1',
                                    src=None, width='100%',style={'height':'100rem'}),
                                    label="nodes"),
                               
                                dbc.Tab(html.Div([
                                    html.Br(),
                                    html.Iframe(
                                    id='co-oc',
                                    src=None, width='100%',style={'height':'100rem'})]),
                                    label="Network", style=dict(border=33)),

                                # dbc.Tab( html.Img(
                                # src=app.get_asset_url('Rplot06.png'),style={'backgroundColor': '#fdfe2', 'height': '650px','width':'1050px'}),style={'backgroundColor': '#fdfe2', 'height': '650px'}, label="Sentiment")
                                dbc.Tab(html.Iframe(
                                    id='sentiment',
                                    src=None, width='100%', style={'height':'100rem'}),
                                    label="Sentiment", style=dict(border=33)),

                            ]),

                            # dcc.Graph(id='sentiment-dates', style={'backgroundColor': '#fdfe2', 'height': '650px'}),
                            html.Br(),
                            html.Div(

                                # children=[
                                # dcc.Dropdown(
                                #   id='filter_dropdown',
                                #  options=[{'label':st, 'value':st} for st in states],
                                #  value = states[0]
                                #  ),
                                #  dt.DataTable(id='table-container', columns=[{'id': c, 'name': c} for c in top_hashtag.columns.values],style_table=dict(overflowX='auto', minWidth='100%',style_cell={'minWidth': '5px', 'width': '8px', 'maxWidth': '10px','height': 'auto',  'color': '#7fafdf','backgroundColor':'#1f2630','textAlign':'center',
                                # 'fontFamily':'Helvetica Neue'}))
                                # ]
                            ),

                        ]), style={'backgroundColor': '#252e3f'}

                    )), md=9),

                ]
            ), html.Div(
        [
            html.H4('Acknowledgements and Data Sources',
                    style={"margin-top": "0"}),
            dcc.Markdown('''\
**Important Data Caveats:**  Due to anonymized data, access to individual tweets is not available. See [FAQ](https://github.com/asquires11/un) for details.
- Special Thanks to Polly Zhang for doing the computing and analysis of the China data
- Text data used with permission from Twitter and Weibo, [Twitter](https://www.twitter.com/).
- Text analysis used Quanteda [Quanteda]
- Network Correlation developed with [visNetwork](https://datastorm-open.github.io/visNetwork/).
- Dashboard developed with [Plot.ly Dash](https://plotly.com/dash/).
- For source code and data workflow, please contact [Annika Squires](annikasquires@icloud.com).
'''),
        ],
        style={
            'width': '98%',
            'margin-right': '0',
            'padding': '10px',
        },
        className='twelve columns pretty_container',
    ),
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

    fig.update_traces(mode='lines+markers', line_color='#7fafdf')  # '#2cfec1')

    fig.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                     tickfont=dict(  # family='Helvetica Neue',

                         color='#7fafdf', size=14))

    fig.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                     tickfont=dict(family='Helvetica Neue', color='#7fafdf', size=14))

    # fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #  xref='paper', yref='paper', showarrow=False, align='left',
    #  bgcolor='rgba(0, 0,0,0)')

    fig.update_layout(margin={'l': 100, 'b': 100, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                      paper_bgcolor='#1f2630', title_text='Compound Sentiment of Tweets by Date', title_x=0.5,
                      font=dict(family='Helvetica Neue',
                                size=12,
                                color='#7fafdf'), xaxis_title='Date',
                      yaxis_title='Compound Sentiment Score',
                       annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-.2,
                              showarrow=False,
                              text="<br>Source: Twitter",
                              xref="paper",
                              yref="paper",
                              textangle=0
                          )],
                     
                     )

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
    dft = dft.iloc[:, :2]
    dft = dft.rename(columns={' Number of Appearances': 'Frequency'})
    return html.Div(dash_table.DataTable(
        id='Table',

        columns=[{'id': c, 'name': c} for c in dft.columns],
        data=dft.to_dict('records'),
        fixed_rows={'headers': True},
        style_table=dict(overflowX='auto', minWidth='100%'),
        style_cell={'minWidth': '5px', 'width': '8px', 'maxWidth': '10px', 'height': 'auto', 'color': '#7fafdf',
                    'backgroundColor': '#1f2630', 'textAlign': 'center',
                    'fontFamily': 'Helvetica Neue'}
    ))


@app.callback(
    dash.dependencies.Output('bigrams', 'figure'),
    [dash.dependencies.Input('demo-dropdown', 'value'),
     dash.dependencies.Input('number-dropdown', 'value')])
def update_graph(value, number_dropdown):
    df6 = bigrams[bigrams['Country'] == value]
    if number_dropdown == 10:
        fig_3 = px.bar(df6[:10], x='Name', y='weight', title='Counts of top bigrams',
                       labels={'Name': 'Bigram', 'weight': 'Count'})

        fig_3.update_traces(marker_color='#7fafdf')

        fig_3.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue',

                                         color='#7fafdf', size=14))
        fig_3.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue', color='#7fafdf', size=14))

        fig_3.update_layout(margin={'l': 100, 'b': 50, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630', title_text='Top Bigram Occurence', title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-.3,
                              showarrow=False,
                              text="<br>Source: Twitter",
                              xref="paper",
                              yref="paper",
                              textangle=0
                          )],
                           )

    if number_dropdown == 20:
        fig_3 = px.bar(df6[:20], x='Name', y='weight', title='Counts of top bigrams',
                       labels={'Name': 'Bigram', 'weight': 'Count'})

        fig_3.update_traces(marker_color='#7fafdf')

        fig_3.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue',

                                         color='#7fafdf', size=14))
        fig_3.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue', color='#7fafdf', size=14))

        fig_3.update_layout(margin={'l': 100, 'b': 50, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630', title_text='Top Bigram Occurence', title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-.3,
                              showarrow=False,
                              text="<br>Source: Twitter",
                              xref="paper",
                              yref="paper",
                              textangle=0
                          )],
                           )

    if number_dropdown == 30:
        fig_3 = px.bar(df6[:30], x='Name', y='weight', title='Counts of top bigrams',
                       labels={'Name': 'Bigram', 'weight': 'Count'})

        fig_3.update_traces(marker_color='#7fafdf')

        fig_3.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue',

                                         color='#7fafdf', size=14))
        fig_3.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue', color='#7fafdf', size=14))

        fig_3.update_layout(margin={'l': 100, 'b': 50, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630', title_text='Top Bigram Occurence', title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-1,
                              showarrow=False,
                              text="<br>Source: Twitter",
                              xref="paper",
                              yref="paper",
                              textangle=0
                          )],
                           )

    if number_dropdown == 40:
        fig_3 = px.bar(df6[:40], x='Name', y='weight', title='Counts of top bigrams',
                       labels={'Name': 'Bigram', 'weight': 'Count'})

        fig_3.update_traces(marker_color='#7fafdf')

        fig_3.update_xaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue',

                                         color='#7fafdf', size=14))
        fig_3.update_yaxes(showgrid=True, gridcolor='#5b5b5b',
                           tickfont=dict(family='Helvetica Neue', color='#7fafdf', size=14))

        fig_3.update_layout(margin={'l': 100, 'b': 50, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630', title_text='Top Bigram Occurence', title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                           annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-1.2,
                              showarrow=False,
                              text="<br>Source: Twitter",
                              xref="paper",
                              yref="paper",
                              textangle=0
                          )],
                           )

    # fig_3.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
    #    xref='paper', yref='paper', showarrow=False, align='left',
    #  bgcolor='rgba(0, 0,0,0)')

    return fig_3


@app.callback(
    Output('table-container', 'data'),
    [Input('demo-dropdown', 'value')])
def display_table(Country):
    dff_3 = top_hashtag[top_hashtag.Country == Country]
    dff_3 = dff_3.iloc[:, :2]

    return dff_3.to_dict('records')
   
   

@app.callback(Output('nodes_1', 'src'),
                 [Input('demo-dropdown', 'value')])
def change_video(option):
       if option == 'US':
           return 'assets/node_test_2.html'
       if option == 'Nigeria':
           return 'assets/nigeria_node_test.html'
       else:
           return 'https://www.youtube.com/embed/ALZHF5UqnU4'


@app.callback(Output('co-oc', 'src'),
                 [Input('demo-dropdown', 'value')])
def change_video(option):
       if option == 'US':
           return 'assets/yay.html'
       if option == 'Nigeria':
           return 'assets/yay_nigeria.html'
       else:
           return 'https://www.youtube.com/embed/ALZHF5UqnU4'
         
@app.callback(Output('sentiment', 'src'),
                 [Input('demo-dropdown', 'value')])
def change_video(option):
       if option == 'US':
           return 'assets/Us_emotion.html'
       if option == 'Nigeria':
           return 'assets/Nigeria_emotion.html'
       else:
           return 'https://www.youtube.com/embed/ALZHF5UqnU4'



# run app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=False)
