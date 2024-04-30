import time

import pandas as pd
from pykiwoom.kiwoom import *

# login
kiwoom = Kiwoom()  # allocation
print("login..")
kiwoom.CommConnect(block=True)  # waiting to login
print("login..complete")

# connect
state = kiwoom.GetConnectState()
if state == 0:
    print("not connected")
elif state == 1:
    print("status : connected")

# login - information
account_num = kiwoom.GetLoginInfo("ACCOUNT_CNT")  # number of account
accounts = kiwoom.GetLoginInfo("ACCNO")  # list of account
user_id = kiwoom.GetLoginInfo("USER_ID")  # user id
user_name = kiwoom.GetLoginInfo("USER_NAME")  # user name
print("number of account : {}".format(account_num))
# print('acounts : {}'.format(accounts))
# print('user id : {}'.format(user_id))
# print('user name : {}'.format(user_name))
