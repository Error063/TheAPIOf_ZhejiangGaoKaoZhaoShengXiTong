import json
import pprint

import ddddocr
import requests
from bs4 import BeautifulSoup

# 浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": 'application/x-www-form-urlencoded',
    "Cookie": "",
}
# 初始化验证码ocr
ocr = ddddocr.DdddOcr()
# 禁用警告
requests.packages.urllib3.disable_warnings()
# 准考证号
_ZKZH = "YOUR_EXAM_NUMBER"
# 密码
_PASSWORD = "YOUR_PASSWORD"

# 初始化请求会话
req = requests.session()

# 获取验证码
cap_raw = req.get("https://cx.zjzs.net/INC/VerifyCode.aspx", verify=False, headers=headers)
# 将验证码的cookie信息添加到请求头中
headers['Cookie'] += f"{cap_raw.cookies.items()[0][0]}={cap_raw.cookies.items()[0][1]};"
# 识别验证码
cap = ocr.classification(cap_raw.content)

# 登录信息
login_info = {"ZKZH": _ZKZH, "PASSWORD": _PASSWORD, "yzm": cap}
# 将登录信息和请求头上传到服务器中
login = req.post("https://cx.zjzs.net/exam/GKCX2023YCKDASHDKIUWQJBCZLGDV/resault.aspx", data=login_info, verify=False,
                 headers=headers)
# 解码返回的HTML页面
result = login.content.decode("utf8")

# 初始化BeautifulSoup
soup = BeautifulSoup(result, "html5lib")
scores = {
    "info": {  # 考生信息
        "name": str(soup.find(id='XM').text),  # 考生姓名
        "exam_number": str(soup.find(id='ZKZH').text)  # 准考证号
    },
    "main": {  # 主科目成绩
        "语文": int(soup.find(id='KM1').text),
        "数学": int(soup.find(id='KM2').text),
        "外语": int(soup.find(id='KM3').text)  # 此为外语最终成绩
    },
    "selected_end": {  # 选考最终成绩
        str(soup.find(id='KM4MC').text): int(soup.find(id='KM4').text),
        str(soup.find(id='KM5MC').text): int(soup.find(id='KM5').text),
        str(soup.find(id='KM6MC').text): int(soup.find(id='KM6').text),
    },
    "selected_now": {  # 选考（包括外语）当次成绩（2023年6月）
        "外语": int(soup.find(id='BCWYCJ').text),
        str(soup.find(id='KM4MC').text): int(soup.find(id='KM4CJ').text),
        str(soup.find(id='KM5MC').text): int(soup.find(id='KM5CJ').text),
        str(soup.find(id='KM6MC').text): int(soup.find(id='KM6CJ').text),
    },
    "total": int(soup.find(id='TOT').text),  # 总分
    "rank_number": str(soup.find(id='TOTMCH').text),  # 总分位次号
    "note": str(soup.find(id='BZ').text)  # 备注
}
# pprint.pprint(scores)
with open(f"result_{str(soup.find(id='XM').text)}.json", mode='wb') as f:
    tmp = json.dumps(obj=scores, ensure_ascii=False).encode("utf8")
    f.write(tmp)
