from dash import Dash, html, dcc, Input, Output


def main():
    layout = html.Div(children=[
      html.H1('page1 입니다.')
    ])


if __name__ == '__main__':
    Dash.register_page(__name__)
    main()
