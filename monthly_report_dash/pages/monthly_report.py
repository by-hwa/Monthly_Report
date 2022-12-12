import flask
from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import plotly.express as px
import pandas as pd
import json


def main():
    app.layout = html.Div(
        children=['안녕하세요'],
    )


if __name__ == '__main__':
    css_list = ['./assets/']

    app = Dash(__name__, external_stylesheets=css_list, suppress_callback_exceptions=True,
               url_base_pathname='/', title="Monthly Report",)

    main()

    app.run_server(debug=True)

