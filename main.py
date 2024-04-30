import ctypes
import sys

import win32com.client
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

################################################
# PLUS 공통 OBJECT 초기화
g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
g_objCpStatus = win32com.client.Dispatch("CpUtil.CpCybos")
g_objCpTrade = win32com.client.Dispatch("CpTrade.CpTdUtil")


################################################
# PLUS 실행 기본 체크 함수
def InitPlusCheck():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        print("오류: 관리자 권한으로 실행해 주세요.")
        return False

    if g_objCpStatus.IsConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음.")
        return False

    return True


################################################
# 주식 실시간 수신 클래스
class CpStockCur:
    def __init__(self):
        self.obj = win32com.client.Dispatch("DsCbo1.StockCur")

    def Subscribe(self, code):
        if not self.obj.GetDibStatus() == 0:
            print("통신상태가 비정상입니다.")
            return False

        self.obj.SetInputValue(0, code)
        handler = win32com.client.WithEvents(self.obj, CpEvent)
        self.obj.Subscribe()
        print(f"{code}에 대한 실시간 데이터 수신을 시작합니다.")
        return True

    def Unsubscribe(self):
        self.obj.Unsubscribe()


################################################
# 실시간 이벤트 수신 처리 클래스
class CpEvent:
    def OnReceived(self):
        code = self.client.GetHeaderValue(0)
        name = g_objCodeMgr.CodeToName(code)
        time = self.client.GetHeaderValue(1)
        price = self.client.GetHeaderValue(13)
        print(f"시간: {time}, 종목명: {name}, 현재가: {price}")


################################################
# 메인 화면 클래스
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        if not InitPlusCheck():
            exit()

        self.setWindowTitle("실시간 주식 데이터 수신")
        self.setGeometry(300, 300, 400, 300)

        self.stockCur = CpStockCur()

        btnStart = QPushButton("데이터 수신 시작", self)
        btnStart.move(20, 20)
        btnStart.clicked.connect(self.btnStart_clicked)

        btnStop = QPushButton("종료", self)
        btnStop.move(20, 70)
        btnStop.clicked.connect(self.btnExit_clicked)

    def btnStart_clicked(self):
        code = input("종목 코드를 입력하세요: ")
        self.stockCur.Subscribe(code)

    def btnExit_clicked(self):
        self.stockCur.Unsubscribe()
        print("데이터 수신을 중단하고 프로그램을 종료합니다.")
        exit()


################################################
# 프로그램 실행
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
