import hashlib
import requests
import ddddocr

_Id = "YOUR_ID_NUMBER"
_Pwd = "YOUR_PASSWORD"
_MainURL = "https://pgzy.zjzs.net:4431/"

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

req = requests.session()
cap = req.get(f"{_MainURL}INC/VerifyCode.aspx", verify=False, headers=headers)
headers['Cookie'] += f"{cap.cookies.items()[0][0]}={cap.cookies.items()[0][1]};"
res = ocr.classification(cap.content)
data = {"title": "login", "shenfenzheng": _Id, "mima": str(hashlib.md5(_Pwd.encode("utf-8")).hexdigest()), "yzm": res,
        "isadmin": False}
login = req.post(f"{_MainURL}ashx/loginHandler.ashx", verify=False, data=data, headers=headers)
print(login.cookies.items())
for cookie in login.cookies.items():
    headers['Cookie'] += f"{cookie[0]}={cookie[1]};"
print(login.content.decode("utf8"))
pic_url = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getkspic" }, headers=headers)
pic = req.get(f"{_MainURL}{pic_url.content.decode('utf8')}", verify=False, headers=headers)
print(f"{_MainURL}{pic_url.content.decode('utf8')}")
with open("./exp.jpg", mode='wb') as f:
    f.write(pic.content)
basedata_raw = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getbasedata" }, headers=headers)
print(basedata_raw.content.decode("utf8"))
r = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getdsbyxq", "xq": 54}, headers=headers)
print(r.content.decode("utf8"))
r = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getxqbyxq", "xq": 54, "dq": int(r.content.decode("utf8"))}, headers=headers)
print(r.content.decode("utf8"))
