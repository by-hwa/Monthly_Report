# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output, ctx, State, dash_table
import plotly.express as px
import pandas as pd
import paho.mqtt.client as mqtt
import json


# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("connected OK")
    else:
        print("Bad connection Returned code=", rc)


def on_disconnect(client, userdata, flags, rc=0):
    print(str(rc))


def on_subscribe(client, userdata, mid, granted_qos):
    print("subscribed: " + str(mid) + " " + str(granted_qos))


def on_message(client, userdata, msg):
    json_msg = json.loads(str(msg.payload.decode("utf-8")))
    # print(json_msg)
    json_mqtt.append(json_msg)


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


def render_sidebar():
    return html.Div(
        # sidebar
        style={'flex': 1, 'width': '20%'},
        children=[
            html.H1(children=['Select Setting Step']),
            html.Button(children='Custom Setting', id='setting-btn', className='button'),
            html.Button(children='Make Report', id='report-btn', className='button'),
            html.Button(children='Manage Subscribe', id='subscribe-btn', className='button'),
        ])


def render_main():
    return html.Div(id='main-page-context',
                    style={'flex': 3, 'width': '60%'},)


def default_page():
    return html.Div(
                style={'margin-left': '10%'},
                children=[
                    html.H1(children='매달 정기 발간 리포트'),
                    html.Br(),
                    html.H4(children='사용자 설정을 통하여 원하는 양식 또는 형식의 리포트를 구독 설정하는 웹')
                    ],
            )


def make_report():
    return html.Div(
                style={'margin-left': '10%'},
                children=[
                    # 1st dropdown box
                    html.H1(children='Make Report Page'),
                    html.Br(),
                    html.Div(
                        style={'padding-right': '20%'},
                        children=[
                            html.H2(children='Select report template'),
                            dcc.Dropdown(
                                style={'background-color': '#000000', 'color': '#aaa'},
                                options=template_list,
                                placeholder='select template...',
                                id='dropdown-selected-template',
                            ),
                            html.Div(
                                style={'margin-top': '7.5%'},
                                id='selected-template',)
                        ]
                    ),
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
                    html.Div(id='selected-file-df'),
                    html.Div(  # chart type dropdown
                        style={'padding-right': '20%'},
                        id='select-chart-type-dropdown',
                        ),
                    ],
            )


def select_chart_type():
    return html.H2(children='Select Chart Type'), \
                    dcc.Dropdown(
                        style={'background-color': '#000000', 'color': '#aaa'},
                        options=chart_list,
                        placeholder='select chart...',
                        id='dropdown-selected-chart-type',),\
                    html.Div(
                        style={'margin-top': '7.5%'},
                        id='selected-chart-type',),\
                    html.Div(
                        id='select-data-value-dropdown')


def select_data_value():
    return html.H2(children='Select data value1'), \
                dcc.Dropdown(
                    style={'background-color': '#000000', 'color': '#aaa'},
                    options=data_list,
                    placeholder='select data value1...',
                    id='dropdown-selected-data-value1',),\
                html.H2(children='Select data value2'), \
                dcc.Dropdown(
                    style={'background-color': '#000000', 'color': '#aaa'},
                    options=data_list,
                    placeholder='select data value2...',
                    id='dropdown-selected-data-value2',),\
                html.Div(
                    style={'margin-top': '7.5%'},
                    id='selected-data-value',),\
                html.Div(
                    id='input-width-height')


def enter_width_height():
    return html.Div(style={'display': 'flex', 'flex-direction': 'row'},
                    children=[
                     html.Div(
                         style={'flex': 1, 'width': '100%'},
                         children=[
                             html.H2(children='Enter Width'),
                             dcc.Input(
                                 style={'background-color': '#000000', 'color': '#aaa', 'font-size': '25',
                                        'width': '90%', 'height': '3em'},
                                 type='number',
                                 placeholder='Enter width..,',
                                 min=50,
                                 max=1000,
                                 step=50,
                                 debounce=False,
                                 id='input-width', ),
                         ]),
                     html.Div(
                         style={'flex': 1, 'width': '100%'},
                         children=[
                             html.H2(children='Enter Height'),
                             dcc.Input(
                                 style={'background-color': '#000000', 'color': '#aaa', 'font-size': '25',
                                        'width': '90%', 'height': '3em'},
                                 type='number',
                                 placeholder='Enter height...',
                                 min=50,
                                 max=1000,
                                 step=50,
                                 debounce=False,
                                 id='input-height', ),
                         ]
                     )
                    ]),\
           html.Div(
                style={'margin-top': '7.5%'},
                id='entered-width-height',),\
           html.Div(
                style={'margin-top': '7.5%'},
                id='make-exam-button', ),\
           html.Div(
                style={'margin-top': '7.5%'},
                id='make-exam', )


def custom_setting():
    return html.Div(
                style={'margin-left': '10%'},
                children=[
                    # 1st dropdown box
                    html.H1(children='Custom Setting Page'),
                    html.Br(),
                    html.Div(
                        style={'padding-right': '20%'},
                        children=[
                            html.H2(children='Select Equipment'),
                            dcc.Dropdown(
                                style={'background-color': '#000000', 'color': '#aaa'},
                                options=equipment_list,
                                placeholder='select equipment...',
                                id='dropdown-selected-equipment',
                            ),
                            html.Div(
                                style={'margin-top': '7.5%'},
                                id='selected-equipment',
                            ),
                        ],
                    ),
                    html.Div(  # chart type dropdown
                        style={'padding-right': '20%'},
                        id='select-ETL-recipe-dropdown',
                        ),
                    ],
            )


def select_ETL_recipe():
    return html.H2(children='Select ETL Recipe'),\
                dcc.Dropdown(
                    style={'background-color': '#000000', 'color': '#aaa'},
                    options=ETL_recipe_list,
                    placeholder='select ETL recipe...',
                    id='dropdown-selected-ETL-recipe',
                ),\
                html.Div(
                    style={'margin-top': '7.5%'},
                    id='selected-ETL-recipe',)


def make_exam_button():
    return html.Button(children='Make Exam', id='make-exam-btn', className='push-button')


def render_exam():
    if custom_setting_dict['chart type'] == 'scatter':
        fig = px.scatter(data_frame=mqtt_df, x=custom_setting_dict['value1'], y=custom_setting_dict['value2'])
    elif custom_setting_dict['chart type'] == 'line chart':
        fig = px.line(data_frame=mqtt_df, x=custom_setting_dict['value1'], y=custom_setting_dict['value2'])
    elif custom_setting_dict['chart type'] == 'bar chart':
        fig = px.bar(data_frame=mqtt_df, x=custom_setting_dict['value1'], y=custom_setting_dict['value2'])
    elif custom_setting_dict['chart type'] == 'pie chart':
        fig = px.pie(data_frame=mqtt_df, names=custom_setting_dict['value1'], values=custom_setting_dict['value2'])
    fig.update_layout(
        plot_bgcolor='#000000',
        paper_bgcolor='#000000',
        font_color='#7FDBFF',)

    return html.H2(children='Exam Report',),\
        dcc.Graph(figure=fig)


def build_data_table():
    return dash_table.DataTable(
                data=mqtt_df.to_dict('records'),
                columns=[{'id': c, 'name': c}for c in mqtt_df.columns],
                style_header={
                    'backgroundColor': 'rgb(30, 30, 30)',
                    'color': 'white'
                },
                style_data={
                    'backgroundColor': 'rgb(50, 50, 50)',
                    'color': 'white'
                },
                page_size=10,
                style_table={'overflowX': 'auto', 'overflowY': 'auto'},
                )


def manage_subscribe():
    return html.Div(
                style={'margin-left': '10%'},
                children=[
                    # 1st dropdown box
                    html.H1(children='Subscribe Manage Page'),
                    html.Br(),
                    html.Div(
                        style={'padding-right': '20%'},
                        children=[
                            html.H2(children='Setting Info'),
                            html.Div(
                                style={'background-color': '#303030', 'margin-bottom': '5%'},
                                children=[
                                    html.Div(children=['선택된 템플릿 [ {} ]'.format(custom_setting_dict['template'])]),
                                    html.Div(children=['선택된 데이터 [ {} ]'.format(custom_setting_dict['file'])]),
                                    html.Div(children=['선택된 차트 타입 [ {} ]'.format(custom_setting_dict['chart type'])]),
                                    html.Div(children=['선택된 x, value [ {} ]'.format(custom_setting_dict['value1'])]),
                                    html.Div(children=['선택된 y, value [ {} ]'.format(custom_setting_dict['value2'])]),
                                    html.Div(children=['설정된 Width [ {} ]'.format(custom_setting_dict['width'])]),
                                    html.Div(children=['설정된 Height [ {} ]'.format(custom_setting_dict['height'])]),
                                ],),
                            html.Div(
                                style={'display': 'flex', 'flex-direction': 'row'},
                                children=[
                                    html.Div(
                                        style={'flex': 1, 'width': '100%', 'margin-right': '2.5%'},
                                        children=[html.Button(children='설정 구독 주기 리포트 발행', id='period-report-btn',
                                                              className='push-button')]),
                                    html.Div(
                                        style={'flex': 1, 'width': '100%'},
                                        children=[html.Button(children='트리거 동작시 리포트 발행', id='triggered-report-btn',
                                                              className='push-button')]),
                                ]),
                            html.Div(id='setting-report-period'),
                            html.Div(id='setting-subscribe-method'),
                            html.Div(id='download-report')
                            ])
                    ])


def period_setting():
    return html.Div(
        style={'display': 'flex', 'flex-direction': 'row', 'margin-top': '5%'},
        children=[
            html.H3(children='주기 : '),
            dcc.Dropdown(id='select-period', options=['매달', '매주', '매일'], style={'margin': '2.5%'}),
            html.H3(children='날짜 : '),
            dcc.Dropdown(id='select-date', options=[x for x in range(30)], style={'margin': '2.5%'}),
            html.H3(children='요일 : '),
            dcc.Dropdown(id='select-day', options=['월', '화', '수', '목', '금', '토', '일'], style={'margin': '2.5%'}),
            html.H3(children='시간 : '),
            dcc.Dropdown(id='select-time', options=[str(x)+':00' for x in range(24)], style={'margin': '2.5%'})
        ])


def triggered_setting():
    return html.Div(
        style={'margin-top': '5%'},
        children=[html.H2('트리거 선택'),
                  dcc.Dropdown(id='selected-trigger', options=['tri1', 'tri2', 'tri3'], multi=True)])


def select_subscribe_type():
    return html.Div(
        children=[
            html.H2('구독 방법 선택'),
            dcc.Dropdown(options=subscribe_type, style={'margin-bottom': '5%'}),
            html.Button('구독', className='push-button')
        ]
    )


def download():
    return html.Br(),\
            html.Button("Download Report", id="btn-download-report", className='push-button'),\
            dcc.Download(id="download-report")


def main():
    app.layout = html.Div(style={'display': 'flex', 'flex-direction': 'row'}, children=[
        render_sidebar(),
        render_main(),
    ])

    # Make Report 파일 선택

    @app.callback(
        Output(component_id='selected-template', component_property='children'),
        Input(component_id='dropdown-selected-template', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_template(value):
        custom_setting_dict['template'] = value
        return f'Selected Template is [ {value} ]'

    @app.callback(
        Output(component_id='selected-file', component_property='children'),
        Output(component_id='selected-file', component_property='className'),
        Output(component_id='selected-file-df', component_property='children'),
        Input(component_id='dropdown-selected-file', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_file(value):
        custom_setting_dict['file'] = value
        if value:
            return f'Selected file [ {value} ]', 'ContentText', build_data_table()
        else:
            return f'Selected file [ {value} ]', 'ContentText', ''

    @app.callback(
        Output(component_id='select-chart-type-dropdown', component_property='children'),
        Input(component_id='dropdown-selected-file', component_property='value'),
        prevent_initial_call=False,
    )
    def render_chart_dropdown(value):
        if value:
            return select_chart_type()

    @app.callback(
        Output(component_id='selected-chart-type', component_property='children'),
        Input(component_id='dropdown-selected-chart-type', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_chart_type(value):
        custom_setting_dict['chart type'] = value
        return f'Selected Chart Type [ {value} ]'

    @app.callback(
        Output(component_id='select-data-value-dropdown', component_property='children'),
        # Input(component_id='dropdown-selected-file', component_property='value'),
        Input(component_id='dropdown-selected-chart-type', component_property='value'),
        prevent_initial_call=True,
    )
    def render_data_value_dropdown(value):
        if value:
            return select_data_value()

    @app.callback(
        Output(component_id='selected-data-value', component_property='children'),
        Output(component_id='input-width-height', component_property='children'),
        Input(component_id='dropdown-selected-data-value1', component_property='value'),
        Input(component_id='dropdown-selected-data-value2', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_data_value(value1, value2):
        if value1 and value2:
            custom_setting_dict['value1'] = value1
            custom_setting_dict['value2'] = value2
            return f'Selected Data Value1 is [ {value1} ], Value2 is [ {value2} ]', enter_width_height()
        else:
            return f'Selected Data Value1 is [ {value1} ], Value2 is [ {value2} ]', ''

    @app.callback(
        Output(component_id='entered-width-height', component_property='children'),
        Output(component_id='make-exam-button', component_property='children'),
        Input(component_id='input-width', component_property='value'),
        Input(component_id='input-height', component_property='value'),
        prevent_initial_call=False,
    )
    def update_entered_value(value1, value2):
        if value1 and value2:
            custom_setting_dict['width'] = value1
            custom_setting_dict['height'] = value2
            return f'Width : [ {value1} ], Height : [ {value2} ]', make_exam_button()
        else:
            return f'Width : [ {value1} ], Height : [ {value2} ]', ''

    @app.callback(
        Output(component_id='make-exam', component_property='children'),
        Input(component_id='make-exam-btn', component_property='n_clicks'),
    )
    def update_render_exam(n_clicks):
        if n_clicks:
            return render_exam()

    # custom setting
    @app.callback(
        Output(component_id='selected-equipment', component_property='children'),
        Input(component_id='dropdown-selected-equipment', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_equipment(value):
        return f'Selected Equipment is [ {value} ]'

    @app.callback(
        Output(component_id='select-ETL-recipe-dropdown', component_property='children'),
        Input(component_id='dropdown-selected-equipment', component_property='value'),
        prevent_initial_call=True,
    )
    def render_ETL_reciep_dropdwon(value):
        if value:
            return select_ETL_recipe()

    @app.callback(
        Output(component_id='selected-ETL-recipe', component_property='children'),
        Input(component_id='dropdown-selected-ETL-recipe', component_property='value'),
        prevent_initial_call=False,
    )
    def update_selected_ETL_recipe(value):
        return f'Selected ETL Recipe is [ {value} ]'

    @app.callback(
        Output(component_id='setting-report-period', component_property='children'),
        Output(component_id='setting-subscribe-method', component_property='children'),
        Output(component_id='download-report', component_property='children'),
        Input(component_id='period-report-btn', component_property='n_clicks'),
        Input(component_id='triggered-report-btn', component_property='n_clicks'),
        prevent_initial_call=True,
    )
    def update_subscribe_period_setting(*args):
        triggered_id = ctx.triggered_id
        if triggered_id == 'period-report-btn':
            return period_setting(), select_subscribe_type(), download()
        elif triggered_id == 'triggered-report-btn':
            return triggered_setting(), select_subscribe_type(), download()

    @app.callback(
        Output(component_id='select-date', component_property='disabled'),
        Output(component_id='select-day', component_property='disabled'),
        Output(component_id='select-time', component_property='disabled'),
        Input(component_id='select-period', component_property='value'),
        prevent_initial_call=False,
    )
    def update_setting_list(value, *args):
        return_value = [True, True, True]
        if value == '매달':
            return_value[0] = False
            return_value[2] = False
        elif value == '매주':
            return_value[1] = False
            return_value[2] = False
        elif value == '매일':
            return_value[2] = False

        return return_value

    @app.callback(
        Output("download-text", "data"),
        Input("btn-download-txt", "n_clicks"),
        prevent_initial_call=True,
    )
    def func(n_clicks):
        return dict(content=mqtt_df.to_csv, filename="Reports.csv")

    # sidebar
    @app.callback(
        Output(component_id='main-page-context', component_property='children'),
        Output(component_id='setting-btn', component_property='style'),
        Output(component_id='report-btn', component_property='style'),
        Output(component_id='subscribe-btn', component_property='style'),

        Input(component_id='setting-btn', component_property='n_clicks'),
        Input(component_id='report-btn', component_property='n_clicks'),
        Input(component_id='subscribe-btn', component_property='n_clicks'),
        prevent_inital_call=True,
    )
    def upload_main_page(*args):
        triggered_id = ctx.triggered_id
        return_value = [default_page(), {}, {}, {}]
        if triggered_id == 'setting-btn':
            return_value[0] = custom_setting()
            return_value[1] = {'border-color': '#65A4ECFF'}
            return return_value
        elif triggered_id == 'report-btn':
            return_value[0] = make_report()
            return_value[2] = {'border-color': '#65A4ECFF'}
            return return_value
        elif triggered_id == 'subscribe-btn':
            return_value[0] = manage_subscribe()
            return_value[3] = {'border-color': '#65A4ECFF'}
            return return_value
        else:
            return return_value


if __name__ == '__main__':

    json_mqtt = []

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe
    client.on_message = on_message
    # address : localhost, port: 1883 에 연결
    client.connect('3.38.255.45', 1883)
    # common topic 으로 메세지 발행
    client.subscribe('vib_data')

    css_list = ['./assets/']
    app = Dash(__name__, external_stylesheets=css_list,
               suppress_callback_exceptions=True,
               # use_pages=True,
               title="Monthly Report",)

    custom_setting_dict = {'template': '', 'file': '', 'chart type': '', 'value1': '', 'value2': '', 'height': '', 'width': ''}
    equipment_list = ['nc쿠션', 'press', 'other']
    template_list = ['월간 운영 리포트', '월간 보전 리포트', '특정 기간의 변화 체크 리포트']
    csv_file_list = ['1.csv', '2.csv', '3.csv', '4.csv']
    chart_list = ['bar chart', 'line chart', 'pie chart', 'scatter']
    ETL_recipe_list = ['mean', 'std', 'min', 'max', 'mid']
    subscribe_period = ['설정 구독 주기 리포트 발행', '트리거 동작시 리포트 발행']
    subscribe_type = ['메일 내 링크', 'pdf', 'excel']

    for i in range(100):
        client.loop()
    mqtt_df = pd.DataFrame(json_mqtt).applymap(lambda x: ', '.join(list(map(str, x))) if type(x) == list else x)
    data_list = mqtt_df.columns
    client.disconnect()
    main()

    app.run_server(debug=True)
