import base64
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
from dash import dash_table
import plotly.graph_objs as go

df = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\lab_results_cleaned.xlsx')
by_month1 = pd.to_datetime(df['create_timestamp']).dt.to_period('M').value_counts().sort_index()
by_month1.index = pd.PeriodIndex(by_month1.index)
df_month1 = by_month1.rename_axis('month').reset_index(name='counts')
value_categories = df['Value Categories'].unique().tolist()

df1 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\SickCalls.xlsx')
by_month = pd.to_datetime(df1['SickCallCompletedAt']).dt.to_period('M').value_counts().sort_index()
by_month.index = pd.PeriodIndex(by_month.index)
df_month = by_month.rename_axis('month').reset_index(name='counts')

df2 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\BookinToIntakeAssessment.xlsx')

df3 = pd.read_excel(r'C:\Users\garre\PycharmProjects\my-python-app\calvert_cleaned.xlsx')
df3['Assigned To'] = df3['Assigned To'].fillna('Unknown')
value_categories1 = df3['Assigned To'].unique().tolist()
value_categories2 = df3['Gender'].unique().tolist()

df4 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\cc_records.xlsx')

df5 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\tests.xlsx')

df6 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\a1c_linechart.xlsx')

df7 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\hep_c_results.xlsx')

df8 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\PT_results.xlsx')

df9 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\HIV_results.xlsx')

df10 = pd.read_excel(r'C:\Users\garre\Desktop\Envisioneering\inr_cleaned.xlsx')

fig = px.pie(df, names='Value Categories', title='A1C Values')
fig.update_layout(title_x=0.49)

fig1 = px.pie(df1, names='Range Interval', title='Sick Call Range')

fig2 = px.pie(df2, names='Within24Hrs', title='Booked to Intake Assessment')

fig3 = px.histogram(df3, x="Assigned To", color="Recid", title="Recidivism by Provider")

fig4 = px.pie(df3, names="Recid", title="Recidivism True or False")

fig5 = px.histogram(df3, x="Assigned To", color="Reentry Service Status", title='Reentry Service Status by Provider')

fig7 = px.histogram(df3, x="Most Recent Charge Description", title='Charge Counts')
fig7.update_xaxes(title_text='')

fig8 = px.histogram(df3, x='Origin', title="Origin")

fig9 = px.pie(df3, names='Assigned To', title='Reentry Caseloads')

fig10 = px.pie(df3, names='Number of Bookings', title='Number of Bookings')

fig11 = px.pie(df3, names='Age Categories', title='Age Categories')

fig12 = px.pie(df3, names='Gender', title='Gender')
fig12.update_layout(clickmode='event+select')

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

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

image_logo = 'C:/Users/garre/Desktop/Envisioneering/logo.png'


def b64_image(image_file_name):
    with open(image_file_name, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    html.Br(),
    html.Img(src=b64_image(image_logo), style={'textAlign': 'center', 'height': '20%', 'width': '20%'}),
    html.H1("Analytics Dashboards", style={'text-align': 'center', 'color': '#4FA1F3'}),
    dcc.Tabs([
        dcc.Tab(label='A1C Dashboard',
                children=[
                    dcc.Graph(
                        id='basic-interactions',
                        config={'editable': True},
                        figure=fig),
                    dcc.Graph(
                        id='basic-interactions15',
                        config={'editable': True},
                        figure=fig15),
                    dcc.Graph(
                        id='basic-interactions18',
                        config={'editable': True},
                        figure=fig18),

                    dcc.Dropdown(
                        id='filter_dropdown',
                        options=[{"label": v, 'value': v} for v in value_categories],
                        value=value_categories[0],
                    ),
                    dcc.ConfirmDialogProvider(
                        children=html.Button('Transfer to?'), id='button',
                        message='This could be used to send the analysis that was completed to a workflow that could '
                                'trigger other individuals to take action on the analysis that was conducted.'),

                    dash_table.DataTable(id='table-container',
                                         columns=[{'id': c, 'name': c} for c in df.columns.values],
                                         filter_action='native',
                                         sort_action='native',
                                         sort_mode='multi',
                                         row_selectable='multi',
                                         page_action='native',
                                         page_size=20,
                                         export_format='xlsx'),

                ]),
        dcc.Tab(label='Other Lab Results',
                children=[
                    dcc.Dropdown(
                        id='filter_dropdown3',
                        options=[{"label": 'Hepatitis C', 'value': 'HEPC'},
                                 {'label': 'PT', 'value': 'PT'},
                                 {'label': 'HIV', 'value': 'HIV'}],
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
                            data=df2.to_dict('records'),  # contents of data table
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
                            data=df1.to_dict('records'),  # contents of data table
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
                    dcc.Graph(
                        id='basic-interactions9',
                        config={'editable': True},
                        figure=fig9),
                    dcc.Graph(
                        id='basic-interactions5',
                        config={'editable': True},
                        figure=fig5),

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
                            data=df3.to_dict('records'),  # contents of data table
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
                    html.Div(id='click-data')
                ]),
    ])
])


@app.callback(
    Output('table-container', 'data'),
    [Input('filter_dropdown', 'value')])
def display_table(select_category):
    dff = df[df['Value Categories'] == select_category]
    return dff.to_dict('records')


@app.callback(
    Output('table-container1', 'data'),
    [Input('filter_dropdown1', 'value')])
def display_table(select_category1):
    dff1 = df3[df3['Assigned To'] == select_category1]
    return dff1.to_dict('records')


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions12', 'selectedData')])
def display_table(selectedData):
    dff2 = df3[df3['Gender'] == selectedData]
    return dff2.to_dict('records'),


if __name__ == '__main__':
    app.run_server(debug=True)