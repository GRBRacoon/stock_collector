import datetime
import logging


class LogFactory:
    def __init__(self) -> None:
        self.log = logging.getLogger()
        self.log.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.log.addHandler(stream_handler)

        file_name = datetime.datetime.now()
        file_handler = logging.FileHandler(f"{file_name}.log")
        file_handler.setFormatter(formatter)
        self.log.addHandler(file_handler)


# def LogTest():

#     # 로그 생성
#     log = logging.getLogger()

#     # 로그의 레벨
#     log.setLevel(logging.INFO)

#     # log 출력 형식
#     formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
#     stream_handler = logging.StreamHandler()
#     stream_handler.setFormatter(formatter)
#     log.addHandler(stream_handler)

#     # log를 파일에 출력
#     file_name = datetime.datetime.now()
#     file_handler = logging.FileHandler(f"{file_name}.log")
#     file_handler.setFormatter(formatter)
#     log.addHandler(file_handler)

#     for i in range(10):
#         log.info(f"테스트 로그 입니다. {i}")
