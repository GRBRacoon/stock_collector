import os
import sys
import urllib.request

import pandas as pd

client_id = "um1bgVzc2ip6qTDUnixZ"
client_secret = "VAVAzQL2Tw"

encText = urllib.parse.quote("미국증시")

encText2 = urllib.parse.quote("100")


url = "https://openapi.naver.com/v1/search/news.json?query=" + encText + "&display=" + encText2  # JSON 결과
print(url)
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id", client_id)
request.add_header("X-Naver-Client-Secret", client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if rescode == 200:
    response_body = response.read()
    print(response_body.decode("utf-8"))
else:
    print("Error Code:" + rescode)

import json

data = json.loads(response_body.decode("utf-8"))
data["items"]

df = pd.DataFrame(data["items"])
df.to_excel("data.xlsx")
