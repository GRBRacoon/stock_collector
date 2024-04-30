import datetime

import pandas as pd
import win32com.client

DAY_MIN_DATA_SIZE = 155710
instStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

# 초기 설정
instStockChart.SetInputValue(0, "A005930")  # 종목코드
instStockChart.SetInputValue(1, ord("2"))  # 기간으로 요청
instStockChart.SetInputValue(4, DAY_MIN_DATA_SIZE)  # 요청개수
instStockChart.SetInputValue(5, (0, 1, 3))  # 날짜, 시간, 시가, 종가
instStockChart.SetInputValue(6, ord("m"))  # 차트 종류 (분봉)
instStockChart.SetInputValue(9, ord("1"))  # 수정 주가

# 데이터 수집을 위한 빈 리스트
data_list = []

# 데이터 요청 및 수집
moreData = True
while moreData:
    instStockChart.BlockRequest()
    numData = instStockChart.GetHeaderValue(3)
    numField = instStockChart.GetHeaderValue(1)

    # 데이터 수집
    for i in range(numData):
        row_data = []
        for j in range(numField):
            row_data.append(instStockChart.GetDataValue(j, i))
        data_list.append(row_data)

    # 연속 데이터 요청 여부 확인
    moreData = instStockChart.Continue

# DataFrame 생성
columns = ["Date", "Time", "Close"]  # 적절한 컬럼 이름 설정
df = pd.DataFrame(data_list, columns=columns)
file_name = "minute_chart_data_20220419_20240429"
# DataFrame 확인
print(df)
df.to_excel(f"{file_name}.xlsx")
