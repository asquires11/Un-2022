
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
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

df_date = pd.read_csv('compound_date.csv')
# df_date = pd.read_csv(
# 'US_COMPOUND_SENTIMENT_AND_DATE.csv')

sentiment_scores = pd.read_csv(
    'sentiment_scores.csv')
bigrams = pd.read_csv('bigrams.csv')
top_hashtag = pd.read_csv('tophashtag_final.csv')



states = top_hashtag.Country.unique().tolist()

# build app
# _________________________________________________


app.layout = html.Div(id='root',
    children=[
        html.Div(id='header',children=[
html.A([(dbc.Button("About",className='button', id="open-backdrop")),




                    ]), dbc.Modal(
                [
                    dbc.ModalHeader("About this project"),
                    dbc.ModalBody(
                        html.Div([
                                  html.H5('Motivation'),
                                  html.P(
                                      'The research objective was to understand how parents,students,teachers,and schools felt about their countries implementation of distance learning, as well as examining the everyday challenges and triumphs of education discussed on social media'
                                      ' during the pandemic. As we gather more country data, we hope to encounter patterns in social media post across borders leading to a better understanding'
                                      'of what makes a succesful distance learning program whether it be distributed by television, online, radio or any other method currently in use.'),
                                  html.Br(),
                                  html.H5('Developer'),
                                  html.P('This project was developed for UNICEF by Annika Squires')

                                  ]),

                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "Close", id="close-backdrop", className="ml-auto"
                        )
                    ),
                ],
                id="modal-backdrop",
                scrollable=True,

            ),
            html.Img(id='logo',src=app.get_asset_url("UNICEF_logo_2016.png")),

html.H4('COVID-19 AND EDUCATION',

                                     style={'color': '#7fafdf'}, className='app-header--title'),
                             html.P(
                                 id="description",

                                 children='This project uses Natural Language Processing (NLP) to study the social media sentiment \
                on education during COVID-19. Our inital focus is on the United States and Nigeria with social media data\
                acquired from Twitter. Click around to explore the results from more than 20,000 social media posts\
                discussing distance learning between March 16,2020 and June 06,2020.'
                                        ,

                             ),

            html.Br(),


        ]),

        html.Br(),

        html.Div(children=[
            dbc.Row(
                [

                    dbc.Col(children=[

                        dbc.Card(
                            dbc.CardBody(className='left-column', children=[
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
                                                                     #{'label': 'China', 'value': 'CHN'},
                                                                     {'label': 'Nigeria', 'value': 'Nigeria'},
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
                            ], style={'backgroundColor': '#252e3f','height': '99rem',

                                      'fontColor': '#7fafdf'},

                            ), style={'backgroundColor': '#252e3f'})

                    ],md=3),

                    dbc.Col(html.Div(className='heatmap-container', children=dbc.Card(
                        dbc.CardBody([



                            dbc.Tabs(className="nav nav-pills", children=[

                                dbc.Tab(tab_id="tab_4", label="Bigrams",
                                        style={'height': '90rem'},
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
                                                          style={'backgroundColor': '#fdfe2','height': '75rem'}),

                                            ], fluid=True),
                                        ],),

                                dbc.Tab(label="Dates",
                                        children=[

                                            html.Br(),
                                            dcc.Graph(id="sentiment-dates",
                                                      style={'height': '88rem'} ),
                                        ],
                                        style={'height': '90rem'}),
                                # dbc.Tab(
                                # dcc.Graph(id='bigrams', style={'backgroundColor': '#fdfe2', 'height': '650px'}),
                                # label='Bigrams'),
                                dbc.Tab(html.Div([
                                    html.Br(),
                                    html.H5('Cocccurence Network'),
                                    html.P('Explore how connected words have appeared in social media post from your country of choice'),

                                    html.Iframe(
                                                    id='nodes_1',
                                                    src=None, width='100%',style={'height': '80rem'}),  # ),



                               ]),  label="Nodes",style={'height': '90rem'}, ),

                                dbc.Tab(html.Div([
                                    html.Br(),

                                    html.H5('Term Based Network Analysis'),
                                    html.P(
                                        'Explore terms that relate to your chosen countries distance learning methods. Click terms (nodes) and zoom in to see word relationships (edges).'),
                                    html.Br(),
                                    html.Iframe(
                                        id='co-oc',
                                        src=None, width='100%',style={'height': '80rem'})]),
                                    label="Network", style={'height': '90rem'}),

                                # dbc.Tab( html.Img(
                                # src=app.get_asset_url('Rplot06.png'),style={'backgroundColor': '#fdfe2', 'height': '650px','width':'1050px'}),style={'backgroundColor': '#fdfe2', 'height': '650px'}, label="Sentiment")
                                dbc.Tab(html.Iframe(
                                    id='sentiment',
                                    src=None, width='100%',style={'height': '90rem'}),
                                    label="Sentiment", style={'height': '90rem'}),

                            ]),


                            html.Br(),
                            html.Div(


                            ),

                        ]), style={'backgroundColor': '#252e3f'}

                    ))),

                ]
            ), html.Div(
                [
                    html.H4('Acknowledgements and Data Sources',
                            style={"margin-top": "0", 'backgroundColor': '#1f2630'}),
                    dcc.Markdown('''\
**Important Data Caveats:**  Due to anonymized data, access to individual tweets is not available. See [FAQ](https://github.com/asquires11/un) for details.
- Special Thanks to Polly Zheng for doing the computing and analysis of the China data
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
                    'backgroundColor': '#1f2630'
                },
                className='twelve columns pretty_container',
            ),
        ],
        style={'backgroundColor': '#1f2630', 'width': '100%', 'height': '900px'}),

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

    fig.update_layout(margin={'l': 100, 'b': 250, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                      paper_bgcolor='#1f2630', title_text='Compound Sentiment of Tweets by Date', title_x=0.5,
                      font=dict(family='Helvetica Neue',
                                size=12,
                                color='#7fafdf'), xaxis_title='Date',
                      yaxis_title='Compound Sentiment Score',
                      annotations=[
                          go.layout.Annotation(
                              x=0,
                              y=-1.2,
                              showarrow=False,
                              text="<br>Data: Twitter",
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
        fig_3.update_layout(margin={'l': 100, 'b':130, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630',
                            title_text='Top Bigram Occurence <br> <sup>Bigrams are 2 consecutive words in a sentence. This'
                                       ' plot represents the most commonly occcuring bigrams from all social media posts <sup>',

                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                                go.layout.Annotation(
                                    x=0,
                                    y=-.3,
                                    showarrow=False,
                                    text="<br> Data: Twitter",
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
        fig_3.update_layout(margin={'l': 100, 'b': 150, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630',
                            title_text='Top Bigram Occurence <br> <sup>Bigrams are 2 consecutive words in a sentence. This'
                                       ' plot represents the most commonly occcuring bigrams from all social media posts <sup>',

                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                                go.layout.Annotation(
                                    x=0,
                                    y=-.3,
                                    showarrow=False,
                                    text="<br>Data: Twitter",
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

        fig_3.update_layout(margin={'l': 100, 'b': 290, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630',
                            title_text='Top Bigram Occurence <br> <sup>Bigrams are 2 consecutive words in a sentence. This'
                                       ' plot represents the most commonly occcuring bigrams from all social media posts <sup>',
                            # title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                                go.layout.Annotation(
                                    x=0,
                                    y=-1,
                                    showarrow=False,
                                    text="<br>Data: Twitter",
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

        fig_3.update_layout(margin={'l': 100, 'b': 330, 'r': 10, 't': 100}, plot_bgcolor='#1f2630',
                            paper_bgcolor='#1f2630',
                            title_text='Top Bigram Occurence <br> <sup>Bigrams are 2 consecutive words in a sentence. This'
                                       ' plot represents the most commonly occcuring bigrams from all social media posts <sup>'

                            ,  # title_x=0.5,
                            font=dict(family='Helvetica Neue',
                                      size=12,
                                      color='#7fafdf'), xaxis_title='Bigram',
                            yaxis_title='Frequency',
                            annotations=[
                                go.layout.Annotation(
                                    x=0,
                                    y=-1.5,
                                    showarrow=False,
                                    text="<br>Data: Twitter",
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


@app.callback(
    Output("modal-backdrop", "backdrop"), [Input("backdrop-selector", "value")]
)
def select_backdrop(backdrop):
    return backdrop


@app.callback(
    Output("modal-backdrop", "is_open"),
    [Input("open-backdrop", "n_clicks"), Input("close-backdrop", "n_clicks")],
    [State("modal-backdrop", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# run app
if __name__ == '__main__':
    app.run_server(host='127.0.0.1', debug=False)
