import hashlib
import requests
import ddddocr

_Id = "YOUR_ID_NUMBER"  # 身份证号
_Pwd = "YOUR_PASSWORD"  # 密码
_MainURL = "https://pgzy.zjzs.net:4431/"  # 主链接

# 浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Content-Type": 'application/x-www-form-urlencoded',
    "Cookie": "",
}
ocr = ddddocr.DdddOcr()  # 初始化验证码ocr
requests.packages.urllib3.disable_warnings()  # 禁用警告

# 登录开始
req = requests.session()  # 初始化请求会话

cap = req.get(f"{_MainURL}INC/VerifyCode.aspx", verify=False, headers=headers)  # 获取验证码
headers['Cookie'] += f"{cap.cookies.items()[0][0]}={cap.cookies.items()[0][1]};"  # 将验证码的cookie信息添加到请求头中
res = ocr.classification(cap.content)  # 识别验证码
data = {"title": "login", "shenfenzheng": _Id, "mima": str(hashlib.md5(_Pwd.encode("utf-8")).hexdigest()), "yzm": res,
        "isadmin": False}  # 登录信息
login = req.post(f"{_MainURL}ashx/loginHandler.ashx", verify=False, data=data, headers=headers)  # 将登录信息和请求头上传到服务器中
print(login.cookies.items())
for cookie in login.cookies.items():  # 将获取到的cookie信息依次添加到请求头
    headers['Cookie'] += f"{cookie[0]}={cookie[1]};"
print(login.content.decode("utf8"))
# 登录结束

pic_url = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getkspic" }, headers=headers)  # 获取考生证件照图片URL链接
pic = req.get(f"{_MainURL}{pic_url.content.decode('utf8')}", verify=False, headers=headers)  # 获取考生证件照图片
with open("./exp.jpg", mode='wb') as f:  # 保存图片
    f.write(pic.content)
basedata_raw = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getbasedata" }, headers=headers)  # 获取考生基本信息
print(basedata_raw.content.decode("utf8"))
r = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getdsbyxq", "xq": 54}, headers=headers)
print(r.content.decode("utf8"))
r = req.post(f"{_MainURL}ashx/ajaxHandler.ashx", verify=False, data={ "title": "getxqbyxq", "xq": 54, "dq": int(r.content.decode("utf8"))}, headers=headers)
print(r.content.decode("utf8"))
