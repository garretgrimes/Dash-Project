from whitenoise import WhiteNoise
import dash_auth
import pandas as pd
import dash
from dash import dcc
import plotly.express as px
import plotly.graph_objs as go
from dash import dash_table
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

df = pd.read_excel('C:/Users/garre/PycharmProjects/dash-demo/lab_results_cleaned.xlsx')
by_month1 = pd.to_datetime(df['create_timestamp']).dt.to_period('M').value_counts().sort_index()
by_month1.index = pd.PeriodIndex(by_month1.index)
df_month1 = by_month1.rename_axis('month').reset_index(name='counts')
value_categories1 = df['Value Categories'].unique().tolist()

df1 = pd.read_excel('a1c_linechart.xlsx')

df2 = pd.read_excel('cc_records.xlsx')

df3 = pd.read_excel('tests.xlsx')

transfer_options = ['John Smith', 'Jerry Kibler', 'Amy Lettering', 'Pam Jones']

fig = px.pie(df, names='Value Categories', title='A1C Distribution')

fig1 = px.bar(df1, x='Date', y='Count', color='Value Categories', barmode='group', text_auto='.2',
              title='A1C Result Ranges Time Series')
fig1.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)

fig1.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig2 = go.Figure(data=go.Scatter(x=df_month1['month'].astype(dtype=str), y=df_month1['counts'], text="counts"))
fig2.update_layout({"title": 'A1C Labs Completed by Month', "xaxis": {"title": "Months"},
                    "yaxis": {"title": "Total"}, "showlegend": False})
fig2.update_xaxes(dtick='M1', tickformat="%b\n%Y")

fig3 = px.pie(df2, names='service_item_desc', title='Chronic Care Clinic Visits')

fig4 = px.line(df3, x='Date', y='Count', color='Chronic Care Visit Type', markers=True,
               title='Chronic Care Clinic Visit Type')
fig4.update_xaxes(dtick='M1', tickformat="%b\n%Y")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.wsgi_app = WhiteNoise(server.wsgi_app, root='static/')

auth = dash_auth.BasicAuth(
    app,
    {'guest': 'openarms'}
)

modal_1 = html.Div([
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("A1C Values")),
        html.Br(),
        dbc.Button("Transfer to?",
                   className="ms-auto",
                   id="open-toggle-modal-2",
                   n_clicks=0,
                   ),
        html.Br(),
        dcc.Dropdown(
            id='filter_dropdown',
            options=[{"label": i, 'value': i} for i in value_categories1],
            value=value_categories1[0],
            placeholder='Please select...'),
        dbc.ModalBody(
            dash_table.DataTable(
                id='table',
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

    ],
        id="toggle-modal-1",
        is_open=False,
        size="xl",
    ),
]
)

modal_2 = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Transfer Options")),
        dbc.ModalBody("Select who to transfer analysis to"),
        dcc.Dropdown(
            id='filter_dropdown1',
            options=[{"label": i, 'value': i} for i in transfer_options],
            value=value_categories1[0],
            placeholder='Please select...'),
        html.Br(),
        dcc.ConfirmDialogProvider(
            children=html.Button('Transfer to?'), id='button122',
            message='Transfer Complete!'),
        dbc.ModalFooter(
            dbc.Button(
                "Back to Dataset",
                id="open-toggle-modal-1",
                className="ms-auto",
                n_clicks=0),

        ),
    ],
    id="toggle-modal-2",
    is_open=False,
)

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
                    html.Div([
                        dcc.Graph(
                            id='basic-interactions',
                            config={'editable': True},
                            figure=fig),
                        html.Br(),
                        dcc.Graph(
                            id='basic-interactions1',
                            config={'editable': True},
                            figure=fig1),
                        html.Br(),
                        dcc.Graph(
                            id='basic-interactions2',
                            config={'editable': True},
                            figure=fig2),
                        html.Div(
                            [
                                modal_1,
                                modal_2,
                            ]
                        )

                    ])
                ]),
        dcc.Tab(label='Chronic Care',
                children=[
                    html.Div([
                        dcc.Graph(
                            id='basic-interactions3',
                            config={'editable': True},
                            figure=fig3),
                        dcc.Graph(
                            id='basic-interactions4',
                            config={'editable': True},
                            figure=fig4),
                    ])
                ]),
        dcc.Tab(label='Encounters'),
    ])
])


@app.callback(
    Output("toggle-modal-1", "is_open"),
    [
        Input("basic-interactions", "clickData"),
        Input("basic-interactions1", "clickData"),
        Input("open-toggle-modal-1", "n_clicks"),
        Input("open-toggle-modal-2", "n_clicks"),
    ],
    [State("toggle-modal-1", "is_open")],
)
def toggle_modal_1(n0, n1, n2, n3, is_open):
    if n0 or n1 or n2 or n3:
        return not is_open
    return is_open


@app.callback(
    Output("toggle-modal-2", "is_open"),
    [
        Input("open-toggle-modal-2", "n_clicks"),
        Input("open-toggle-modal-1", "n_clicks"),
    ],
    [State("toggle-modal-2", "is_open")],
)
def toggle_modal_2(n2, n1, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output('table', 'data'),
    [Input('filter_dropdown', 'value')])
def display_table(select_category):
    dff1 = df[df['Value Categories'] == select_category]
    return dff1.to_dict('records')


if __name__ == '__main__':
    app.run_server(debug=True)
