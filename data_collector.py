import time

import pandas as pd
from pykiwoom.kiwoom import *

SAMSUNG_CODE = "005930"
TICK_VALUE = 1

TIME_REQUEST_CODE = " opt10006"
REAL_TIME_DATA_REQUEST_CODE = "opt10007"
MINUTE_DATA_REQUEST_CODE = "opt10080"

MARKET_CLOSE_TIME = datetime.datetime(year=2023, month=4, day=24, hour=15, minute=0).time()


class DataCollector:
    # def __init__(self, kiwoom) -> None:
    #     kiwoom = kiwoom

    def real_time_data(self, item_code: str):
        kiwoom = Kiwoom()

        dfs = []
        while datetime.datetime.now().time() < MARKET_CLOSE_TIME:
            start_time = time.time()
            df = kiwoom.block_request(REAL_TIME_DATA_REQUEST_CODE, 종목코드=item_code, output="주식일봉차트조회", next=0)
            dfs.append(df)
            elapsed_time = time.time() - start_time  # 경과 시간 계산
            time_to_wait = max(60 - elapsed_time, 0)  # 다음 작업까지 대기할 시간 계산
            time.sleep(time_to_wait)

        today_df = pd.concat(dfs, ignore_index=True)
        today_df = today_df.sort_values(by="시간")

        file_name = f"{item_code}_{datetime.datetime.now().date()}"
        today_df.to_excel(f"{file_name}.xlsx")
