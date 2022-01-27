import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from whitenoise import WhiteNoise
import dash_auth
import dash_daq as daq

# Pulling in all the cleansed data
df = pd.read_excel('lab_results_cleaned.xlsx')
by_month1 = pd.to_datetime(df['create_timestamp']).dt.to_period('M').value_counts().sort_index()
by_month1.index = pd.PeriodIndex(by_month1.index)
df_month1 = by_month1.rename_axis('month').reset_index(name='counts')
value_categories = df['Value Categories'].unique().tolist()

df1 = pd.read_excel('SickCalls.xlsx')
by_month = pd.to_datetime(df1['SickCallCompletedAt']).dt.to_period('M').value_counts().sort_index()
by_month.index = pd.PeriodIndex(by_month.index)
df_month = by_month.rename_axis('month').reset_index(name='counts')

df2 = pd.read_excel('BookinToIntakeAssessment.xlsx')

df3 = pd.read_excel('calvert_cleaned.xlsx')
df3['Assigned To'] = df3['Assigned To'].fillna('Unknown')
value_categories1 = df3['Assigned To'].unique().tolist()
value_categories2 = df3['Gender'].unique().tolist()

df4 = pd.read_excel('cc_records.xlsx')

df5 = pd.read_excel('tests.xlsx')

df6 = pd.read_excel('a1c_linechart.xlsx')

df7 = pd.read_excel('hep_c_results.xlsx')

df8 = pd.read_excel('PT_results.xlsx')

df9 = pd.read_excel('HIV_results.xlsx')

df10 = pd.read_excel('inr_cleaned.xlsx')

df11 = pd.read_excel('NIJ_cleaned.xlsx')

df12 = pd.read_excel('encounters_cleaned.xlsx')

df13 = pd.read_excel('encounters_cleaned1.xlsx')

df14 = pd.read_excel('encounters_cleaned2.xlsx')

# Defining all the figures used in the app layout
fig = px.pie(df, names='Value Categories', title='A1C Values', hole=.5)

fig1 = px.pie(df1, names='Range Interval', title='Sick Call Range')

fig2 = px.sunburst(df2, path=["Within24Hrs"], title='Booked to Intake Assessment')

fig3 = px.histogram(df3, x="Assigned To", color="Recid", title="Recidivism by Provider")

fig4 = px.pie(df3, names="Recid", title="Recidivism True or False")

fig5 = px.histogram(df3, x="Assigned To", color="Reentry Service Status", title='Reentry Service Status by Provider')

fig7 = px.histogram(df3, x="Most Recent Charge Description", title='Charge Counts')
fig7.update_xaxes(title_text='')

fig8 = px.histogram(df3, x='Origin', title="Origin")

fig9 = px.pie(df3, names='Assigned To', title='Reentry Caseloads')
fig9.update_layout(clickmode='event+select')

fig10 = px.pie(df3, names='Number of Bookings', title='Number of Bookings')

fig11 = px.pie(df3, names='Age Categories', title='Age Categories')

fig12 = px.sunburst(df3, path=["Gender"], title='Gender')

fig13 = px.pie(df3, names='Race', title='Race')

fig14 = go.Figure(data=go.Scatter(x=df_month['month'].astype(dtype=str), y=df_month['counts'], text="counts"))
fig14.update_layout({"title": 'Sick Calls Completed by Month', "xaxis": {"title": "Months"},
                     "yaxis": {"title": "Total"}, "showlegend": False})
fig14.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig15 = go.Figure(data=go.Scatter(x=df_month1['month'].astype(dtype=str), y=df_month1['counts'], text="counts"))
fig15.update_layout({"title": 'A1C Labs Completed by Month', "xaxis": {"title": "Months"},
                     "yaxis": {"title": "Total"}, "showlegend": False})
fig15.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig16 = px.pie(df4, names='service_item_desc', title='Chronic Care Clinic Visits')

fig17 = px.line(df5, x='Date', y='Count', color='Chronic Care Visit Type', markers=True,
                title='Chronic Care Clinic Visit Type')
fig17.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig18 = px.bar(df6, x='Date', y='Count', color='Value Categories', barmode='group',
               title='A1C Result Ranges Time Series')
fig18.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig19 = px.pie(df7, names='Result', title="Hep C Results")

fig20 = px.pie(df8, names='Result', title="Prothrombin Time Test")

fig21 = px.pie(df9, names='Result', title='HIV Results')

fig22 = px.pie(df10, names='Results', title='International Normalized Ratio Results')

fig23 = px.histogram(df11, x='Recidivism_Within_3years', title='Recidivism within 3 years')

fig24 = px.pie(df11, names='Race', title='Race', hole=.5)

fig25 = px.histogram(df11, x="Prison_Offense", color="Education_Level", title='Education Level vs. Prison Offense')

fig26 = px.histogram(df11, y='Supervision_Risk_Score_First', color='Recidivism_Within_3years', barmode='group',
                     title='Supervision Risk Score vs. Recidivate within 3 Years')
fig26.update_yaxes(tickmode='linear')

fig27 = px.histogram(df11, x='Prison_Years', color='Recidivism_Within_3years', barmode='group', category_orders={
    "Prison_Years": ['Less than 1 year', '1-2 years', 'Greater than 2 to 3 years', 'More than 3 years']},
                     title='Prison Sentence vs. Recidivate within 3 Years')

fig28 = px.histogram(df11, x='Age_at_Release', color='Recidivism_Within_3years', barmode='group', category_orders={
    "Age_at_Release": ['18-22', '23-27', '28-32', '33-37', '38-42', '43-47', '48 or older']},
                     title='Age at Release vs. Recidivate within 3 Years')

fig29 = px.histogram(df11, x='Prison_Offense', color='Recidivism_Within_3years', barmode='group',
                     title='Prison Offense vs. Recidivate within 3 Years')

fig30 = px.histogram(df11, x='Condition_MH_SA', color='Recidivism_Within_3years', barmode='group',
                     title='Mental Health/Substance Abuse vs. Recidivate within 3 Years')

fig31 = px.histogram(df11, x='Percent_Days_Employed', color='Recidivism_Within_3years', barmode='group',
                     title='Percent of Days Employed vs. Recidivate within 3 Years')

fig32 = px.histogram(df11, x='Jobs_Per_Year', color='Recidivism_Within_3years', barmode='stack',
                     title='Number of Jobs per Year vs. Recidivate within 3 Years')
fig32.update_layout(xaxis_range=[.25, 4])
fig32.update_layout(yaxis_range=[1, 2500])

fig33 = px.line(df12, x='Date', y='Count', color='Venue', markers=True,
                title='Encounter Visit Type')
fig33.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig34 = px.histogram(df13, x='Assigned To', y='Count', color='Venue', title='Encounters by Provider')

fig35 = px.histogram(df14, x='Assigned To', y='Count', title='Declined Services by Provider',
                     color_discrete_sequence=['indianred'])

fig36 = go.Figure(go.Indicator(
    domain={'x': [0, 1], 'y': [0, 1]},
    value=27,
    mode="gauge+number+delta",
    title={'text': "A1C Labs Completed"},
    delta={'reference': 220},
    gauge={'axis': {'range': [None, 250]},
           'steps': [
               {'range': [0, 175], 'color': "rgb(203,213,232)"},
               {'range': [175, 250], 'color': "gray"}],
           'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 220}}))
fig36.update_layout(title='Current Month')

# Initializing the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

auth = dash_auth.BasicAuth(
    app,
    {'~': '~'}
)

modal = html.Div([
    dbc.Button("Open A1C Data Table", id="open", n_clicks=0, className="d-grid gap-2 col-2 mx-auto"),
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("A1C Values")),
        dcc.Dropdown(
            id='filter_dropdown',
            options=[{"label": i, 'value': i} for i in value_categories],
            value=value_categories[0], ),
        html.Br(),
        dcc.ConfirmDialogProvider(
            children=html.Button('Transfer to?'), id='button',
            message='This could be used to send the analysis that was completed to a workflow that could '
                    'trigger other individuals to take action on the analysis that was conducted.'),
        dbc.ModalBody(
            dash_table.DataTable(
                id='table9',
                columns=[{"name": i, "id": i} for i in df.columns],
                page_size=10,
                data=df.to_dict('records'),
                filter_action='native',
                sort_action='native',
                sort_mode='multi',
                row_selectable='multi',
                page_action='native',
                export_format='xlsx',
            )),
        dbc.ModalFooter(
            dbc.Button(
                "Close", id="close", className="ms-auto", n_clicks=0
            )
        ),
    ],
        id="modal",
        is_open=False,
        size="xl",
    ),
])

cards = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="757",
                        id='led-4',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Client Registrations", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="1483",
                        id='led-5',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Case Encounters", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="23",
                        id='led-6',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Declined", className="card-title"),
                ])
        ),
    ]
)

cards1 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="31",
                        id='led-1',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Encounters This Month", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="31",
                        id='led-2',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Encounters Last Month", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="0",
                        id='led-3',
                        size=64,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Percent Difference", className="card-title"),
                ])
        ),
    ]
)

cards2 = dbc.CardGroup(
    [
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="3820",
                        id='led-7',
                        size=35,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Total Patients", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="1080",
                        id='led-8',
                        size=35,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Diabetic Patients", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="152",
                        id='led-9',
                        size=35,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Newly Diagnosed", className="card-title"),
                ])
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    daq.LEDDisplay(
                        value="83.5",
                        id='led-10',
                        size=35,
                        color='#4FA1F3',
                        style={'display': 'inline-block', 'align': 'center'}),
                    html.H2("Non-Compliance Rate %", className="card-title"),
                ])
        ),
    ]
)
# Beginning of app layout
app.layout = html.Div([
    html.Br(),
    html.A(
        href="https://oafoundationweb.odoo.com/", target="_blank",
        children=[
            html.Img(src='logo.png', style={'textAlign': 'center', 'height': '20%', 'width': '20%'}),
        ]),
    html.H1("Analytics Dashboards", style={'text-align': 'center', 'color': '#4FA1F3'}),
    dcc.Tabs([
        dcc.Tab(label='A1C Dashboard',
                children=[
                    html.Br(),
                    html.Div(
                        modal),
                    html.Br(),
                    html.Div(
                        cards2),
                    dcc.Graph(
                        id='fig36',
                        config={'editable': True},
                        figure=fig36,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='basic-interactions',
                        config={'editable': True},
                        figure=fig,
                        style={'display': 'inline-block'}),
                    html.Br(),
                    dcc.Graph(
                        id='basic-interactions15',
                        config={'editable': True},
                        figure=fig18),
                    dcc.Graph(
                        id='basic-interactions18',
                        config={'editable': True},
                        figure=fig15),
                    html.Br(),

                ]),
        dcc.Tab(label='Other Lab Results',
                children=[
                    html.Br(),
                    dcc.Dropdown(
                        id='filter_dropdown3',
                        options=[{"label": 'Hepatitis C', 'value': 'fig19'},
                                 {'label': 'PT', 'value': 'fig20'},
                                 {'label': 'HIV', 'value': 'fig21'},
                                 {'label': 'INR', 'value': 'fig22'}],
                        value='Hepatitis C'),
                    dcc.Graph(
                        id='basic-interactions19',
                        config={'editable': True},
                        figure=fig19,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='basic-interactions20',
                        config={'editable': True},
                        style={'display': 'inline-block'},
                        figure=fig20),
                    dcc.Graph(
                        id='basic-interactions21',
                        config={'editable': True},
                        style={'display': 'inline-block'},
                        figure=fig21),
                    dcc.Graph(
                        id='basic-interactions22',
                        config={'editable': True},
                        style={'display': 'inline-block'},
                        figure=fig22),
                ]),
        dcc.Tab(label='Initial Clinical Intake Compliance Dashboard',
                children=[
                    dcc.Graph(
                        id='basic-interactions2',
                        config={'editable': True},
                        figure=fig2),
                    html.Button('Transfer to?', id='button1'),
                    html.Div(
                        dash_table.DataTable(
                            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                            id='table',
                            columns=[{"name": i, "id": i} for i in df2.columns],
                            data=df2.to_dict('records'),
                            filter_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            row_selectable='multi',
                            page_action='native',
                            page_size=10,
                            export_format='xlsx'),
                    ),
                ]),
        dcc.Tab(label='Sick Call Monitoring',
                children=[
                    dcc.Graph(
                        id='basic-interactions1',
                        config={'editable': True},
                        figure=fig1),

                    dcc.Graph(
                        id='basic-interactions14',
                        config={'editable': True},
                        figure=fig14),
                    html.Button('Transfer to?', id='button2'),
                    html.Div(
                        dash_table.DataTable(
                            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                            id='table2',
                            columns=[{"name": i, "id": i} for i in df1.columns],
                            data=df1.to_dict('records'),
                            filter_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            row_selectable='multi',
                            page_action='native',
                            page_size=10,
                            export_format='xlsx'),
                    ),
                ]),

        dcc.Tab(label='Reentry Service Status',
                children=[
                    html.Br(),
                    html.Div(
                        cards),
                    dcc.Graph(
                        id='basic-interactions9',
                        config={'editable': True},
                        figure=fig9),
                    dcc.Graph(
                        id='basic-interactions5',
                        config={'editable': True},
                        figure=fig5,
                    ),
                    dcc.Dropdown(
                        id='filter_dropdown1',
                        options=[{"label": v, 'value': v} for v in value_categories1],
                        value=value_categories1[0],
                    ),
                    html.Button('Transfer to?', id='button10'),
                    dash_table.DataTable(id='table-container1',
                                         columns=[{'id': c, 'name': c} for c in df3.columns.values],
                                         filter_action='native',
                                         sort_action='native',
                                         sort_mode='multi',
                                         row_selectable='multi',
                                         page_action='native',
                                         page_size=20,
                                         export_format='xlsx'),

                ]),
        dcc.Tab(label='Encounters',
                children=[
                    html.Br(),
                    html.Div(
                        cards1),
                    html.Br(),
                    dcc.Graph(
                        id='basic-interactions33',
                        config={'editable': True},
                        figure=fig33),
                    dcc.Graph(
                        id='basic-interactions34',
                        config={'editable': True},
                        figure=fig34),
                    dcc.Graph(
                        id='basic-interactions35',
                        config={'editable': True},
                        figure=fig35),
                ]),
        dcc.Tab(label='Recidivism Baseline',
                children=[
                    dcc.Graph(
                        id='basic-interactions4',
                        config={'editable': True},
                        figure=fig4),

                    dcc.Graph(
                        id='basic-interactions3',
                        config={'editable': True},
                        figure=fig3),

                    dcc.Graph(
                        id='basic-interactions10',
                        config={'editable': True},
                        figure=fig10,
                        style={'display': 'inline-block'}),

                    dcc.Graph(
                        id='basic-interactions11',
                        config={'editable': True},
                        figure=fig11,
                        style={'display': 'inline-block'}),

                    dcc.Graph(
                        id='basic-interactions7',
                        config={'editable': True},
                        figure=fig7),
                    html.Br(),
                    html.Br(),
                    html.Button('Transfer to?', id='button4'),
                    html.Div(
                        dash_table.DataTable(
                            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                            id='table3',
                            columns=[{"name": i, "id": i} for i in df3.columns],
                            data=df3.to_dict('records'),
                            filter_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            row_selectable='multi',
                            page_action='native',
                            page_size=10,
                            export_format='xlsx'),
                    ),
                ]),
        dcc.Tab(label='Chronic Care Compliance',
                children=[
                    dcc.Graph(
                        id='basic-interactions16',
                        config={'editable': True},
                        figure=fig16),
                    dcc.Graph(
                        id='basic-interactions17',
                        config={'editable': True},
                        figure=fig17),
                    html.Button('Transfer to?', id='button5'),
                    html.Div(
                        dash_table.DataTable(
                            style_data={'whiteSpace': 'normal', 'height': 'auto', 'lineHeight': '15px'},
                            id='table6',
                            columns=[{"name": i, "id": i} for i in df4.columns],
                            data=df4.to_dict('records'),
                            filter_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            row_selectable='multi',
                            page_action='native',
                            page_size=10,
                            export_format='xlsx'),
                    ),
                ]),
        dcc.Tab(label='OCS',
                children=[
                    html.Br(),
                    html.Br(),
                    html.H4(id="title"),

                    dcc.Graph(
                        id='basic-interactions12',
                        config={'editable': True},
                        figure=fig12,
                        style={'display': 'inline-block'}),

                    dcc.Graph(
                        id='basic-interactions13',
                        config={'editable': True},
                        figure=fig13,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='basic-interactions8',
                        config={'editable': True},
                        figure=fig8,
                        style={'display': 'inline-block'}),
                    html.Div(
                        dash_table.DataTable(
                            id='click-data',
                            columns=[{"name": i, "id": i} for i in df3.columns],
                            data=df3.to_dict("records"),

                        ))
                ]),

        dcc.Tab(label='Recidivism Charts',
                children=[
                    html.Br(),
                    dcc.Graph(
                        id='fig23',
                        config={'editable': True},
                        figure=fig23,
                        style={'display': 'inline-block'}),

                    dcc.Graph(
                        id='fig24',
                        config={'editable': True},
                        figure=fig24,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig25',
                        config={'editable': True},
                        figure=fig25,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig26',
                        config={'editable': True},
                        figure=fig26,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig27',
                        config={'editable': True},
                        figure=fig27,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig28',
                        config={'editable': True},
                        figure=fig28,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig29',
                        config={'editable': True},
                        figure=fig29,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig30',
                        config={'editable': True},
                        figure=fig30,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig31',
                        config={'editable': True},
                        figure=fig31,
                        style={'display': 'inline-block'}),
                    dcc.Graph(
                        id='fig32',
                        config={'editable': True},
                        figure=fig32,
                        style={'display': 'inline-block'}),
                    html.Br(),
                    html.Div(
                        dash_table.DataTable(
                            id='click-data-test1',
                            columns=[{"name": i, "id": i} for i in df11.columns],
                            data=df11.to_dict("records"),
                            filter_action='native',
                            sort_action='native',
                            sort_mode='multi',
                            row_selectable='multi',
                            page_action='native',
                            page_size=10,
                            export_format='xlsx',
                        )),
                ])
    ])
])


# Callback for case manager filter
@app.callback(
    Output('table-container1', 'data'),
    [Input('filter_dropdown1', 'value')])
def display_table(select_category1):
    dff1 = df3[df3['Assigned To'] == select_category1]
    return dff1.to_dict('records')


# Callback for Initial Clinical Intake Compliance Dashboard clickData
@app.callback(
    Output("table", "data"),
    [Input("basic-interactions2", "clickData")],
)
def update_table1(clickData):
    path = ['Within24Hrs']
    data = df2.to_dict("records")
    dff1 = []
    if clickData:
        click_path = clickData["points"][0]["id"].split("/")
        selected = dict(zip(path, click_path))

        if "Within24Hrs" in selected:
            dff1 = df2[(df2["Within24Hrs"] == selected["Within24Hrs"])]
        data = dff1.to_dict("records")

    return data


# Callback for Charge Counts histogram on Recidivism Baseline Tab
@app.callback(
    Output("table3", "data"),
    [Input("basic-interactions7", "clickData")],
)
def update_table2(clickData):
    path = ['Most Recent Charge Description']
    data = df3.to_dict("records")
    dff1 = []
    if clickData:
        click_path = clickData["points"][0]["x"].split("/")
        selected = dict(zip(path, click_path))

        if "Most Recent Charge Description" in selected:
            dff1 = df3[(df3["Most Recent Charge Description"] == selected["Most Recent Charge Description"])]
        data = dff1.to_dict("records")

    return data


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# A1C data table filter within modal
@app.callback(
    Output('table9', 'data'),
    [Input('filter_dropdown', 'value')])
def display_table(select_category):
    dff1 = df[df['Value Categories'] == select_category]
    return dff1.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
