import json
import pprint

import ddddocr
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": 'application/x-www-form-urlencoded',
    "Cookie": "",
}
ocr = ddddocr.DdddOcr()
requests.packages.urllib3.disable_warnings()
_MainURL = "https://cx.zjzs.net/exam/GKCX2023YCKDASHDKIUWQJBCZLGDV/"
_ZKZH = "YOUR_EXAM_NUMBER"
_PASSWORD = "YOUR_PASSWORD"

req = requests.session()

cap_raw = req.get("https://cx.zjzs.net/INC/VerifyCode.aspx", verify=False, headers=headers)
headers['Cookie'] += f"{cap_raw.cookies.items()[0][0]}={cap_raw.cookies.items()[0][1]};"
cap = ocr.classification(cap_raw.content)

login_info = {"ZKZH": _ZKZH, "PASSWORD": _PASSWORD, "yzm": cap}
login = req.post("https://cx.zjzs.net/exam/GKCX2023YCKDASHDKIUWQJBCZLGDV/resault.aspx", data=login_info, verify=False,
                 headers=headers)
result = login.content.decode("utf8")

soup = BeautifulSoup(result, "html5lib")
scores = {
    "info": {
        "name": str(soup.find(id='XM').text),
        "exam_number": str(soup.find(id='ZKZH').text)
    },
    "main": {
        "语文": int(soup.find(id='KM1').text),
        "数学": int(soup.find(id='KM2').text),
        "外语": int(soup.find(id='KM3').text)
    },
    "selected_end": {
        str(soup.find(id='KM4MC').text): int(soup.find(id='KM4').text),
        str(soup.find(id='KM5MC').text): int(soup.find(id='KM5').text),
        str(soup.find(id='KM6MC').text): int(soup.find(id='KM6').text),
    },
    "selected_now": {
        "外语": int(soup.find(id='BCWYCJ').text),
        str(soup.find(id='KM4MC').text): int(soup.find(id='KM4CJ').text),
        str(soup.find(id='KM5MC').text): int(soup.find(id='KM5CJ').text),
        str(soup.find(id='KM6MC').text): int(soup.find(id='KM6CJ').text),
    },
    "total": int(soup.find(id='TOT').text),
    "rank_number": str(soup.find(id='TOTMCH').text),
    "note": str(soup.find(id='BZ').text)
}
pprint.pprint(scores)
with open(f"result_{str(soup.find(id='XM').text)}.json", mode='wb') as f:
    tmp = json.dumps(obj=scores, ensure_ascii=False).encode("utf8")
    f.write(tmp)
