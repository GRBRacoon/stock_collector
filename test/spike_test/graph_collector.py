import sys

from PyQt5.QAxContainer import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Kiwoom(QAxWidget):
    def __init__(self):
        super().__init__()
        print("[Kiwoom] Open API start....")

        # QEventLoop 클래스 저장
        self.login_event_loop = QEventLoop()

        self.getOCXInstance()  # OCX to Python
        self.eventSlots()  # Signal Slot
        self.signalLoginCommConnect()  # 로그인 요청 함수

    def getOCXInstance(self):
        # 키움 OpenAPI API 호출
        self.setControl("KHOPENAPI.KHOpenAPICtrl.1")

    def eventSlots(self):
        # 로그인 관련 이벤트 연결
        self.OnEventConnect.connect(self.loginSlot)

    def signalLoginCommConnect(self):
        # 로그인 요청 시그널
        self.dynamicCall("CommConnect()")
        # 이벤트 루프 실행
        self.login_event_loop.exec_()

    def loginSlot(self, err_code):
        if err_code == 0:
            print("[Kiwoom] Open API Connected.")
        else:
            print("[Kiwoom] Open API is not connect.")

        self.login_event_loop.exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    kiwoom = Kiwoom()
