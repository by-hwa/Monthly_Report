# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options


def get_barchart():
    df = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
    })

    fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font_color='#7FDBFF',
    )
    return fig


def main():
    custom_setting_dict = {'file': '', 'chart type': '', 'x': '', 'y': '', 'height': '', 'width': ''}
    fig = get_barchart()
    csv_file_list = ['1.csv', '2.csv', '3.csv', '4.csv']
    # chart_list = ['bar chart', 'line chart', 'pie chart']

    app.layout = html.Div(style={'display': 'flex', 'flex-direction': 'row'}, children=[
        html.Div(
            # sidebar
            style={'flex': 1, 'width': '20%'},
            children=[
                html.H1(children=['Select Setting Step']),
                html.Button(children='Custom Setting', id='setting-btn', className='button'),
                html.Button(children='Make Report', id='report-btn', className='button'),
                html.Button(children='Manage Subscribe', id='subscribe-btn', className='button'),
            ])
        ,
        html.Div(style={'flex': 2, 'width': '60%'}, children=[# main page
            html.Div(
                id='main-page-context',
                style={'margin-left': '10%'},
                children=[
                    # 1st dropdown box
                    html.H1(children='Custom Setting Page'),
                    html.Br(),
                    html.Div(
                        style={'padding-right': '20%'},
                        children=[
                            html.H2(children='Select csv File'),
                            dcc.Dropdown(
                                style={'background-color': '#000000', 'color': '#aaa'},
                                options=csv_file_list,
                                placeholder='select file...',
                                id='dropdown-selected-file',
                            ),
                            html.Div(
                                style={'margin-top': '7.5%'},
                                id='selected-file',
                            ),
                        ],
                    ),
                    html.Div(  # chart type dropdown
                        style={'padding-right': '20%'},
                        id='select-chart-type-dropdown',
                        ),
                    ],
            ),
        ]),
    ])

    @app.callback(
        Output(component_id='selected-file', component_property='children'),
        Output(component_id='selected-file', component_property='className'),
        Input(component_id='dropdown-selected-file', component_property='value'),
        prevent_initial_call=True,
    )
    def update_selected_file(value):
        custom_setting_dict['file'] = value
        return f'Selected file [ {value} ]', 'ContentText'

    @app.callback(
        Output(component_id='select-chart-type-dropdown', component_property='children'),
        Input(component_id='dropdown-selected-file', component_property='value'),
        prevent_initial_call=True,
    )
    def render_chart_dropdown(value):
        chart_list = ['bar chart', 'line chart', 'pie chart']

        if value:
            return html.H2(children='Select Chart Type'), \
                   dcc.Dropdown(
                        style={'background-color': '#000000', 'color': '#aaa'},
                        options=chart_list,
                        placeholder='select file...',
                        id='dropdown-selected-chart-type',),\
                   html.Div(
                        style={'margin-top': '7.5%'},
                        id='selected-chart-type',)
        else:
            return ''

    @app.callback(
        Output(component_id='selected-chart-type', component_property='children'),
        Input(component_id='dropdown-selected-chart-type', component_property='value'),
        prevent_initial_call=True,
    )
    def update_selected_chart_type(value):
        custom_setting_dict['chart type'] = value
        return f'Selected Chart Type [ {value} ]'


if __name__ == '__main__':
    css_list = ['./assets/']
    app = Dash(__name__, external_stylesheets=css_list,
               suppress_callback_exceptions=True,
               # use_pages=True,
               title="Monthly Report",)
    main()
    app.run_server(debug=True)
