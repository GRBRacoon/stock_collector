import datetime

print(datetime.datetime.now().date())


start_day = datetime.datetime(2022, 4, 19).date()
print(str(start_day))
one_day_later = start_day + datetime.timedelta(days=1)
print(str(one_day_later))
