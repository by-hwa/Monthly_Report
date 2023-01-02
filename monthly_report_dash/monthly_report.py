import time
import flask
from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import json
from datetime import date, timedelta
import datetime
import api_module

data = pd.read_csv('./hour_summary_data.csv', index_col=0)
data.index = pd.to_datetime(data.index)
data['date'] = data.index
data['date'] = data['date'].apply(lambda x: x.date())
data["sumData"] = data["cycleIndex"] + data["contiIndex"]
health_percent = 0.5
month_data = data["sumData"]
limit = 10000
heatmap_click_x = '0/0/0'
heatmap_click_y = 0
barchart3_click_x = 0
heatmap_zmax = 0
heatmap_zmin = 0
heatmap_state = 'sumData'
heatmap_selected_btn = 'total'
timestamp = time.mktime(datetime.datetime.today().timetuple()) - 60 * 60 * 24 * 50
cycletime_stamp = pd.DataFrame()
display_list = []
filtered_data = data.copy()
line_data = pd.DataFrame()

op_dict = {0: "Off", 1: "Auto", 2: "Manual", 3: "Service", 4: "Error", 5: "Service2", 6: "Error2"}

colorscale = [[0.0, "rgb(79,41,146)"],
              # [0.1111111111111111, "rgb(215,48,39)"],
              # [0.2222222222222222, "rgb(244,109,67)"],
              # [0.3333333333333333, "rgb(253,174,97)"],
              # [0.4444444444444444, "rgb(254,224,144)"],
              [0.5, "rgb(234,80,135)"],
              # [0.6666666666666666, "rgb(171,217,233)"],
              # [0.7777777777777778, "rgb(116,173,209)"],
              # [0.8888888888888888, "rgb(69,117,180)"],
              [1.0, "rgb(237,217,163)"]]


def list2matrix(data, front):
    back = 24 - ((len(data) + front) % 24)
    matrix = np.concatenate(([0] * front, data, [0] * back)).reshape(-1, 24).T
    return matrix.astype(int)


def make_heat_map(monthdata=data["contiIndex"] + data["cycleIndex"], date=data['date'], colorscale=colorscale):
    global heatmap_zmax
    global heatmap_zmin

    monthdata = list2matrix(monthdata, front=9).copy()
    date_list = list(map(lambda x: f'{x.year % 100}/{x.month}/{x.day}', date.unique()))

    heatmap_zmax = monthdata.max()
    heatmap_zmin = monthdata.min()

    fig = go.Figure(data=go.Heatmap(
        z=monthdata,
        x=date_list,
        y=list(range(24)),
        text=monthdata[:, 0:31],
        xgap=1, ygap=1,
        texttemplate="%{text}",
        hovertemplate="%{x} %{y}h  <extra></extra>",
        textfont={"size": 10},
        colorscale=colorscale,
    ))

    fig.update_layout(
        autosize=False,
        width=800,
        height=500,
        showlegend=True,
        xaxis=dict(
            visible=True,
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
            # domain=[1, 1]
        ),
        yaxis=dict(
            autorange="reversed",
            visible=True,
            showgrid=False,
            showline=True,
            showticklabels=True,
            zeroline=False,
        ),
        yaxis_title="Hour",
        xaxis_title="Day",
        margin=dict(l=0, r=0, t=25, b=0), )
    return fig


def make_bar_chart1(operation_data=api_module.operation(timestamp)):
    operation_data['diff'] = operation_data['time_to'] - operation_data['time_from']

    state_df = operation_data[operation_data["type"] == "state"]
    state_df["class"] = state_df["data"].apply(lambda x: op_dict[x])

    fig = px.bar(state_df, x="diff", y="type",
                 color="class", barmode='stack',
                 color_discrete_map={
                     "Off": 'rgb(237, 230, 205)',
                     "Auto": 'rgb(40, 160, 161)',
                     "Manual": 'rgb(199,107,152)',
                     "Service": 'rgb(99,43,108)',
                     "Error": 'rgb(201,80,74)',
                     "Service2": 'rgb(18,81,76)',
                     "Error2": 'rgb(196, 118, 130)'
                 })
    fig.update_layout(
        coloraxis_showscale=False,
        autosize=False,
        width=700,
        height=80,
        xaxis=dict(
            showticklabels=True,
            title=""
        ),
        legend_title="운영 상태",
        yaxis=dict(
            visible=False
        ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=10, r=0, t=45, b=0),
        showlegend=True,
        legend=dict(yanchor="top", y=3, xanchor="left", orientation="h")
    )

    tickvalues = []
    # ticktexts = []

    for i in range(0, 3601, 600):
        tickvalues.append(i)
        # ticktexts.append(str(i//60)+'분')

    fig.update_xaxes(
        ticks="inside",
        ticklen=10,
        tickfont_size=1,
        # ticktext=ticktexts,
        tickvals=tickvalues
    )
    # min_value = operation_data['diff'][operation_data['diff'] > 0].min()
    # operation_data['diff'] = round((operation_data['time_to'] - operation_data['time_from']) / min_value).apply(int)

    # state_data = operation_data[operation_data['type'] == 'state']

    # run_color = {0: "black", 1: "cornsilk", 2: "aqua", 3: "lightseagreen", 4: "coral", 5: "teal"}
    # color_data = list()

    # y_data = ['운영']

    # colorscale1 = [[0.0, "rgb(0,0,0)"],
    #               [0.2, "rgb(215,48,39)"],
    #               [0.4, "rgb(244,109,67)"],
    #               [0.6, "rgb(253,174,97)"],
    #               [0.8, "rgb(254,224,144)"],
    #               [1.0, "rgb(224,243,248)"]]

    # print(state_data)

    # for i, value in enumerate(state_data['diff']):
    #     if value<=0:continue
    #     color_data += [state_data['flag'].iloc[i] for x in range(value)]

    # fig.add_trace(go.Heatmap(
    #     z=[color_data],
    #     y=y_data,
    #     zmax=5,
    #     zmin=0,
    #     colorscale=colorscale1,
    #     hoverinfo='none',
    #     showscale=False,
    # ))

    # fig.update_layout(
    #     # coloraxis_showscale=False,
    #     autosize=False,
    #     width=600,
    #     height=35,
    #     xaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=False,
    #         zeroline=False,
    #     ),
    #     yaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=True,
    #         zeroline=False,
    #     ),
    #     barmode='stack',
    #     paper_bgcolor='rgb(255, 255, 255)',
    #     plot_bgcolor='rgb(255, 255, 255)',
    #     margin=dict(l=30, r=0, t=0, b=10),
    #     showlegend=False,
    # )

    return fig


def make_bar_chart2(operation_data=api_module.operation(timestamp)):
    operation_data['diff'] = operation_data['time_to'] - operation_data['time_from']

    model_df = operation_data[operation_data["type"] == "model"]
    model_df["data"] = model_df["data"].astype(str)

    fig = px.bar(model_df, x="diff", y="type",
                 color="data", barmode='stack',
                 color_discrete_sequence=["rgb(67, 146, 192)", "rgb(246, 222, 126)", "rgb(227, 104, 87)",
                                          "rgb(240, 211, 186)"])
    fig.update_layout(
        coloraxis_showscale=False,
        autosize=False,
        width=700,
        height=80,
        xaxis=dict(
            showticklabels=True,
            title=""
        ),
        legend_title="생산 모델",

        yaxis=dict(visible=False
                   ),
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',

        margin=dict(l=10, r=0, t=45, b=0),
        showlegend=True,
        legend=dict(yanchor="top", y=3, xanchor="left", orientation="h")
    )

    tickvalues = []
    # ticktexts = []

    for i in range(0, 3601, 600):
        tickvalues.append(i)
        # ticktexts.append(str(i//60)+'분')

    fig.update_xaxes(
        ticks="inside",
        ticklen=10,
        tickfont_size=1,
        # ticktext=ticktexts,
        tickvals=tickvalues
    )
    # fig = go.Figure()

    # operation_data['diff'] = operation_data['time_to'] - operation_data['time_from']
    # min_value = operation_data['diff'][operation_data['diff'] > 0].min()
    # operation_data['diff'] = round((operation_data['time_to'] - operation_data['time_from']) / min_value).apply(int)

    # model_data = operation_data[operation_data['type'] == 'model']

    # # run_color = {0: "black", 1: "cornsilk", 2: "aqua", 3: "lightseagreen", 4: "coral", 5: "teal"}

    # color_data = list()

    # y_data = ['모델']

    # colorscale2 = [[0.0, "rgb(0,0,0)"],
    #               [0.2, "rgb(215,48,39)"],
    #               [0.4, "rgb(244,109,67)"],
    #               [0.6, "rgb(253,174,97)"],
    #               [0.8, "rgb(254,224,144)"],
    #               [1.0, "rgb(224,243,248)"]]

    # for i, value in enumerate(model_data['diff']):
    #     if value <= 0: continue
    #     color_data += [model_data['flag'].iloc[i] for x in range(value)]

    # if not color_data:color_data.append(0)

    # fig.add_trace(go.Heatmap(
    #     z=[color_data],
    #     y=y_data,
    #     zmax=100,
    #     zmin=0,
    #     colorscale=colorscale2,
    #     hoverinfo='none',
    #     showscale=False,
    # ))

    # fig.update_layout(
    #     # coloraxis_showscale=False,
    #     autosize=False,
    #     width=600,
    #     height=70,
    #     xaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=False,
    #         zeroline=False,
    #     ),
    #     yaxis=dict(
    #         showgrid=False,
    #         showline=False,
    #         showticklabels=True,
    #         zeroline=False,
    #     ),
    #     barmode='stack',
    #     paper_bgcolor='rgb(255, 255, 255)',
    #     plot_bgcolor='rgb(255, 255, 255)',
    #     margin=dict(l=30, r=0, t=0, b=10),
    #     showlegend=False,
    # )

    return fig


def make_bar_chart3(health_data=api_module.min_data(timestamp)):
    global cycletime_stamp
    global colorscale

    fig = go.Figure()

    color_data = [0 for x in range(60)]

    y_data = ['지표']

    if 'best_to' not in health_data.columns and 'best_from' not in health_data.columns:
        health_data['best_to'] = health_data['timeto']
        health_data['best_from'] = health_data['timefrom']

    cycletime_stamp = health_data[['timeto', 'timefrom', 'best_to', 'best_from']]

    for i, value in enumerate(health_data[heatmap_state]):
        color_data[i] = int(value)

    if heatmap_state == "cycleIndex":
        health_data["json"] = health_data.iloc[:, 4:11].abs().apply(
            lambda x: (x.loc[x == x.max()].keys()[0], int(x.loc[x == x.max()].values[0])), axis=1)
    elif heatmap_state == "contiIndex":
        health_data["json"] = health_data.iloc[:, 11:14].abs().apply(
            lambda x: (x.loc[x == x.max()].keys()[0], int(x.loc[x == x.max()].values[0])), axis=1)
    else:
        health_data["json"] = health_data.iloc[:, 4:14].abs().apply(
            lambda x: (x.loc[x == x.max()].keys()[0], int(x.loc[x == x.max()].values[0])), axis=1)

    fig.add_trace(go.Heatmap(
        z=[color_data],
        y=y_data,
        text=[[str(x).replace("0", "") for x in color_data]],
        texttemplate="%{text}",
        textfont={"size": 8},

        hovertext=[health_data["json"]],
        hovertemplate=
        "<b>%{x}min</b><br>" +
        "%{z}value<br>" +
        "%{hovertext}<br><extra></extra>",
        colorscale=colorscale,
        zmax=heatmap_zmax,
        zmin=heatmap_zmin,
        showscale=False,
        xgap=0.5,
    ))

    fig.update_layout(

        autosize=False,
        width=668,
        height=100,
        yaxis=dict(
            visible=False,
            title=""),
        barmode='stack',
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=10, r=0, t=0, b=0),

    )

    fig.add_annotation(dict(font=dict(color='black',
                                      size=15),
                            x=0,
                            y=-1,
                            showarrow=False,
                            text=(datetime.datetime.fromtimestamp(timestamp)).strftime('%Y-%m-%d %H:%M'),
                            textangle=0,
                            xanchor='left',
                            )),
    fig.add_annotation(dict(font=dict(color='black',
                                      size=15),
                            x=0,
                            y=1,
                            showarrow=False,
                            text="건정성 index      <= 왼쪽 색상 범위 참조",
                            textangle=0,
                            xanchor='left',
                            )
                       )

    return fig


def make_line_chart(raw_data=api_module.rawdata(timestamp, timestamp + 60 * 60)):
    if raw_data.empty:
        fig = px.line()
        return fig

    raw_data['timestamp'] = raw_data['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    fig = px.line(raw_data, x='timestamp', y=list(raw_data.columns))
    fig.update_layout(
        autosize=True,
        # showlegend=True,
        xaxis=dict(
            visible=True,
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=False,
            # domain=[1, 1]
        ),
        yaxis=dict(
            visible=True,
            showgrid=True,
            showline=True,
            showticklabels=True,
            zeroline=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0),
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1.02,
        #     xanchor="right",
        #     x=1
        # )
    )

    return fig


def render_main():
    def title_button_set():
        return html.Div(
            style={'display': 'grid', 'grid-auto-flow': 'column', 'grid-template-columns': 'auto 1fr'},
            id='btn-div',
            children=[
                dcc.DatePickerSingle(
                    # style={'margin': '1em'},
                    id='picked-date',
                    month_format='YYYY MM DD',
                    display_format='YYYY/MM/DD',
                    placeholder='YYYY MM DD',
                    min_date_allowed=date(2022, 8, 1),
                    max_date_allowed=date(2022, 11, 30),
                    initial_visible_month=date(2022, 11, 30),
                    date=date(2022, 11, 30), ),
                html.H2(children='Timezone: +9h', style={'margin-top': '0.5em', 'text-align': 'left',
                                                         'margin-left': '0.5em'}),
                html.Div(
                    style={'left-margin': 'auto'},
                    children=[
                        html.Button(id='cyclic', children='Cyclic', className='button'),
                        html.Button(id='conti', children='Conti.', className='button'),
                        html.Button(id='total', children='Total', className='button'),
                    ]
                ),
            ],
        )

    def heat_map():
        # fig = make_heat_map()
        return dcc.Graph(id='heat-map')

    def threshold_button_set():
        return html.Div(
            style={'display': 'grid', 'grid-auto-flow': 'column', 'grid-template-columns': '2fr', 'margin-top': '1em'},
            id='threshold-div',
            children=[
                dcc.Slider(0, 100, 1, value=50,
                           id='threshold',
                           marks={
                               0: {'label': '0%', 'style': {'color': '#77b0b1'}},
                               25: {'label': '25%'},
                               50: {'label': '50%'},
                               75: {'label': '75%'},
                               100: {'label': '100%', 'style': {'color': '#f50'}}
                           },
                           tooltip={"placement": "top", "always_visible": True},
                           included=False),
                html.Div(
                    style={'left-margin': 'auto', 'top-margin': '1em'},
                    children=[
                        html.Button(id='apply', children='적용', className='button'),
                        # html.Button(id='normal', children='정상', className='button'),
                        # html.Button(id='abnormal', children='비정상', className='button'),
                    ]
                ),
            ],
        )

    return html.Div(id='main-context',
                    style={'flex': 3},
                    children=[
                        title_button_set(),
                        heat_map(),
                        html.H3("건전성 판정 기준(%)"),
                        threshold_button_set(),
                        html.H3(id="health-percent"),
                    ])


def render_detail():
    def bar_chart():
        # fig1 = make_bar_chart1()
        # fig2 = make_bar_chart2()
        # fig3 = make_bar_chart3()

        return html.Div(
            children=[dcc.Graph(id='bar-chart1'),
                      dcc.Graph(id='bar-chart2'),
                      dcc.Graph(id='bar-chart3')]
        )

    def linechart():
        # fig = make_line_chart()
        return dcc.Graph(id='line-chart')

    def filter_button_set():
        return html.Div(
            children=[
                html.H3('필터 :'),
                html.Button(id='filter-normal', children='정상', className='button', n_clicks=1,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-abnormal', children='비교', className='button', n_clicks=1,
                            style={'margin-left': '5%'}),

                html.Button(id='filter-operation', children='운영', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-accessory', children='유틸', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-slide', children='각도', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),

                html.Button(id='filter-force', children='포스', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-pressure', children='압력', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),

                html.Button(id='filter-position', children='위치', className='button', n_clicks=0,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-servo', children='서보', className='button', n_clicks=1,
                            style={'margin-left': '5%'}),
                html.Button(id='filter-1', children='1번', className='button', n_clicks=1, style={'margin-left': '5%'}),
                html.Button(id='filter-2', children='2번', className='button', n_clicks=1, style={'margin-left': '5%'}),
                html.Button(id='filter-3', children='3번', className='button', n_clicks=1, style={'margin-left': '5%'}),
                html.Button(id='filter-4', children='4번', className='button', n_clicks=1, style={'margin-left': '5%'}),
            ]
        )

    return html.Div(id='detail-context', style={'flex': 2, 'margin-left': '2%'},
                    children=[
                        html.Br(style={'height': '100'}),
                        bar_chart(),
                        linechart(),
                        filter_button_set(),
                        html.Div(id='test')
                    ])


def main():
    app.layout = html.Div(
        style={'display': 'flex', 'flex-direction': 'row', 'margin': '2.5%'},
        children=[render_main(), render_detail()], )

    @app.callback(
        Output(component_id='heat-map', component_property='figure'),
        Output(component_id='health-percent', component_property='children'),
        Output(component_id='cyclic', component_property='style'),
        Output(component_id='conti', component_property='style'),
        Output(component_id='total', component_property='style'),
        Input(component_id='picked-date', component_property='date'),
        State(component_id='threshold', component_property='value'),
        Input(component_id='cyclic', component_property='n_clicks'),
        Input(component_id='conti', component_property='n_clicks'),
        Input(component_id='total', component_property='n_clicks'),
        Input(component_id='apply', component_property='n_clicks'),
        prevent_initial_call=False,
    )
    def update_heatmap(picked_date, threshold, *args):
        global data
        global health_percent
        global month_data
        global limit
        global filtered_data
        global heatmap_state
        global heatmap_selected_btn
        global colorscale

        picked_date = datetime.date.fromisoformat(picked_date)
        filtered_data = data[(data['date'] - picked_date > datetime.timedelta(-31)) &
                             (data['date'] - picked_date <= datetime.timedelta(0))]

        triggered_id = ctx.triggered_id

        style_list = [{}, {}, {}]
        location = {'cyclic': 0, 'conti': 1, 'total': 2}

        if triggered_id == 'apply':
            health_percent = threshold / 100
            colorscale[1] = [health_percent, "rgb(234,80,135)"]

        elif triggered_id == 'cyclic':
            heatmap_state = "cycleIndex"
            heatmap_selected_btn = 'cyclic'
            limit = filtered_data["cycleIndex"].loc[filtered_data["cycleIndex"] > 0].quantile(health_percent / 100)
        elif triggered_id == 'conti':
            heatmap_state = "contiIndex"
            heatmap_selected_btn = 'conti'
            limit = filtered_data["contiIndex"].loc[filtered_data["contiIndex"] > 0].quantile(health_percent / 100)
        elif triggered_id == 'total':
            heatmap_state = "sumData"
            heatmap_selected_btn = 'total'
            limit = filtered_data["sumData"].loc[filtered_data["sumData"] > 0].quantile(health_percent / 100)

        month_data = filtered_data[heatmap_state]

        message = f'설정된 건정성 판정 기준은 {(health_percent * 100)}% 입니다.'

        style_list[location[heatmap_selected_btn]] = {'border-bottom': ' solid', 'border-bottom-color': '#000000'}

        return make_heat_map(monthdata=month_data.copy(), date=filtered_data['date'].copy(),
                             colorscale=colorscale), message, *style_list

    @app.callback(
        Output(component_id='bar-chart1', component_property='figure'),
        Output(component_id='bar-chart2', component_property='figure'),
        Output(component_id='bar-chart3', component_property='figure'),
        Input(component_id='picked-date', component_property='date'),
        Input(component_id='heat-map', component_property='clickData'),
        Input(component_id='apply', component_property='n_clicks'),
        prevent_initial_call=False,
    )
    def update_barchart(picked_date, clickData, *args):
        global heatmap_click_x
        global heatmap_click_y
        global timestamp

        if clickData:
            heatmap_click_x = clickData['points'][0]['x']
            heatmap_click_y = clickData['points'][0]['y']

        y, m, d = map(int, heatmap_click_x.split('/'))

        picked_date = datetime.date.fromisoformat(picked_date)
        # timestamp = time.mktime((picked_date-datetime.timedelta(days=int(heatmap_click_x), hours=int(heatmap_click_y))).timetuple())

        if heatmap_click_x == '0/0/0':
            timestamp = time.mktime(picked_date.timetuple())
        else:
            timestamp = time.mktime(
                datetime.datetime(year=(2000 + y), month=m, day=d, hour=int(heatmap_click_y)).timetuple())
            print(timestamp)

        lt = time.localtime()
        timeoffset = lt.tm_gmtoff
        timestamp = timestamp + 60 * 60 * 9 - timeoffset
        operation_data = api_module.operation(timestamp)
        min_data = api_module.min_data(timestamp)

        return make_bar_chart1(operation_data), make_bar_chart2(operation_data), make_bar_chart3(min_data)

    @app.callback(
        Output(component_id='line-chart', component_property='figure'),

        Output(component_id='filter-normal', component_property='style'),
        Output(component_id='filter-abnormal', component_property='style'),

        Output(component_id='filter-force', component_property='style'),
        Output(component_id='filter-pressure', component_property='style'),
        Output(component_id='filter-position', component_property='style'),
        Output(component_id='filter-servo', component_property='style'),

        Output(component_id='filter-1', component_property='style'),
        Output(component_id='filter-2', component_property='style'),
        Output(component_id='filter-3', component_property='style'),
        Output(component_id='filter-4', component_property='style'),

        Output(component_id='filter-operation', component_property='style'),
        Output(component_id='filter-slide', component_property='style'),
        Output(component_id='filter-accessory', component_property='style'),

        Input(component_id='bar-chart3', component_property='clickData'),

        Input(component_id='filter-normal', component_property='n_clicks'),
        Input(component_id='filter-abnormal', component_property='n_clicks'),

        Input(component_id='filter-force', component_property='n_clicks'),
        Input(component_id='filter-pressure', component_property='n_clicks'),
        Input(component_id='filter-position', component_property='n_clicks'),
        Input(component_id='filter-servo', component_property='n_clicks'),

        Input(component_id='filter-1', component_property='n_clicks'),
        Input(component_id='filter-2', component_property='n_clicks'),
        Input(component_id='filter-3', component_property='n_clicks'),
        Input(component_id='filter-4', component_property='n_clicks'),

        Input(component_id='filter-operation', component_property='n_clicks'),
        Input(component_id='filter-slide', component_property='n_clicks'),
        Input(component_id='filter-accessory', component_property='n_clicks'),

        prevent_initial_call=False,
    )
    def update_linechart(clickData, *args):
        # global filter_state
        global cycletime_stamp
        global barchart3_click_x

        # triggered_id = ctx.triggered_id

        if clickData:
            barchart3_click_x = clickData['points'][0]['x']

        if not cycletime_stamp.empty:
            raw_data1 = api_module.rawdata(cycletime_stamp.iloc[barchart3_click_x]['timefrom'],
                                           cycletime_stamp.iloc[barchart3_click_x]['timeto'])
            raw_data2 = api_module.rawdata(cycletime_stamp.iloc[barchart3_click_x]['best_from'],
                                           cycletime_stamp.iloc[barchart3_click_x]['best_to'])
            raw_data2.drop('timestamp', axis=1, inplace=True, errors='ignore')
            raw_data1.columns = list(map(lambda x: "비교_" + x if not x == 'timestamp' else x, raw_data1.columns))
            raw_data2.columns = list(map(lambda x: "정상_" + x, raw_data2.columns))
            raw_data = pd.concat([raw_data1, raw_data2], axis=1)
        else:
            # time_now = time.mktime(datetime.datetime.today().timetuple())
            # raw_data = api_module.rawdata(time_now-3600, time_now)
            raw_data = api_module.rawdata(1665187398.77, 1665187403.75)

        display_list = list(raw_data.columns)

        filter_dict = {0: '정상_', 1: '비교_', 2: 'force', 3: 'pressure', 4: 'position', 5: 'servo', 6: '1', 7: '2', 8: '3',
                       9: '4', 10: "op", 11: "slide", 12: "acc"}
        btn_state_list = [{} for i in range(len(args))]

        force_list = ['cushion 1 force', 'cushion 2 force', 'cushion 3 force', 'cushion 4 force', 'cushion 1 set force',
                      'cushion 2 set force', 'cushion 3 set force', 'cushion 4 set force']
        pressure_list = ['cushion 1 pressure A ', 'cushion 1 pressure B', 'cushion 2 pressure A',
                         'cushion 2 pressure B', 'cushion 3 pressure A', 'cushion 3 pressure B', 'cushion 4 pressure A',
                         'cushion 4 pressure B']
        position_list = ['cushion 1 position', 'cushion 2 position', 'cushion 3 position', 'cushion 4 position',
                         'cushion 1 set position', 'cushion 2 set position', 'cushion 3 set position',
                         'cushion 4 set position']
        servo_list = ['cushion 1 servo output ', 'cushion 1 servo feedback', 'cushion 2 servo output',
                      'cushion 2 servo feedback', 'cushion 3 servo output', 'cushion 3 servo feedback',
                      'cushion 4 servo output', 'cushion 4 servo feedback']
        op_list = ['oReady', 'oNoError', 'oAuto', 'oManual', 'oService', ]
        slide_list = ['slide angle', 'slide position', 'die number']
        acc_list = ['oil temperature', 'main pump 1 pressure', 'main pump 2 pressure', 'pilot pump pressure',
                    'acc 1 pressure', 'acc 2 pressure']

        for i, click in enumerate(args):

            if click % 2:
                btn_state_list[i] = {'border-bottom': ' solid', 'border-bottom-color': '#000000'}
            else:
                if i in [0, 1, 6, 7, 8, 9]:
                    display_list = [x for x in display_list if filter_dict[i] not in x]

        if not args[2] % 2:
            display_list = [x for x in display_list if x[3:] not in force_list]
        if not args[3] % 2:
            display_list = [x for x in display_list if x[3:] not in pressure_list]
        if not args[4] % 2:
            display_list = [x for x in display_list if x[3:] not in position_list]
        if not args[5] % 2:
            display_list = [x for x in display_list if x[3:] not in servo_list]
        if not args[10] % 2:
            display_list = [x for x in display_list if x[3:] not in op_list]
        if not args[11] % 2:
            display_list = [x for x in display_list if x[3:] not in slide_list]
        if not args[12] % 2:
            display_list = [x for x in display_list if x[3:] not in acc_list]

        if 'timestamp' not in display_list: display_list.append('timestamp')
        display_list = [x for x in display_list if "tank" not in x]

        return make_line_chart(raw_data[display_list].copy()), *btn_state_list


if __name__ == '__main__':
    css_list = ['./assets/']

    app = Dash(__name__, external_stylesheets=css_list, suppress_callback_exceptions=True,
               url_base_pathname='/', title="Monthly Report", )

    main()

    # app.run_server(debug=True)
    app.run_server(host='0.0.0.0', port=8050)