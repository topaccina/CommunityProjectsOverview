
from dash import Dash, html, dcc, Input, Output, dash_table, ctx, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# import datetime as dt
import plotly.express as px

###############################################################################
# import data
df = pd.read_csv('./data/CFP_Alldata.csv')
df_dload = df[['N', 'ROUND', 'TYPE', 'TITLE',
              'DFIREQ', 'STATUS', 'CATEGORY', 'REQUESTER', 'GITHUB', 'REDDIT', 'WEBSITE', 'TWITTER']]
###############################################################################
# data prep
###############################################################################
# card section data
totalRound = len(df['ROUND'].unique())
lastRoundDate = pd.to_datetime(df['DATE'].astype('datetime64[ns]')).dt.strftime(
    '%Y-%m').sort_values(ascending=False)[0]
totalDFIRequested = df[(df.TYPE == 'cfp')]['DFIREQ'].sum()
totalDFIAssigned = df[(df.RESULT == 'Approved') &
                      (df.TYPE == 'cfp')]['DFIREQ'].sum()
totalDFIAssignedPct = round(100*totalDFIAssigned/totalDFIRequested, 1)
totalCFP = df.TYPE.value_counts().loc['cfp']
totalCFPApproved = df[(df.RESULT == 'Approved') &
                      (df.TYPE == 'cfp')].shape[0]
totalCFPApprovedPct = round(100*totalCFPApproved/totalCFP, 1)
totalDFIP = df.TYPE.value_counts().loc['dfip']
totalDFIPApproved = df[(df.RESULT == 'Approved')
                       & (df.TYPE == 'dfip')].shape[0]
totalDFIPApprovedPct = round(100*totalDFIPApproved/totalDFIP, 1)
############################################################################
# category plots data
df_cfp_cat = df[(df.RESULT == 'Approved') & (
    df.TYPE == 'cfp')]['CATEGORY'].value_counts().reset_index()
df_cfp_cat.columns = ['category', 'count']
#############################################################################
# dfi assegned/year data
df_dfi_yyyy = df[(df.RESULT == 'Approved')].groupby(df.DATE.astype(
    'datetime64[ns]').dt.strftime('%Y'))['DFIREQ'].sum().reset_index()
############################################################################
# dfi assegned/year/round data ---->NOT USED!!!!!!!
df_dfi_yyyy_round = df[(df.RESULT == 'Approved')].groupby([df.DATE.astype(
    'datetime64[ns]').dt.strftime('%Y'), 'ROUND'])['DFIREQ'].sum().reset_index()
#############################################################################
# dfi per cfp data
df_dfi_cfp = df[(df.RESULT == 'Approved') & (
    df.TYPE == 'cfp')][['N', 'DFIREQ', 'TITLE']]
df_dfi_cfp_sorted = df_dfi_cfp.sort_values(by='DFIREQ', ascending=False)
##############################################################################
# masternode statistics per round
df_masternodes_round = df.groupby(
    df.DATE.astype(
        'datetime64[ns]').dt.strftime('%Y-%m'))['MASTERNODESCOUNT'].unique().apply(lambda x: x[0]).reset_index()
##############################################################################
# plots
# CFP by category pie chart
labels = df_cfp_cat['category'].values
values = df_cfp_cat['count'].values
fig_2_1 = go.Figure(go.Pie(labels=labels, values=values,
                    name="CFPs", insidetextorientation='radial'))
fig_2_1.update_traces(hole=.4, hoverinfo="label+percent+value+name", textinfo="percent", marker=dict(
    colors=px.colors.qualitative.Dark24))
fig_2_1.update_layout(
    title={'text': "CFPs Overview by Category"},
    uirevision=True, font={'color': 'rgb(200, 200, 200)'},
    showlegend=True,
    paper_bgcolor='#1f2c56',
    plot_bgcolor='#1f2c56',
    autosize=True,
)
# plots
# DFI assigned/Year pie chart
labels = df_dfi_yyyy['DATE'].unique()
values = df_dfi_yyyy['DFIREQ'].unique()
fig_3_1 = go.Figure(
    go.Pie(labels=labels, values=values, name="DFIAssingnedYear"))
fig_3_1.update_traces(hoverinfo="label+percent+value+name", textinfo="percent+label", marker=dict(
    colors=px.colors.qualitative.Light24))
fig_3_1.update_layout(
    title={'text': "DFI Assigned per Year"},
    uirevision=True, font={'color': 'rgb(200, 200, 200)'},
    showlegend=True,
    paper_bgcolor='#1f2c56',
    plot_bgcolor='#1f2c56',
    autosize=True,
)

fig_2_3 = go.Figure()
fig_3_2 = go.Figure(go.Scatter(x=df_masternodes_round.DATE, y=df_masternodes_round.MASTERNODESCOUNT, mode="markers+lines",
                               name="Assigned DFI - cumulative sum",
                               line=dict(width=6, color='#FF00FF'),
                               hoverinfo='text', fill='tozeroy', marker=dict(size=12),
                               hovertext=df_masternodes_round['DATE'].astype(str)+'-masternodes ' +
                               df_masternodes_round['MASTERNODESCOUNT'].astype(
                                   str),
                               ))
fig_3_2.update_traces(fillcolor='rgba(255, 0, 255, 0.1)')
fig_3_2.update_layout(title={'text': 'Masternode with Voting Rights',
                             },
                      titlefont={'color': 'white',
                                 'size': 20},
                      font=dict(family='sans-serif',
                      color='white',
                      size=12),
                      hovermode='closest',
                      paper_bgcolor='#1f2c56',
                      plot_bgcolor='#1f2c56',

                      margin=dict(r=20),
                      xaxis=dict(title='<b>Date</b>',
                                 color='white',
                                 showline=True,
                                 showgrid=True,
                                 showticklabels=True,
                                 linecolor='rgb(200, 200, 200)',
                                 linewidth=1,
                                 ticks='outside',
                                 tickfont=dict(
                                       family='sans-serif',
                                     color='rgb(200, 200, 200)',
                                     size=12
                                 )),
                      yaxis=dict(title='<b>Masternodes DFI</b>',
                                 color='white',
                                 showline=True,
                                 showgrid=True,
                                 showticklabels=True,
                                 linecolor='rgb(200, 200, 200)',
                                 linewidth=1,
                                 ticks='outside',
                                 tickfont=dict(
                                       family='sans-serif',
                                     color='rgb(200, 200, 200)',
                                     size=12
                                 )
                                 )

                      )


def generate_modal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",

                        children=(
                            html.Div([
                                html.H6(['Title'], id='title-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(['Result'], id='result-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(['DFI Requested'], id='DFI-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(['Requester'], id='requester-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(['Category'], id='cat-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(['Status'], id='status-id', style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(["Go to ", html.A('GitHub', href='', target='_blank', id="git-id", style={
                                    'textAlign': 'left', 'padding': 10})], style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(["Go to ", html.A('Reddit', href='', target='_blank', id="reddit-id", style={
                                    'textAlign': 'left', 'padding': 10})], style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(["Go to ", html.A('Twitter', href='', target='_blank', id="twitter-id", style={
                                    'textAlign': 'left', 'padding': 10})], style={
                                    'textAlign': 'left', 'padding': 10}),
                                html.H6(["Go to ", html.A('Project Web Page', href='', target='_blank', id="web-id", style={
                                    'textAlign': 'left', 'padding': 10})], style={
                                    'textAlign': 'left', 'padding': 10}),

                            ], className='')
                        ),
                    ),
                ],
            )
        ),
    )


# author/collaborators card
# contactsCard = dbc.Card([
#     dbc.Row([
#         dbc.Col([dbc.CardImg(src='assets/me.png', top=True,
#                 style={'max-width': '50%', 'max-height': '50%'}), ]),
#         dbc.Col(dbc.CardBody(
#             [html.H3([html.A(html.I(className="bi bi-linkedin "), href='https://www.linkedin.com/in/laura-lorenzi-14885a12/', target='__blank__'), " Laura L.", ], className="text-nowrap", style={'margin-bottom': '0px',   'font-size': 20,  'line-height': '0.5'}),
#              html.H6([" Maintaner and Developer"],
#                      style={'margin-bottom': '0px',  'font-size': 15, 'text-transform': 'uppercase'}), html.Hr(style={'margin': '20px'}),
#              html.Div([html.A(html.I(className="bi bi-envelope mx-2"), href='mailto:myemailaddress@gmail.com', target='__blank__'),
#                        html.A(html.I(className="bi bi-twitter"), href='mailto:myemailaddress@gmail.com', target='__blank__')], style={'margin': '0px 40px',   'font-size': 30,  'line-height': '0.5',  'display': 'flex', 'justify-content': 'space-evenly'}),

#              ],))])], className="my-5",)
contactsCard = html.Div([html.Div([html.Img(src='assets/cfpOv_ico.jpg',
                                            id='logo-us-image',
                                            style={'height': 'auto',
                                                   'width': '100%',
                                                   })], style={'margin-bottom': '0px'}),
                         html.Div([html.H6([html.A(html.I(className="bi bi-envelope "), href='mailto:defichainproposal@gmail.com', target='__blank__'), html.A(html.I(className="bi bi-twitter "), href='https://twitter.com/DefiProposal', target='__blank__')],  style={'margin-bottom': '0px', 'font-size': 40, 'display': 'flex', 'justify-content': 'space-evenly'}),
                                   html.Hr(
                                       style={'margin-top': '0px', 'margin-bottom': '10px'}),
                                   html.H6([html.A(html.I(className="bi bi-linkedin "), href='https://www.linkedin.com/in/laura-lorenzi-14885a12/', target='__blank__'), " Laura L."],
                                           style={'margin-bottom': '0px',  'font-size': 20}),
                                   html.H6(["Maintaner and Developer"],
                                           style={'margin-bottom': '0px',  'font-size': 15})], ),
                         ], className='contacts-container-flex')


app = Dash(__name__, suppress_callback_exceptions=True, meta_tags=[
    {"name": "viewport", "content": "width=device-width"}], external_stylesheets=[dbc.icons.BOOTSTRAP])
#server = app.server

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                html.H3('CFP and DFIP Overview ',
                        style={'margin-bottom': '0px',   'font-size': 20,  'line-height': '0.5'}),
                html.H6('Statistics and Projects Reporting',
                        style={'margin-bottom': '0px',  'font-size': 15}), ],),
        ], style={'justify-content': 'flex-start', 'flex-basis': '90%'}, id='title', ),
        html.Div([
            html.A(
                html.Img(src=app.get_asset_url('DEFICHAIN LOGO FULL COLOUR WHITE.png'),
                         id='logo-image',
                         style={'height': '40px',
                                'width': 'auto',
                                'margin': '0px'}),  href="https://defichain.com/", target='_blank',
                style={"textDecoration": "none"},
            ),
        ], style={'justify-content': 'flex-end', 'flex-basis': '10%'},),
    ], id='header', className='row flex-display',  style={'align-items': 'end'}),

    html.Div([html.Hr()], style={'margin': '-20px', 'line-height': '0'}),

    dcc.Tabs([
        dcc.Tab(label='Overall Statistics', value='tab1', id='tab1', className='custom-tab', selected_className='custom-tab--selected', children=[
                html.Div([
                    html.Div([html.H6(children='Total Rounds',
                                      className='card-header'),
                              html.P(f"{totalRound}",
                                     className='card-body', style={'color': 'green'}),
                              html.P('last Round: ' + f"{lastRoundDate}",
                                     className='card-footer', style={'color': '#77ff99'})], className='card-container-flex'),
                    html.Div([html.H6(children='Total DFI assigned',
                                      className='card-header'),
                              html.P(f"{totalDFIAssigned:,.0f}",
                                     className='card-body', style={'color': 'red'}),
                              html.P(f"{totalDFIAssignedPct}% total requested",
                                     className='card-footer', style={'color': '#ff5555'})], className='card-container-flex'),
                    html.Div([html.H6(children='Total CFPs Approved',
                                      className='card-header'),
                              html.P(f"{totalCFPApproved}",
                                     className='card-body', style={'color': 'orange'}),
                              html.P(f"{totalCFPApprovedPct}% total proposed",
                                     className='card-footer', style={'color': '#ffff55'})], className='card-container-flex'),
                    html.Div([html.H6(children='Total DFIPs Approved',
                                      className='card-header'),
                              html.P(f"{totalDFIPApproved}",
                                     className='card-body', style={'color': 'aqua'}),
                              html.P(f"{totalDFIPApprovedPct}% total proposed",
                                     className='card-footer', style={'color': '#99ddff'})], className='card-container-flex'),
                ], className='row flex-display', style={'justify-content': 'space-between'}),

                html.Div([

                    html.Div([
                        dcc.Graph(id='pie_category',
                                  config={'displayModeBar': 'hover'}, figure=fig_2_1, className='pie-plot')], className='create_container'),

                    html.Div([
                        html.Div(
                            dcc.Graph(id='line_chart-DFIAssigned', config={
                                'displayModeBar': 'hover'}, figure=fig_2_3, className='line-scatter-plot')),
                        html.Div(
                            dcc.RadioItems(['Top-10', 'All'], 'Top-10', inline=True, id='radio-cfp-dfi', className='radio-cfp-dfi')),
                    ], className='create_container'),

                ], className='row flex-display', style={'justify-content': 'space-between', }),
                html.Div([
                    html.Div([
                        dcc.Graph(id='pie_DFIAssigned_year', config={
                            'displayModeBar': 'hover'}, figure=fig_3_1, className='pie-plot')
                    ], className='create_container'),
                    html.Div([
                        dcc.Graph(id='line_chart-Masternodes',
                                  config={'displayModeBar': 'hover'}, figure=fig_3_2, className='line-plot')
                    ], className='create_container'),
                ], className='row flex-display', style={'justify-content': 'space-between'}),

                ]),
        dcc.Tab(label='Proposals Details', value='tab2', id='tab2', className='custom-tab',
                selected_className="custom-tab--selected", children=[
                    html.Div([
                        html.Div([
                            html.H6(id='filter-title', className='filter-title', children=[
                                    'Filter Panel', html.Span(id='filter-panel-label', className='table-label', children=[
                                        ' (Fitering Options to refine the research)'], style={'display': 'inline', 'font-size': '14px', 'text-transform': 'none', 'font-weight': '200'}), ]), ], className='filter-header'),
                        html.Div([
                            html.Div([
                                html.Label(
                                    ['Round'], className='filter-label'),
                                dcc.Dropdown(id='dropdown-round',
                                             options=df['ROUND'].unique(),
                                             # value=df['ROUND'].unique()[0],
                                             placeholder='select a value',
                                             multi=False,
                                             clearable=True,
                                             className='filter-dropdown',
                                             ),
                            ], className='drop-container'),
                            html.Div([
                                html.Label(
                                    ['Category'], className='filter-label'),
                                dcc.Dropdown(id='dropdown-category',
                                             options=df['CATEGORY'].unique(),
                                             # value=df['CATEGORY'].unique()[0],
                                             placeholder='select a value',
                                             multi=False,
                                             clearable=True,
                                             className='filter-dropdown',
                                             ),
                            ], className='drop-container'),
                            html.Div([
                                html.Label(['Type'], className='filter-label'),
                                dcc.Dropdown(id='dropdown-type',
                                             options=df['TYPE'].unique(),
                                             # value=df['TYPE'].unique()[0],
                                             placeholder='select a value',
                                             multi=False,
                                             clearable=True,
                                             className='filter-dropdown',
                                             ),
                            ], className='drop-container'),
                            html.Div([
                                html.Label(
                                    ['Result'], className='filter-label'),
                                dcc.Dropdown(id='dropdown-result',
                                             options=df.RESULT.unique(),
                                             # value=df.RESULT.unique()[0],
                                             multi=False,
                                             clearable=True,
                                             className='filter-dropdown',
                                             ),
                            ], className='drop-container'),
                            html.Div([
                                html.Label(['Requester'],
                                           className='filter-label'),
                                dcc.Dropdown(id='dropdown-requester',
                                             options=df.REQUESTER.unique(),
                                             # value=df.REQUESTER.unique()[0],
                                             placeholder='select a value',
                                             multi=False,
                                             clearable=True,
                                             className='filter-dropdown',
                                             optionHeight=80
                                             ),
                            ], className='drop-container'),
                            # tblClearFilter-button
                            html.Div([html.Label(['Clear Filter'],
                                                 className='filter-label'), html.Button(children=['Click'], id='button-clearFilter', n_clicks=0, className='button-details')],
                                     className='button-container'),
                            html.Div([html.Label(['Download'],
                                                 className='filter-label'), html.Button(children=['Click'], id='button-download', n_clicks=0, className='button-details'), dcc.Download(id="download-dataframe-csv")],
                                     className='button-container')

                        ], className='filter-container'),
                        html.Div([
                            html.H6(id='table-title', className='table-title', children=[
                                       'Proposals Information', html.Span(id='table-label', className='table-label', children=[
                                           ' (Select a project for more details)'], style={'display': 'inline', 'font-size': '14px', 'text-transform': 'none', 'font-weight': '200'}), ]),
                            html.Br(),

                            #     html.Button(
                            #     id="button-selection-details", children="Selection Details", n_clicks=0, className='button-details'
                            # ),
                            # html.Div([html.Label(['Download Data'],
                            #                      className='filter-label'), html.Button(children=['Click'], id='button-download', n_clicks=0, className='button-details'), dcc.Download(id="download-dataframe-csv")],
                            #          className='drop-container'),

                            generate_modal(),
                            dbc.Container([
                                dash_table.DataTable(
                                    id='table-cfp-dfip',
                                    data=df.to_dict(
                                        'records'),
                                    columns=[{'id': d, 'name': c}
                                             # for c in df.loc[:, ['title', 'DFIREQ', 'CATEGORY', 'REQUESTER', 'STATUS']]
                                             for c, d in zip(['Title', 'Result', 'DFI Amount', 'Category', 'Requester', 'Status'], df.loc[:, [
                                                 'TITLE', 'RESULT', 'DFIREQ', 'CATEGORY', 'REQUESTER', 'STATUS']])
                                             # for c in df.columns
                                             ],
                                    #  sort_action="native",
                                 fixed_rows={
                                        'headers': True},



                                 style_data={
                                        'color': 'black',
                                        'backgroundColor': '#1f2c56',
                                        'border': 'rgb(200, 200, 200) solid 1px',
                                        'font-size': '11px',
                                        # 'whiteSpace': 'normal',

                                    },
                                    style_cell={
                                        'overflow': 'hidden',
                                        'textOverflow': 'ellipsis',
                                        'minWidth': '20px', 'width': '80px', 'maxWidth': '80px',
                                        'textAlign': 'left',
                                    },
                                    style_header={
                                        'color': 'black',
                                        'backgroundColor': '#192244',
                                        'border': 'rgb(200, 200, 200) solid 1px',
                                        'font-size': '13px',
                                        'text-transform': 'uppercase',
                                        'font-weight': 'bold',
                                    },
                                    style_cell_conditional=[
                                        {'if': {'column_id': ['title']},
                                         'maxWidth': '200px'},
                                        {'if': {'column_id': ['RESULT', 'DFIREQ']},
                                         'maxWidth': '50px'},

                                    ],
                                    style_data_conditional=[
                                        {
                                            "if": {"state": "active" or 'selected'},
                                            "backgroundColor": '#192244',
                                            "border": "1px solid rgb(255,000,255)",
                                            "color": "rgb(0,0,255)",
                                        },
                                    ],
                                    tooltip_data=[
                                        {
                                            column: {'value': str(
                                                value), 'type': 'markdown'}
                                            for column, value in row.items()
                                        } for row in df.to_dict('records')
                                    ],
                                    # tooltip_duration=None,
                                    style_table={'overflowX': 'auto',
                                                 'overflowY': 'auto',
                                                 'height': '700px',
                                                 'width': '100%'
                                                 },

                                    # left align text in columns for readability

                                 ), ], style={'margin': 'auto 0px auto 0px'}),
                        ], className='table-container')


                    ], className='flex-display container-tab2 '),  # end container tab2 content
                ]),  # end tab2
        dcc.Tab(label='Contacts', value='tab3', id='tab3', className='custom-tab',
                selected_className="custom-tab--selected", children=[

                    html.Div([contactsCard])
                ]),
    ], className='custom-tabs', value='tab1'),

], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


#####################################################################################
# callback section
@ app.callback(
    Output('line_chart-DFIAssigned', 'figure'),
    Input('radio-cfp-dfi', 'value')
)
def CFP_DFI_bar(radio_sel):
    if radio_sel == 'All':
        x = df_dfi_cfp_sorted['N'].astype(str)
        y = df_dfi_cfp_sorted['DFIREQ']
        z = df_dfi_cfp_sorted['TITLE']
    else:
        x = df_dfi_cfp_sorted['N'].astype(str)[0: 10]
        y = df_dfi_cfp_sorted['DFIREQ'][0: 10]
        z = df_dfi_cfp_sorted['TITLE'][0: 10]

    fig_2_3 = go.Figure(go.Bar(x=x, y=y,
                               name='Assigned DFI by CFP',
                               marker=dict(color='orange'),
                               hoverinfo='text',
                               hovertext=''+z  # +' assigned '  +
                               # y.map(
                               #    '{:,.0f}'.format).astype(str)+' DFI',
                               )

                        )
    fig_2_3.update_traces(marker_color=px.colors.sequential.Turbo_r)

    fig_2_3.update_layout(title={'text': 'Assigned DFI by CFP',
                                 },
                          titlefont={'color': 'rgb(200, 200, 200)',
                                     'size': 20},
                          font=dict(family='sans-serif',
                                    color='rgb(200, 200, 200)',
                                    size=12),
                          hovermode='closest',
                          paper_bgcolor='#1f2c56',
                          plot_bgcolor='#1f2c56',
                          legend={'orientation': 'h',
                                  'bgcolor': '#1f2c56',
                                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
                          margin=dict(r=20),
                          xaxis=dict(title='<b>CFP Id</b>',
                                     color='white',
                                     showline=True,
                                     showgrid=False,
                                     showticklabels=True,
                                     linecolor='rgb(200, 200, 200)',
                                     linewidth=1,
                                     ticks='outside',
                                     tickfont=dict(
                                           family='sans-serif',
                                           color='rgb(200, 200, 200)',
                                           size=12
                                     )),
                          yaxis=dict(title='<b>Assigned DFI</b>',
                                     color='white',
                                     showline=True,
                                     showgrid=True,
                                     showticklabels=True,
                                     linecolor='rgb(200, 200, 200)',
                                     linewidth=1,
                                     ticks='outside',
                                     tickfont=dict(
                                           family='sans-serif',
                                           color='rgb(200, 200, 200)',
                                           size=12
                                     )
                                     )

                          )
    return fig_2_3


@ app.callback(
    Output('table-cfp-dfip', 'data'),
    Output('table-cfp-dfip', 'tooltip_data'),
    Input('dropdown-round', 'value'),
    Input('dropdown-category', 'value'),
    Input('dropdown-type', 'value'),
    Input('dropdown-result', 'value'),
    Input('dropdown-requester', 'value')
)
def update_dropdown_options(round_v, category_v, type_v, result_v, requester_v):
    dff = df.copy()

    if round_v is not None:
        dff = dff[dff['ROUND'] == round_v]
    if category_v is not None:
        dff = dff[dff['CATEGORY'] == category_v]
    if type_v is not None:
        dff = dff[dff['TYPE'] == type_v]
    if result_v is not None:
        dff = dff[dff['RESULT'] == result_v]
    if requester_v is not None:
        dff = dff[dff['REQUESTER'] == requester_v]

    if dff.shape[0] == 0:
        return no_update
    else:
        return dff.to_dict('records'), [
            {column: {'value': str(value), 'type': 'markdown'}
             for column, value in row.items()
             } for row in dff.to_dict('records')
        ]


@ app.callback(
    [Output('dropdown-round', 'value'),
     Output('dropdown-category', 'value'),
     Output('dropdown-type', 'value'),
     Output('dropdown-result', 'value'),
     Output('dropdown-requester', 'value')],
    Input("button-clearFilter", "n_clicks"),

)
def clear_tbl_filter(n1):
    return None, None, None, None, None


@ app.callback(
    Output("markdown", "style"),
    [
        # Input("button-selection-details", "n_clicks"),
        Input('table-cfp-dfip', 'active_cell'),
        Input("markdown_close", "n_clicks")],
)
# def update_click_output(button_click, active_cell, close_click):
def update_click_output(active_cell, close_click):
    # ctx = callback_context

    if ctx.triggered:
        prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
        # print(prop_id)
        # if prop_id == "button-selection-details":
        #     return {"display": "block"}
        if prop_id == "table-cfp-dfip":
            return {"display": "block"}

    return {"display": "none"}


@ app.callback(

    [Output('title-id', 'children'),
     Output('result-id', 'children'),
     Output('DFI-id', 'children'),
     Output('requester-id', 'children'),
     Output('cat-id', 'children'),
     Output('status-id', 'children'),
     Output('git-id', 'href'),
     Output('reddit-id', 'href'),
     Output('twitter-id', 'href'),
     Output('web-id', 'href'), ],
    [Input('table-cfp-dfip', 'active_cell'),
     Input('table-cfp-dfip', 'data')]
)
def testTbl(active_cell, tblData):
    df = pd.DataFrame(tblData)
    if active_cell is None:
        return no_update
    selRows = active_cell["row"]
    # print(f"row id: {selRows}")
    # print(df.loc[selRows]['title'])
    if selRows is not None:
        title = df.loc[selRows]['TITLE']
        dfiAmount = df.loc[selRows]['DFIREQ']
        result = df.loc[selRows]['RESULT']
        requester = df.loc[selRows]['REQUESTER']
        category = df.loc[selRows]['CATEGORY']
        status = df.loc[selRows]['STATUS']
        git = df.loc[selRows]['GITHUB']
        reddit = df.loc[selRows]['REDDIT']
        twitter = df.loc[selRows]['TWITTER']
        web = df.loc[selRows]['WEBSITE']
        title = f"Title: {title}"
        result = f"Round Result: {result}"
        requestedDFI = f"$DFI requested:{dfiAmount}"
        req = f"Requester: {requester}"
        cat = f"category: {category}"
        stat = f"status: {status}"
        git = f"{git}"
        reddit = f"{reddit}"
        twitter = f"{twitter}"
        web = f"{web}"
        return title, result, requestedDFI, req, cat, stat, git, reddit, twitter, web
    else:
        return 'Select a row for more details', '', '', '', '', '', '', '', '', ''


@ app.callback(
    Output("download-dataframe-csv", "data"),
    Input("button-download", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    return dcc.send_data_frame(df_dload.to_csv, "mydf.csv")


if __name__ == '__main__':
    app.run_server(debug=True)
