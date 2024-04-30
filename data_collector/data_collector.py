import datetime

import pandas as pd
import win32com.client

from utils.enum.item_code import ItemCode

MAX_MIN_DATA_SIZE = 155710


class DataCollector:
    def collect_minute_data_two_year(self, item_code: ItemCode):
        inst_stock_chart = win32com.client.Dispatch("CpSysDib.StockChart")
        inst_stock_chart.SetInputValue(0, item_code)  # 종목코드
        inst_stock_chart.SetInputValue(1, ord("2"))  # 기간으로 요청
        inst_stock_chart.SetInputValue(4, MAX_MIN_DATA_SIZE)  # 요청개수
        inst_stock_chart.SetInputValue(5, (0, 1, 3))  # 날짜, 시간, 시가, 종가
        inst_stock_chart.SetInputValue(6, ord("m"))  # 차트 종류 (분봉)
        inst_stock_chart.SetInputValue(9, ord("1"))  # 수정 주가

        data_list = []

        more_data = True
        while more_data:
            inst_stock_chart.BlockRequest()
            num_data = inst_stock_chart.GetHeaderValue(3)
            num_field = inst_stock_chart.GetHeaderValue(1)

            # 데이터 수집
            for i in range(num_data):
                row_data = []
                for j in range(num_field):
                    row_data.append(inst_stock_chart.GetDataValue(j, i))
                data_list.append(row_data)

            # 연속 데이터 요청 여부 확인
            more_data = inst_stock_chart.Continue

        # DataFrame 생성
        columns = ["Date", "Time", "Close"]  # 적절한 컬럼 이름 설정
        df = pd.DataFrame(data_list, columns=columns)
        start_date = df["Date"].iloc[0]
        end_date = df["Date"].iloc[-1]
        file_name = f"data/{item_code}/{item_code}_min_chart_{start_date}_{end_date}"
        # DataFrame 확인

        df.to_excel(f"{file_name}.xlsx")

    def append_minute_data(self, item_code: ItemCode):
        inst_stock_chart = win32com.client.Dispatch("CpSysDib.StockChart")
        inst_stock_chart.SetInputValue(0, item_code)  # 종목코드
        inst_stock_chart.SetInputValue(1, ord("2"))  # 기간으로 요청
        inst_stock_chart.SetInputValue(4, 1)  # 요청개수
        inst_stock_chart.SetInputValue(5, (0, 1, 3))  # 날짜, 시간, 시가, 종가
        inst_stock_chart.SetInputValue(6, ord("m"))  # 차트 종류 (분봉)
        inst_stock_chart.SetInputValue(9, ord("1"))  # 수정 주가

        data_list = []

        more_data = True
        while more_data:
            inst_stock_chart.BlockRequest()
            num_data = inst_stock_chart.GetHeaderValue(3)
            num_field = inst_stock_chart.GetHeaderValue(1)

            # 데이터 수집
            for i in range(num_data):
                row_data = []
                for j in range(num_field):
                    row_data.append(inst_stock_chart.GetDataValue(j, i))
                data_list.append(row_data)

            # 연속 데이터 요청 여부 확인
            more_data = inst_stock_chart.Continue

        # DataFrame 생성
        columns = ["Date", "Time", "Close"]  # 적절한 컬럼 이름 설정
        df = pd.DataFrame(data_list, columns=columns)

        today = df["Date"].iloc[-1]
        file_name = f"data/{item_code}_daily/{item_code}_min_chart_{today}"
        df.to_excel(f"{file_name}.xlsx")
