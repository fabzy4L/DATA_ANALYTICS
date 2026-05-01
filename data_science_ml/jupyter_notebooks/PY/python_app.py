import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="#")),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                children=[
                    dbc.DropdownMenuItem("Page 1", href="#"),
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("About", href="#"),
                ],
            ),
        ],
        brand="Demo",
        brand_href="#",
        sticky="top",
    ),
    html.Div(children=[
        html.H1(children='Hello Dash'),
        html.Div(children='''
            Dash: A web application framework for Python.
        '''),
        dcc.Input(id='input-box', type='text', value=''),
        html.Button('Submit', id='button'),
        html.Div(id='output-div')
    ]),
])

@app.callback(
    Output('output-div', 'children'),
    Input('button', 'n_clicks'),
    Input('input-box', 'value'))
def update_output(n_clicks, value):
    if n_clicks is not None:
        return 'You have entered "{}"'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)
