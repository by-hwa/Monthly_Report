from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import dash_draggable
import pandas as pd

# def drag_and_drop_test():
#     return html.Div(
#         style={'color': 'red'},
#         children=[
#             dash_draggable.GridLayout(
#                 style={'background-color': 'gray'},
#                 id='draggable',
#                 children=[
#                     html.Div(
#                         style={'width': '50px', 'height': '50px', 'color': '#505050'},
#                         children=['1']
#                     ),
#                     html.Div(
#                         style={'width': '150px', 'height': '150px', 'color': '#505050'},
#                         children=['2']
#                     ),
#                     html.H2(children='안녕하세요 !', style={'color':'black'})
#                 ]
#             ),
#             ]
#         )

# def drag_and_drop_test():
#     df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#     return html.Div([
#     html.H1("Dash Draggable"),
#     html.B("Description:"),
#     html.Ul([
#         html.Li("The chart is not draggable nor resizeable (with the value 'static' set to True in 'layout')."),
#         html.Li("The slider is draggable and resizeable.")
#     ]),
#     dash_draggable.GridLayout(
#         id='draggable',
#         clearSavedLayout=True,
#         # layout=[
#         #     {
#         #         "i": "graph-with-slider",
#         #         "x":0, "w":8, "y":0, "h":12, "static": True
#         #     },
#         #     {
#         #         "i": "year-slider",
#         #         "x": 0, "w":8, "y":13, "h":2
#         #     },
#         # ],
#         children=[
#             dcc.Graph(
#                 # id='graph-with-slider',
#                 responsive=True,
#                 style={
#                     "width":"100%",
#                     "height":"100%",
#
#                 }),
#             dcc.Slider(
#                 # id='year-slider',
#                 min=df['year'].min(),
#                 max=df['year'].max(),
#                 value=df['year'].min(),
#                 marks={str(year): str(year) for year in df['year'].unique()},
#                 step=None)
#         ]
#     ),
#     html.Div(id='drag-test')
# ])
