from korea_news_crawler.articlecrawler import ArticleCrawler


def main():
    Crawler = ArticleCrawler()
    Crawler.set_category("경제", "정치", "사회", "IT과학", "세계")
    Crawler.set_date_range("2022-05-01", "2024-05-31")

    Crawler.start()


if __name__ == "__main__":
    from multiprocessing import freeze_support

    freeze_support()
    main()
