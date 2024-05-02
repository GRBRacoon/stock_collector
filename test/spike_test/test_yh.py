from datetime import datetime

from dateutil.relativedelta import relativedelta

# 시작 날짜 설정
start_date = datetime(2023, 1, 1)

# 12개월 동안 매월 출력
for i in range(12):
    print_date = start_date + relativedelta(months=i)
    print(print_date.strftime("%Y-%m-%d"))
