import streamlit as st
import plotly.express as px
import pandas as pd


def load_data(path):
    df = pd.read_csv(path)
    df.rename(columns={'persionId': 'personID'}, inplace=True)
    df.drop(df.columns[0], axis=1, inplace=True)
    df.set_index(keys=['personID', 'time'], inplace=True, drop=True)

    return df


def get_info_bar_and_line_chart(df: pd.DataFrame):
    x = st.sidebar.selectbox('Select X ', ['index'])
    y = st.sidebar.selectbox('Select Y ', df.columns)
    width = st.sidebar.number_input('Enter width', min_value=50, max_value=500, value=100, step=50)
    height = st.sidebar.number_input('Enter height', min_value=50, max_value=500, value=300, step=50)
    st.sidebar.write(f'x : [{x}] y : [{y}]')
    st.sidebar.write(f'width : [{width}], height : [{height}]')
    return x, y, width, height


def get_info_pie_chart(df: pd.DataFrame):
    columns = list(df.columns)
    value = st.sidebar.selectbox('Select Value ', columns)
    columns.remove(value)
    name = st.sidebar.selectbox('Select Names ', columns)
    width = st.sidebar.number_input('Enter width', min_value=0, max_value=500, value=100, step=50)
    height = st.sidebar.number_input('Enter height', min_value=0, max_value=500, value=300, step=50)
    st.sidebar.write(f'Value : [{value}] name : [{name}]')
    st.sidebar.write(f'width : [{width}], height : [{height}]')
    if value != name:
        return value, name, width, height


def set_layout(fig, width: int, height: int):
    fig.update_layout(
        autosize=False,
        width=width,
        height=height,
        showlegend=False,
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
        margin=dict(l=0, r=0, t=0, b=0),
    )


def draw_line_chart(df: pd.DataFrame, x: pd.DataFrame.columns, y: pd.DataFrame.columns, width: int, height: int) -> px.line():
    if x=='index':x=df.index
    fig = px.line(df, x=x, y=y)
    set_layout(fig, width, height)

    return fig


def draw_bar_chart(df: pd.DataFrame, x: pd.DataFrame.columns, y: pd.DataFrame.columns, width: int, height: int) -> px.bar():
    if x == 'index': x = df.index
    fig = px.bar(df, x=x, y=y)
    set_layout(fig, width, height)

    return fig


def draw_pie_chart(df: pd.DataFrame, value: pd.DataFrame.columns, name: pd.DataFrame.columns, width: int, height: int) -> px.pie():
    fig = px.pie(df, values=value, names=name)
    set_layout(fig, width, height)
    fig.update_layout(showlegend=True,)
    fig.update_traces(textposition='inside', textinfo='percent+label')

    return fig


def render_sidebar(df):
    st.sidebar.header('Custom Chart')

    id_list = {id for id, time in df.index}
    selected_data = st.sidebar.selectbox('select data', id_list)
    st.sidebar.write(f'selected data file : [ {selected_data} ]')

    chart_list = ['line chart', 'bar chart', 'pie chart']
    selected_chart = st.sidebar.selectbox('select chart shape', chart_list)
    st.sidebar.write(f'selected chart shape : [ {selected_chart} ]')

    return selected_data, selected_chart


def render_main_page(df: pd.DataFrame, option: tuple):
    selected_data, selected_chart = option

    if selected_chart == 'line chart':
        x, y, width, height = get_info_bar_and_line_chart(df)
        fig = draw_line_chart(df.loc[f'{selected_data}'], x, y, width, height)
        st.plotly_chart(fig, use_container_width=True)

    elif selected_chart == 'bar chart':
        x, y, width, height = get_info_bar_and_line_chart(df)

        fig = draw_bar_chart(df.loc[f'{selected_data}'], x, y, width, height)
        st.plotly_chart(fig, use_container_width=True)

    elif selected_chart == 'pie chart':
        x, y, width, height = get_info_pie_chart(df)

        fig = draw_pie_chart(df.loc[f'{selected_data}'], x, y, width, height)
        st.plotly_chart(fig, use_container_width=True)


def main():
    df = load_data('testdata.csv')
    option = render_sidebar(df)
    render_main_page(df, option)


if __name__ == '__main__':
    main()
