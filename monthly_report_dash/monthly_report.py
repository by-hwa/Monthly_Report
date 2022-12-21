import time
import flask
from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
import json
from datetime import date
import datetime
import api_module

data = pd.read_csv('./hour_summary_data.csv', index_col=0)
data.index = pd.to_datetime(data.index)
data['date'] = data.index
data['date'] = data['date'].apply(lambda x: x.date())
data["sumData"] = data["cycleIndex"]+data["contiIndex"]
health_percent = 0.5
month_data = data["sumData"]
limit = 10000
heatmap_click_x = 0
heatmap_click_y = 0
barchart3_click_x = 0
heatmap_zmax = 0
heatmap_zmin = 0
heatmap_state = 'sumData'
heatmap_selected_btn = 'total'
timestamp = time.mktime(datetime.datetime.today().timetuple())
cycletime_stamp = pd.DataFrame()
filter_state = True

filtered_data = data.copy()

colorscale = [[0.0, "rgb(49,54,149)"],
                    # [0.1111111111111111, "rgb(215,48,39)"],
                    # [0.2222222222222222, "rgb(244,109,67)"],
                    # [0.3333333333333333, "rgb(253,174,97)"],
                    # [0.4444444444444444, "rgb(254,224,144)"],
                    [health_percent, "rgb(224,243,248)"],
                    # [0.6666666666666666, "rgb(171,217,233)"],
                    # [0.7777777777777778, "rgb(116,173,209)"],
                    # [0.8888888888888888, "rgb(69,117,180)"],
                    [1.0, "rgb(165,0,38)"]]


def list2matrix(data, front):
    back = 24 - ((len(data) + front) % 24)
    matrix = np.concatenate(([0]*front, data, [0]*back)).reshape(-1, 24).T
    return matrix.astype(int)


def make_heat_map(monthdata=data["contiIndex"] + data["cycleIndex"],
                 limit=10000, normal=False, abnormal=False):

    global heatmap_zmax
    global heatmap_zmin

    if normal: monthdata[monthdata < limit] = 0
    elif abnormal: monthdata[monthdata > limit] = 0

    monthdata = list2matrix(monthdata, front=9).copy()

    heatmap_zmax = monthdata.max()
    heatmap_zmin = monthdata.min()

    fig = go.Figure(data=go.Heatmap(
        z=monthdata[:, 0:31],
        x=list(range(1, 32, 1)),
        y=list(range(24)),
        text=monthdata[:, 0:31],
        xgap=1, ygap=1,
        texttemplate="%{text}",
        hovertemplate="%{x}day %{y}hour  <extra></extra>",
        textfont={"size": 10},
        colorscale=colorscale,
    ))

    # fig = ff.create_annotated_heatmap(monthdata[:, 0:31], x=list(range(1, 32, 1)), y=list(range(24)),
    #                                   annotation_text=monthdata[:, 0:31], colorscale='phase', xgap=1, ygap=1)
    fig.update_layout(margin=dict(t=2, r=2, b=2, l=2), width=1400, height=700, xaxis=dict(showgrid=False),
                      yaxis=dict(autorange="reversed", showgrid=False), yaxis_title="Hour", xaxis_title="Day")
    # fig.data[0].hovertemplate = "%{x}day %{y}hour  <extra></extra>"

    fig.update_layout(
        # title='GitHub commits per day',
        # xaxis_nticks=36,
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
            visible=True,
            showgrid=False,
            showline=True,
            showticklabels=True,
            zeroline=False,
        ),
        margin=dict(l=0, r=0, t=0, b=0), )
    return fig


def make_bar_chart1(operation_data=api_module.operation(timestamp)):

    fig = go.Figure()

    operation_data['diff'] = operation_data['time_to'] - operation_data['time_from']

    state_data = operation_data[operation_data['type'] == 'state']

    run_color = {0: "black", 1: "cornsilk", 2: "aqua", 3: "lightseagreen", 4: "coral", 5: "teal"}
    color_data = [0 for x in range(60)]

    y_data = ['운영']

    colorscale = [[0.0, "rgb(0,0,0)"],
                  [0.2, "rgb(215,48,39)"],
                  [0.4, "rgb(244,109,67)"],
                  [0.6, "rgb(253,174,97)"],
                  [0.8, "rgb(254,224,144)"],
                  [1.0, "rgb(224,243,248)"]]

    for i, value in enumerate(state_data['diff']):
        color_data[i] = state_data['flag'].iloc[i]

    fig.add_trace(go.Heatmap(
        z=[color_data],
        y=y_data,
        colorscale=colorscale,
        hoverinfo='none',
        showscale=False,
    ))

    fig.update_layout(
        # coloraxis_showscale=False,
        autosize=False,
        width=600,
        height=35,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=30, r=0, t=0, b=10),
        showlegend=False,
    )

    return fig


def make_bar_chart2(operation_data=api_module.operation(timestamp)):
    fig = go.Figure()

    operation_data['diff'] = operation_data['time_to'] - operation_data['time_from']

    model_data = operation_data[operation_data['type'] == 'model']

    # run_color = {0: "black", 1: "cornsilk", 2: "aqua", 3: "lightseagreen", 4: "coral", 5: "teal"}

    color_data = [0 for x in range(60)]

    y_data = ['모델']

    colorscale = [[0.0, "rgb(0,0,0)"],
                  [0.2, "rgb(215,48,39)"],
                  [0.4, "rgb(244,109,67)"],
                  [0.6, "rgb(253,174,97)"],
                  [0.8, "rgb(254,224,144)"],
                  [1.0, "rgb(224,243,248)"]]

    for i, value in enumerate(model_data['diff']):
        color_data[i] = model_data['flag'].iloc[i]

    fig.add_trace(go.Heatmap(
        z=[color_data],
        y=y_data,
        colorscale=colorscale,
        hoverinfo='none',
        showscale=False,
    ))

    fig.update_layout(
        # coloraxis_showscale=False,
        autosize=False,
        width=600,
        height=70,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=30, r=0, t=0, b=10),
        showlegend=False,
    )

    return fig


def make_bar_chart3(health_data=api_module.min_data(timestamp)):
    global cycletime_stamp

    fig = go.Figure()

    color_data = [0 for x in range(60)]

    y_data = ['건강도']

    if 'best_to' not in health_data.columns and 'best_from' not in health_data.columns:
        health_data['best_to'] = health_data['timeto']
        health_data['best_from'] = health_data['timefrom']

    cycletime_stamp = health_data[['timeto', 'timefrom', 'best_to', 'best_from']]

    for i, value in enumerate(health_data[heatmap_state]):
        color_data[i] = health_data[heatmap_state].iloc[i]

    fig.add_trace(go.Heatmap(
        z=[color_data],
        y=y_data,
        hovertemplate="%{x}min %{z}health",
        colorscale=colorscale,
        zmax=heatmap_zmax,
        zmin=heatmap_zmin,
        showscale=False,
    ))

    fig.update_layout(
        # coloraxis_showscale=False,
        autosize=False,
        width=600,
        height=70,
        xaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            zeroline=False,
        ),
        barmode='stack',
        paper_bgcolor='rgb(255, 255, 255)',
        plot_bgcolor='rgb(255, 255, 255)',
        margin=dict(l=30, r=0, t=0, b=10),
        showlegend=False,
    )

    return fig


def make_line_chart(raw_data=api_module.rawdata(timestamp, timestamp+60*60)):

    if raw_data.empty:
        fig = px.line()
        return fig

    raw_data['timestamp'] = raw_data['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x))

    fig = px.line(raw_data, x='timestamp', y=list(raw_data.columns))
    fig.update_layout(
        autosize=True,
        showlegend=True,
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
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
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
                    max_date_allowed=date.today(),
                    initial_visible_month=date.today(),
                    date=date.today(),),
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
                        html.H3("건정성 판정 기준(%)"),
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
                html.Button(id='filter-normal', children='정상', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-abnormal', children='불량', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-input', children='입력', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-location', children='위치', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-servo', children='서보', className='button', n_clicks=1, style={'margin-left': '5%'}),
                html.Button(id='filter-1', children='1번', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-2', children='2번', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-3', children='3번', className='button', n_clicks=0, style={'margin-left': '5%'}),
                html.Button(id='filter-4', children='4번', className='button', n_clicks=0, style={'margin-left': '5%'}),
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
        children=[render_main(), render_detail()],)

    @app.callback(
        Output(component_id='heat-map', component_property='figure'),
        Output(component_id='cyclic', component_property='style'),
        Output(component_id='conti', component_property='style'),
        Output(component_id='total', component_property='style'),
        Input(component_id='picked-date', component_property='date'),
        Input(component_id='cyclic', component_property='n_clicks'),
        Input(component_id='conti', component_property='n_clicks'),
        Input(component_id='total', component_property='n_clicks'),
        Input(component_id='apply', component_property='n_clicks'),
        # Input(component_id='normal', component_property='n_clicks'),
        # Input(component_id='abnormal', component_property='n_clicks'),
        prevent_initial_call=False,
    )
    def update_chart(picked_date, *args):
        global data
        global health_percent
        global month_data
        global limit
        global filtered_data
        global heatmap_state
        global heatmap_selected_btn

        normal = False
        abnormal = False

        picked_date = datetime.date.fromisoformat(picked_date)
        filtered_data = data[(data['date'] - picked_date > datetime.timedelta(-31)) &
                             (data['date'] - picked_date <= datetime.timedelta(0))]

        triggered_id = ctx.triggered_id

        style_list = [{}, {}, {}]
        location = {'cyclic': 0, 'conti': 1, 'total': 2}

        if triggered_id == 'cyclic':
            month_data = filtered_data["cycleIndex"]
            heatmap_state = "cycleIndex"
            heatmap_selected_btn = 'cyclic'
            limit = filtered_data["cycleIndex"].loc[filtered_data["cycleIndex"] > 0].quantile(health_percent/100)
        elif triggered_id == 'conti':
            month_data = filtered_data["contiIndex"]
            heatmap_state = "contiIndex"
            heatmap_selected_btn = 'conti'
            limit = filtered_data["contiIndex"].loc[filtered_data["contiIndex"] > 0].quantile(health_percent/100)
        elif triggered_id == 'total':
            month_data = filtered_data["sumData"]
            heatmap_state = "sumData"
            heatmap_selected_btn = 'total'
            limit = filtered_data["sumData"].loc[filtered_data["sumData"] > 0].quantile(health_percent/100)
        elif triggered_id == 'normal':
            normal = True
        elif triggered_id == 'abnormal':
            abnormal = True

        style_list[location[heatmap_selected_btn]] = {'border-bottom': ' solid', 'border-bottom-color': '#000000'}

        return make_heat_map(monthdata=month_data.copy(), limit=limit, normal=normal, abnormal=abnormal), *style_list

    @app.callback(
        Output(component_id='health-percent', component_property='children'),
        State(component_id='threshold', component_property='value'),
        Input(component_id='apply', component_property='n_clicks'),
    )
    def update_health_state(threshold, n_click):
        global health_percent
        health_percent = threshold / 100
        return f'설정된 건정성 판정 기준은 {(health_percent * 100)}% 입니다.'

    @app.callback(
        Output(component_id='bar-chart1', component_property='figure'),
        Output(component_id='bar-chart2', component_property='figure'),
        Output(component_id='bar-chart3', component_property='figure'),
        Input(component_id='picked-date', component_property='date'),
        Input(component_id='heat-map', component_property='clickData'),
        prevent_initial_call=False,
    )
    def update_barchart(picked_date, clickData, *args):
        global heatmap_click_x
        global heatmap_click_y
        global timestamp

        if clickData:
            heatmap_click_x = clickData['points'][0]['x']
            heatmap_click_y = clickData['points'][0]['y']

        picked_date = datetime.date.fromisoformat(picked_date)
        timestamp = time.mktime((picked_date-datetime.timedelta(days=int(heatmap_click_x), hours=int(heatmap_click_y))).timetuple())
        operation_data = api_module.operation(timestamp)
        min_data = api_module.min_data(timestamp)

        return make_bar_chart1(operation_data), make_bar_chart2(operation_data), make_bar_chart3(min_data)

    @app.callback(
        Output(component_id='line-chart', component_property='figure'),
        Output(component_id='filter-normal', component_property='style'),
        Output(component_id='filter-abnormal', component_property='style'),
        Output(component_id='filter-input', component_property='style'),
        Output(component_id='filter-location', component_property='style'),
        Output(component_id='filter-servo', component_property='style'),
        Output(component_id='filter-1', component_property='style'),
        Output(component_id='filter-2', component_property='style'),
        Output(component_id='filter-3', component_property='style'),
        Output(component_id='filter-4', component_property='style'),
        Input(component_id='bar-chart3', component_property='clickData'),
        Input(component_id='bar-chart3', component_property='figure'),
        Input(component_id='filter-normal', component_property='n_clicks'),
        Input(component_id='filter-abnormal', component_property='n_clicks'),
        Input(component_id='filter-input', component_property='n_clicks'),
        Input(component_id='filter-location', component_property='n_clicks'),
        Input(component_id='filter-servo', component_property='n_clicks'),
        Input(component_id='filter-1', component_property='n_clicks'),
        Input(component_id='filter-2', component_property='n_clicks'),
        Input(component_id='filter-3', component_property='n_clicks'),
        Input(component_id='filter-4', component_property='n_clicks'),
        prevent_initial_call=False,
    )
    def update_linechart(clickData, fig, *args):
        global filter_state
        global cycletime_stamp
        global barchart3_click_x

        triggered_id = ctx.triggered_id

        filter_dict = {0: 'normal', 1: 'abnormal', 2: 'input', 3: 'position', 4: 'servo', 5: '1', 6: '2', 7: '3', 8: '4'}
        btn_state_list = [{} for i in range(len(args))]

        if clickData:
            barchart3_click_x = clickData['points'][0]['x']

        if triggered_id == 'filter-normal':filter_state=True
        elif triggered_id == 'filter-abnormal':filter_state=False

        if filter_state:
            time_from = 'timefrom'
            time_to = 'timeto'
        else:
            time_from = 'best_from'
            time_to = 'best_to'

        if not cycletime_stamp.empty:
            print(cycletime_stamp.iloc[barchart3_click_x].apply(lambda x : '%f' % x))
            raw_data = api_module.rawdata(cycletime_stamp.iloc[barchart3_click_x][time_from], cycletime_stamp.iloc[barchart3_click_x][time_to])
        else:
            time_now = time.mktime(datetime.datetime.today().timetuple())
            raw_data = api_module.rawdata(time_now-3600, time_now)
        display_list = list(raw_data.columns)

        # if triggered_id and 'filter' in triggered_id:
        for i, click in enumerate(args):
            if click % 2:
                if filter_dict[i] == 'normal' or filter_dict[i] == 'abnormal':continue
                display_list = [x for x in display_list if filter_dict[i] in x]
                btn_state_list[i] = {'border-bottom': ' solid', 'border-bottom-color': '#000000'}

        if 'timestamp' not in display_list: display_list.append('timestamp')

        return make_line_chart(raw_data[display_list].copy()), *btn_state_list

    # @app.callback(
    #     Output(component_id='test', component_property='children'),
    #     Input(component_id='bar-chart3', component_property='clickData')
    # )
    # def test(c):
    #     asdf='timeto'
    #     a = cycletime_stamp.iloc[c['points'][0]['x']][asdf]
    #     b = cycletime_stamp.iloc[c['points'][0]['x']]['timefrom']
    #     c = a-b
    #
    #     return '{}'.format(cycletime_stamp)


if __name__ == '__main__':
    css_list = ['./assets/']

    app = Dash(__name__, external_stylesheets=css_list, suppress_callback_exceptions=True,
               url_base_pathname='/', title="Monthly Report",)

    main()

    app.run_server(debug=True)

