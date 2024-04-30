import ctypes
import datetime
import sys
import time as Time

import pandas as pd
import win32com.client
from PyQt5.QtWidgets import *

################################################
# PLUS 공통 OBJECT
g_objCodeMgr = win32com.client.Dispatch("CpUtil.CpCodeMgr")
g_objCpStatus = win32com.client.Dispatch("CpUtil.CpCybos")
g_objCpTrade = win32com.client.Dispatch("CpTrade.CpTdUtil")


################################################
# PLUS 실행 기본 체크 함수
def InitPlusCheck():
    # 프로세스가 관리자 권한으로 실행 여부
    if ctypes.windll.shell32.IsUserAnAdmin():
        print("정상: 관리자권한으로 실행된 프로세스입니다.")
    else:
        print("오류: 일반권한으로 실행됨. 관리자 권한으로 실행해 주세요")
        return False

    # 연결 여부 체크
    if g_objCpStatus.IsConnect == 0:
        print("PLUS가 정상적으로 연결되지 않음. ")
        return False

    # # 주문 관련 초기화
    # if (g_objCpTrade.TradeInit(0) != 0):
    #     print("주문 초기화 실패")
    #     return False

    return True


################################################
# CpEvent: 실시간 이벤트 수신 클래스
class CpEvent:
    def set_params(self, client, name, caller):
        self.client = client  # CP 실시간 통신 object
        self.name = name  # 서비스가 다른 이벤트를 구분하기 위한 이름
        self.caller = caller  # callback 을 위해 보관
        self.last_minute = None

    def OnReceived(self):
        # 실시간 처리 - 현재가 주문 체결
        current_time = datetime.datetime.now().time
        if current_time == datetime.time(15, 30):
            self.caller.create_excel()

        current_minute = datetime.datetime.now().minute
        if self.last_minute == current_minute:
            # 같은 분 내에서는 데이터를 처리하지 않습니다.
            return
        if self.name == "stockcur":
            code = self.client.GetHeaderValue(0)  # 초
            name = self.client.GetHeaderValue(1)  # 초
            time = self.client.GetHeaderValue(18)  # 초
            exFlag = self.client.GetHeaderValue(19)  # 예상체결 플래그
            cprice = self.client.GetHeaderValue(13)  # 현재가
            diff = self.client.GetHeaderValue(2)  # 대비
            cVol = self.client.GetHeaderValue(17)  # 순간체결수량
            vol = self.client.GetHeaderValue(9)  # 거래량

            if exFlag != ord("2"):
                return

            item = {}
            item["종목코드"] = code
            item["시간"] = time

            item["종가"] = cprice

            # 현재가 업데이트
            self.caller.updateCurData(item)

            return


################################################
# plus 실시간 수신 base 클래스
class CpPublish:
    def __init__(self, name, serviceID):
        self.name = name
        self.obj = win32com.client.Dispatch(serviceID)
        self.bIsSB = False

    def Subscribe(self, var, caller):
        if self.bIsSB:
            self.Unsubscribe()

        if len(var) > 0:
            self.obj.SetInputValue(0, var)

        handler = win32com.client.WithEvents(self.obj, CpEvent)
        handler.set_params(self.obj, self.name, caller)
        self.obj.Subscribe()
        self.bIsSB = True

    def Unsubscribe(self):
        if self.bIsSB:
            self.obj.Unsubscribe()
        self.bIsSB = False


################################################
# CpPBStockCur: 실시간 현재가 요청 클래스
class CpPBStockCur(CpPublish):
    def __init__(self):
        super().__init__("stockcur", "DsCbo1.StockCur")


class CMinchartData:
    def __init__(self):
        self.data = pd.DataFrame(columns=["종목코드", "시간", "종가"])
        self.data.set_index(["종목코드"], inplace=True)
        self.objCur = {}
        self.code_list = []

    def stop(self):
        for k, v in self.objCur.items():
            v.Unsubscribe()

    def addCode(self, code):
        # if code not in self.data:
        #     # 각 종목별로 DataFrame을 생성합니다.
        #     self.data[code] = pd.DataFrame(columns=["시간", "시가", "고가", "저가", "종가"])

        # self.data[code] = []
        self.objCur[code] = CpPBStockCur()
        self.objCur[code].Subscribe(code, self)
        self.code_list.append(code)

    def updateCurData(self, item):
        code = item["종목코드"]
        time = item["시간"]
        cur = item["종가"]

        hh, mm = divmod(time, 10000)
        mm, ss = divmod(mm, 100)
        hhmm = hh * 100 + mm

        if hhmm > 1530:
            hhmm = 1530

        index = (code, hhmm)
        # 해당 시간의 데이터가 있는지 확인합니다.

        if index in self.data.index:
            self.data.loc[index, "종가"] = cur  # 종가 업데이트

        else:
            new_row = pd.DataFrame([item], columns=self.data.columns)
            new_row.set_index("종목코드", inplace=True)
            # new_row = pd.Series({"종가": cur}, name=index)
            self.data = pd.concat([self.data, new_row], ignore_index=True)

    def create_excel(self):
        if not self.data.empty:
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            for item_code in self.code_list:
                file_name = f"{item_code}_{today}"
                try:
                    df = self.data.xs(item_code, level="종목코드")  # 멀티인덱스에서 종목코드에 해당하는 데이터 추출
                    df.to_excel(file_name)
                    print(f"파일 저장 성공: {file_name}")
                except Exception as e:
                    print(f"파일 저장 실패: {e}")
            self.data = pd.DataFrame(columns=["종목코드", "시간", "종가"])
            self.data.set_index(["종목코드"], inplace=True)
        else:
            return False

    def printData(self, code):
        if code in self.data.index:
            print(self.data.loc[code])
        else:
            print(f"종목코드 {code}에 대한 데이터가 존재하지 않습니다.")


# print(code, self.minDatas[code])


################################################
# 테스트를 위한 메인 화면
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # plus 상태 체크
        if InitPlusCheck() == False:
            exit()

        self.minData = CMinchartData()

        # 코스피 200 종목 가져와 추가
        self.codelist = []
        self.codelist.append("A005930")
        for code in self.codelist:
            print(code, g_objCodeMgr.CodeToName(code))
            self.minData.addCode(code)

        self.setWindowTitle("주식 분 차트 생성")
        self.setGeometry(300, 300, 300, 180)

        nH = 20

        btnPrint = QPushButton("print", self)
        btnPrint.move(20, nH)
        btnPrint.clicked.connect(self.btnPrint_clicked)
        nH += 50

        btnExit = QPushButton("종료", self)
        btnExit.move(20, nH)
        btnExit.clicked.connect(self.btnExit_clicked)
        nH += 50

    def btnPrint_clicked(self):
        for i in range(len(self.codelist)):
            self.minData.printData(self.codelist[i])
            if i > 10:
                break
        return

    def btnExit_clicked(self):
        self.minData.stop()
        exit()
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
