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
