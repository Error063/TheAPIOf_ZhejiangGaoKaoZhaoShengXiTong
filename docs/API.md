注：部分信息已经过脱敏处理

# pgzy

[示例文件](../getInfos.py)

主链接：https://pgzy.zjzs.net:4431/

 

## 1.  验证码

URL：https://pgzy.zjzs.net:4431/INC/VerifyCode.aspx

请求：GET

需要cookie：否

返回信息：图片（带有验证码），Cookie（ASP.NET_SessionId）

注：完成登录操作时需附上该Cookie信息

## 2.  登录

URL：https://pgzy.zjzs.net:4431/ashx/loginHandler.ashx

请求：POST

需要cookie：是

请求参数：

| 字段           | 内容                 | 数据类型 | 例                    | 备注                |
| -------------- | -------------------- | -------- | --------------------- | ------------------- |
| "title"        | 请求操作             | 字符串   | "login"               |                     |
| "shenfenzheng" | 用户身份证           | 字符串   | “1145141191908102424” |                     |
| "mima"         | 用户密码（需要加密） | 字符串   |                       | 需要使用MD5进行加密 |
| "yzm"          | 验证码               | 字符串   |                       |                     |
| "isadmin"      | 是否为管理员         | 布尔     | False                 |                     |

返回信息：JSON（详见下），Cookie（usersfz和appid）

| 字段     | 内容                   | 数据类型 | 例                     | 备注             |
| -------- | ---------------------- | -------- | ---------------------- | ---------------- |
| "status" | 返回状态               | 字符串   | "success"  \| "failed" | 成功 \| 失败     |
| "des"    | 结果信息（提供给用户） | 字符串   | "登录成功！"           | 见下（1）        |
| “url”    | 重定向页面             | 字符串   | "default.aspx"         | 如果失败则不显示 |

（1）可能出现的错误信息：

1. 证件号或密码输入错误！
2. 验证码输入错误！
3. 请勿输入非法字符!

etc.

注：

1. 完成登录操作时需附上从验证码处获取的Cookie信息（ASP.NET_SessionId）
2. 接下来的所有操作均需附上ASP.NET_SessionId、usersfz和appid的Cookie信息

## 3. 获取考生证件照图片

URL：https://pgzy.zjzs.net:4431/ashx/ajaxHandler.ashx

请求：POST

需要cookie：是

| 字段    | 内容     | 数据类型 | 例         | 备注 |
| ------- | -------- | -------- | ---------- | ---- |
| "title" | 请求操作 | 字符串   | “getkspic” |      |

返回信息：文本，图片的相对URL链接，如：

xnml/pic/savepic/1\*\*8\*/0\*\*81/\*s\*s\*/\*\*57\*\*0y\*\*\*9\*\*\*9\*\*.jpg

需要拼接完整，如：

https://pgzy.zjzs.net:4431/xnml/pic/savepic/1\*\*8\*/0\*\*81/\*s\*s\*/\*\*57\*\*0y\*\*\*9\*\*\*9\*\*.jpg

 

## 4. 获取考生基本信息

URL：https://pgzy.zjzs.net:4431/ashx/ajaxHandler.ashx

请求：POST

需要cookie：是

| 字段    | 内容     | 数据类型 | 例            | 备注 |
| ------- | -------- | -------- | ------------- | ---- |
| "title" | 请求操作 | 字符串   | “getbasedata” |      |

返回信息：JSON（详见下）

| 字段 | 内容 | 数据类型 | 例   | 备注 |
| ---- | ---- | -------- | ---- | ---- |
| NAME | 姓名 | 字符串 | 田所浩二 | |
| SHENFENZHENG | 身份证 | 字符串 | 1145141191908102424 | |
| XINGBIE | 性别 | 字符串 | 男 | |
| MINZU | 民族 | 字符串 | 大和 | |
| HUJI | 户籍 | 字符串 | 1145141 | 身份证开头前七位 |
| PHONE | 电话号码 | 字符串 | 19198101145 | |
| MMCZZT | ? | 整型 | 0 | |
| CSRQ | 出生日期 | 字符串 | 19190810 | |
| ZJLX | ? | 字符串 | "1" | |
| RXSJ | 入学年份 | 字符串 | 1919 | |
| XXSZXQ | 入学地区? | 整型 | 24 | |
| SHZT | ? | 整型 | 0 | |
| ZHMMCOUNT | ? | 整型 | 9 | |
| SFZH_YZ | ? | 整型 | 1 | |
| LAST_LOG_FALSE_TIME | ？ | 整型 | 0 | |
| LAST_LOG_FALSE_COUNT | ？ | 字符串（日期？） | "2000/1/1 0:00:00" | |
| ZJLX_OLD | ？ | 整型 | 0 | |
| SFYZ_GJRKK | ？ | 整型 | 1 | |
| ZPYZZT | ？ | 整型 | 1 | |
| ZPYZJG | ？ | 字符串 | "成功" | |
| LOGIN_TIME | ？ | 字符串（日期？） | "2000/1/1 0:00:00" | |

## 5.获取考生成绩（包括学考和选考）

URL：https://pgzy.zjzs.net:4431/xklscj.aspx

请求：GET

需要cookie：是

返回信息：HTML

## 6.获取考生准考证pdf文档

URL：https://pgzy.zjzs.net:4431/xnml/{考试类别}/xszkz/gkzkz_{appid}.pdf

https://pgzy.zjzs.net:4431/xnml/gk202301/xszkz/gkzkz_00000000000000000.pdf

请求：GET

需要cookie：否

返回信息：文件（pdf）

## 7.获取浙江省的所有地级市信息

URL：https://pgzy.zjzs.net:4431/ashx/ajaxHandler.ashx

请求：POST

需要cookie：是

| 字段    | 内容     | 数据类型 | 例      | 备注 |
| ------- | -------- | -------- | ------- | ---- |
| "title" | 请求操作 | 字符串   | “getds” |      |

返回信息：HTML

```html
<option value='1'>杭州市</option>
<option value='2'>宁波市</option>
<option value='3'>温州市</option>
<option value='4'>嘉兴市</option>
<option value='5'>湖州市</option>
<option value='6'>绍兴市</option>
<option value='7'>金华市</option>
<option value='8'>衢州市</option>
<option value='9'>丽水市</option>
<option value='10'>台州市</option>
<option value='11'>舟山市</option>

```



# cx

[示例文件](../getscores.py)

主链接：https://cx.zjzs.net/exam/<考试ID>/default.htm

考试ID 例如：GKCX2023YCKDASHDKIUWQJBCZLGDV(2023年6月高考)

 

## 1.  验证码

## 2.  登录

URL：https://cx.zjzs.net/exam/<考试ID>/ resault.aspx

请求：POST

请求参数：

| 字段       | 内容     | 数据类型 | 例               | 备注         |
| ---------- | -------- | -------- | ---------------- | ------------ |
| "ZKZH"     | 准考证号 | 字符串   | "11451419198100" |              |
| "PASSWORD" | 密码     | 字符串   |                  | 与pgzy处相同 |
| "yzm"      | 验证码   | 字符串   |                  |              |

 

返回信息：HTML





~~这变量写的真tm乱~~
