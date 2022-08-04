from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from datetime import date

# data import
df = pd.read_csv('data.csv', parse_dates=['Date', 'First of the Year'])

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = '.decimal - Operational Dashboard'

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem"
}

sidebar = html.Div(
    [
        html.Img(src=app.get_asset_url("logo.svg"), height="50px"),
        html.Hr(),
        html.P(
            "Operational Dashboard", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Finance", href="/finance", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

# date picker
date_picker = dcc.DatePickerRange(
    id="date-picker",
    start_date_placeholder_text="Start Period",
    end_date_placeholder_text="End Period",
    start_date=date(2022,4,9),
    end_date=date.today(),
    style={
        'margin-top' : '2%',
        'margin-bottom' : '2%'
    },
    clearable=True,
    reopen_calendar_on_clear=True
)

# annualized EBITDA figure
fig = go.Figure()
fig.add_trace(go.Scatter(
    name='Goal',
    mode="lines",
    x=df['Date'],
    y=df['Goal'],
    line=dict(color='red')
))
fig.add_trace(go.Scatter(
    name='Ann. EBITDA',
    x=df['Date'],
    y=df['Annualized EBITDA'],
    hovertemplate='<br><b>Date</b>: %{x|%m/%d/%Y}<br>'+'<b>EBITDA</b>: $%{y:,.2f}',
    line=dict(color='blue')
))
fig.update_layout(
    title={
        'text': "Annualized EBITDA",
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top',
        'font': dict(
            family='Sans-Serif',
            size=28,
            color='#747c84')},
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1,
                     label="1m",
                     step="month",
                     stepmode="backward"),
                dict(count=6,
                     label="6m",
                     step="month",
                     stepmode="backward"),
                dict(count=1,
                     label="YTD",
                     step="year",
                     stepmode="todate"),
                dict(count=1,
                     label="1y",
                     step="year",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=False
        ),
        type="date"
    )
)
fig.update_xaxes(
    dtick="M1",
    tickformat="%b\n%Y"
)
fig.update_yaxes(
    rangemode='tozero',
    tickformat="$,.0f"
)


content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    finance_content = html.Div([
        html.Div([
            html.H1('Financial Reporting', style={'flex-grow': '1'}),
            date_picker], style={'display': 'inline-flex', 'align-items': 'center', 'width': '100%'}),
        dcc.Graph(id="annualized-ebitda", figure=fig)
    ])

    if pathname == "/":
        return html.P("This is the content of the home page!")
    elif pathname == "/finance":
        return finance_content
    elif pathname == "/page-2":
        return html.P("This is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )

@app.callback(
    Output("annualized-ebitda", "figure"),
    [Input("date-picker", "start_date"),
     Input("date-picker", "end_date")],
    prevent_initial_call=True)
def update_chart(start_date, end_date):
    mask = (df['Date'] >= start_date) & (df['Date'] <= end_date)
    dff = df.loc[mask]

    updated_fig = go.Figure()
    updated_fig.add_trace(go.Scatter(
        name='Goal',
        mode="lines",
        x=dff['Date'],
        y=dff['Goal'],
        line=dict(color='red')
    ))
    updated_fig.add_trace(go.Scatter(
        name='Ann. EBITDA',
        x=dff['Date'],
        y=dff['Annualized EBITDA'],
        hovertemplate='<br><b>Date</b>: %{x|%m/%d/%Y}<br>' + '<b>EBITDA</b>: $%{y:,.2f}',
        line=dict(color='blue')
    ))
    updated_fig.update_layout(
        title={
            'text': "Annualized EBITDA",
            'y': 0.9,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': dict(
                family='Sans-Serif',
                size=28,
                color='#747c84')},
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=1,
                         label="1m",
                         step="month",
                         stepmode="backward"),
                    dict(count=6,
                         label="6m",
                         step="month",
                         stepmode="backward"),
                    dict(count=1,
                         label="YTD",
                         step="year",
                         stepmode="todate"),
                    dict(count=1,
                         label="1y",
                         step="year",
                         stepmode="backward"),
                    dict(step="all")
                ])
            ),
            rangeslider=dict(
                visible=False
            ),
            type="date"
        )
    )
    updated_fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y"
    )
    updated_fig.update_yaxes(
        rangemode='tozero',
        tickformat="$,.0f"
    )

    return updated_fig




if __name__ == '__main__':
    app.run()
