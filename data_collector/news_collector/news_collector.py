import datetime
import time

from dateutil.relativedelta import relativedelta
from korea_news_crawler.articlecrawler import ArticleCrawler

START_DAY = datetime.datetime(2022, 4, 1).date()
END_DAY = datetime.datetime(2022, 12, 31).date()


def main():
    today = START_DAY
    Crawler = ArticleCrawler()
    Crawler.set_category("경제", "정치", "사회", "IT과학", "세계")
    # while today + datetime.timedelta(days=1) != END_DAY:
    #     next_day = today + relativedelta(months=1) - datetime.timedelta(days=1)
    #     Crawler.set_date_range(str(today), str(next_day))
    #     Crawler.start()
    #     today = next_day + datetime.timedelta(days=1)
    #     time.sleep(10)

    Crawler.set_date_range(str(START_DAY), str(END_DAY))
    Crawler.start()


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    main()
