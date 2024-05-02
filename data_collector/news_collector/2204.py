import datetime

from korea_news_crawler.articlecrawler import ArticleCrawler

START_DAY = datetime.datetime(2022, 4, 19).date()
END_DAY = datetime.datetime(2024, 4, 30).date()


def main():
    today = START_DAY
    Crawler = ArticleCrawler()
    Crawler.set_category("경제", "정치", "사회", "IT과학", "세계")
    while today != END_DAY:
        Crawler.set_date_range(str(today), str(today))
        Crawler.start()
        today = today + datetime.timedelta(days=1)


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    main()
