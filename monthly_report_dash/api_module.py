import requests
import pandas as pd
import time
import datetime


def rawdata(time_from, time_to):
    api_endpoint1 = 'https://kdwyu8tywb.execute-api.ap-northeast-2.amazonaws.com/default/cushion_report_api'
    api_endpoint2 = 'https://c5nidsaeoh.execute-api.ap-northeast-2.amazonaws.com/default/ingkle-an2-api-base-swhitech'
    r = requests.get(api_endpoint1 + f'?type=raw_data&time_from={time_from}&time_to={time_to}')
    try:
        data = pd.DataFrame(r.json()["values"], columns = r.json()["fields"])
        return data
    except:
        print("데이터 다운로드 실패")
        data = pd.DataFrame()
        return data


def operation(time_from):
    api_endpoint1 = 'https://kdwyu8tywb.execute-api.ap-northeast-2.amazonaws.com/default/cushion_report_api'
    api_endpoint2 = 'https://c5nidsaeoh.execute-api.ap-northeast-2.amazonaws.com/default/ingkle-an2-api-base-swhitech'
    r = requests.get(api_endpoint1 + f'?type=all&time_from={time_from}&time_to={(time_from + 60 * 60)}')
    try:
        data = pd.DataFrame(r.json()["values"], columns=r.json()["fields"])
        return data
    except:
        print("데이터 다운로드 실패")
        data = pd.DataFrame()
        return data


def min_data(time_from):
    api_endpoint1 = 'https://kdwyu8tywb.execute-api.ap-northeast-2.amazonaws.com/default/cushion_report_api'
    api_endpoint2 = 'https://c5nidsaeoh.execute-api.ap-northeast-2.amazonaws.com/default/ingkle-an2-api-base-swhitech'
    r = requests.get(api_endpoint2 + f'?type=mindex&time_from={time_from}&time_to={time_from + 60*60}')
    try:
        data = pd.DataFrame(r.json()["values"], columns = r.json()["fields"])
        data['sumData'] = data["cycleIndex"]+data["contiIndex"]
        return data
    except:
        print("데이터 다운로드 실패")
        data = pd.DataFrame()
        return data


if __name__ == "__main__":
    pass
