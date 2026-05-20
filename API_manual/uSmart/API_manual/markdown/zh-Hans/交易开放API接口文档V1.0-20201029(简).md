# 交易开放API接口文档V1.0-20201029(简)

- 来源 PDF：`../交易開放API接口文檔V1.0-20201029(繁).pdf`
- 页数：97
- 转换说明：自动文本抽取，保留页码分隔；接口字段、表格和示例代码请与原 PDF 交叉核对。

---

## 第 1 页

交易开放 API 接口文档
V 1 . 0

概述

开放平台可以为个人开发者和机构客户提供接口服务，投资者可以充分的利用盈立智
投的交易服务、报价服务、账户服务等实现自己的投资操作。

接入说明：

IP 白名单，授权访问开放平台接口的 IP 地址，只有在白名单内的 IP 才能访问服务。

协议：

HTTPS

X-Sign

使用 MD5withRSA 加密算法对 Body 中的内容进行加密，得到的密文经过 safeBase64 编码
后作为 X-Sign 的值放入 header 当中，每一个渠道单独分配公私密密钥。

验签测试公开密钥为：

需双方商定

隱私资料加密测试公开密钥为：

需双方商定

URLSAFE_BASE64 算法在 RFC4648 中有定义

最终串會使用 RSA 私密密钥进行加密，之后使用 RFC4648 算法编码放入请求體或表
单項中。

请求頭 X-Request-Id:

---

## 第 2 页

长度为 19 位元数位，必須确保唯一用于做冪等防重，推薦使用分散式 Snowflake 雪花算法
生成。

请求示例：

http header 参数示例

Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiNGZjYTA1MWNmZjQ
wNDI4NzlkNGJiYzYzYjFiYWE0MTgiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozMTgxNDA2MTEwNTc1NTc1MD
R9.gw4_AKh6NGUxWXWjzHb8G2An3ao0nSuI
Content-Type: application/json; charset=utf-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 92823918712371
X-Type: 1
X-Channel：1001
x-Sign：用私密密钥对 body 内容加密后的内容

http body 参数示例：

返回示例：

{

"entrustAmount": 100,

"entrustPrice": 330.4,
"entrustProp": "e",
"entrustType": 0,
"exchangeType": 0,

"stockCode": "00700",

"stockName": "腾讯控股",
"conId": 100008234979823
}

{

"code": 0,

"data": {

---

## 第 3 页

1 用户

1.1 渠道密码登录
手机+密码+渠道登录：

接口地址 /user-server/open-api/login

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

请求参数说明：

参数名称  说明  请求类型  必填  类型

X-Lang

語言类别(1-简體，2-繁體，
3-English)

header

true

string

X-Request-Id

頭部信息的  requestId 信息,长
度 30 位，确保唯一，防止重
複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

签名

header

true

string

areaCode

区域號 86 中國， 852 香港，
853 中國澳門，  886 中國 台
灣，65 新加坡

body

true

string

password

密码 RSA 加密（与 X-Sign 不
同秘钥）

body

true

string
"entrustId": "56765633083899904",

"status": 0,
"statusName": "等待提交"
},

"msg": ""

}

---

## 第 4 页

phoneNumber

手机號 RSA 加密（与 X-Sign
不同秘钥）

body

true

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例：

{
"areaCode": 86, "password":
"rsa", "phoneNumber": "rsa"
}

参数说明：

参数名称  说明  类型
areaCode  区號  string
avatar  頭像地址  string
expiration  过期时间  int64
extendStatusBit  用户擴展状态  int32
firstLogin  是否为第一次登陸  boolean
nickname  昵称  string
openedAccount  是否开户  boolean
phoneNumber  手机號  string
thirdBindBit  綁定位 手机 1<<0 微信 1<<1 微博 1<<2  int32
token  登录授权的 token  string
tradePassword  是否设置过交易密码  boolean
unionId  微信公眾平台的 unionId，如果有则顯示。  string
uuid  盈立用户注冊的 uuid，全域唯一  int64

返回示例：

---

## 第 5 页

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登录密码 1<<1 行情許可权 1<<2 衍生品", "firstLogin": true,
"nickname": "xxx", "openedAccount":
true, "phoneNumber": "188xxxx9188",
"thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回应状态

状态码  说明
0  成功
200  OK
300100  非法请求
300102  账户被冻结，无法完成操作，如非本人操作，请联繫客服
300103  用户被刪除
300309  请輸入正确的手机號码
300701  該手机號沒有注冊
300702  密码错误次数过多账號已鎖定，请%s 分鐘后重新登录或找回密码
300703  密码错误，请重新輸入，您還可以嘗试%s 次
300705  該账户未设置登录密码，请使用短信验证码登录
300809  需要校验手机短信验证码
1.2 获取手机验证码
接口地址 /user-server/open-api/send-phone-captcha

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

请求参数说明：

参数名称  说明  请求类型  必填  类型

X-Lang

語言类别(1-简體，2-繁體，
3-English)

header

true

string

---

## 第 6 页

X-Request-Id

頭部信息的  requestId 信息,长
度 30 位，确保唯一，防止重
複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

签名

header

true

string

areaCode

区域號 86 中國， 852 香港，
853 中國澳門，  886 中國臺
灣，65 新加坡

body

true

string

type

验证码类型 101 注冊 102 重置
密码 103 更换手机號 104 綁定
手机號  105 新设備登录 校验
106 短信登录

body

true

string

phoneNumber

手机號 RSA 加密（与 X-Sign
不同秘钥）

body

true

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例：

{
"areaCode": 86,
"type": 102,
"phoneNumber": "rsa"
}

---

## 第 7 页

出参说明：

参数名称  说明  类型
areaCode  区號  string
avatar  頭像地址  string
expiration  过期时间  int64
extendStatusBit  用户擴展状态  int32
firstLogin  是否为第一次登陸  boolean
invitationCode  邀请码，如果有，则顯示。  string
languageCn  1 简體 2 繁體  int32
languageHk  1 简體 2 繁體  int32
lineColorHk  1 紅漲綠跌 2 綠漲紅跌  int32
nickname  昵称  string
openedAccount  是否开户  boolean
phoneNumber  手机號  string
thirdBindBit  綁定位 手机 1<<0 微信 1<<1 微博 1<<2  int32
token  登录授权的 token  string
tradePassword  是否设置过交易密码  boolean
unionId  微信公眾平台的 unionId，如果有则顯示。  string
uuid  盈立用户注冊的 uuid，全域唯一  int64

返回示例：

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登录密码 1<<1 行情許可权 1<<2 衍生品", "firstLogin": true,
"invitationCode": 1234,
"languageCn": 0,
"languageHk": 0,
"lineColorHk":  0, "nickname": "xxx",
"openedAccount": true, "phoneNumber":
"188xxxx9188", "thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回应状态

状态码  说明
0  成功

---

## 第 8 页

200  OK
300100  非法请求
300102  账户被冻结，无法完成操作，如非本人操作，请联繫客服
300103  用户被刪除
300309  请輸入正确的手机號码
300701  該手机號沒有注冊
300702  密码错误次数过多账號已鎖定，请%s 分鐘后重新登录或找回密码
300703  密码错误，请重新輸入，您還可以嘗试%s 次
300705  該账户未设置登录密码，请使用短信验证码登录
300809  需要校验手机短信验证码

1.3 渠道验证码登录
手机+验证码+渠道登录：

接口地址 /user-server/open-api/loginCaptcha

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

请求参数说明：

参数名称  说明  请求类型  必填  类型

X-Lang

語言类别(1-简體，2-繁體，
3-English)

header

true

string

X-Request-Id

頭部信息的  requestId 信息,长
度 30 位，确保唯一，防止重
複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

签名

header

true

string

areaCode

区域號 86 中國， 852 香港，
853 中國澳門，  886 中國臺
灣，65 新加坡

body

true

string

captcha

验证码

body

true

string

phoneNumber

手机號 RSA 加密（与 X-Sign

body

true

string

---

## 第 9 页

不同秘钥）

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例：

{
"areaCode": 86,
"modifyUserConfigParam": {
"languageCn": 1,
"languageHk": 1,
"lineColorHk": 1
},
"captcha": "1234",
"phoneNumber": "rsa"
}

参数说明：

参数名称  说明  类型
areaCode  区號  string
avatar  頭像地址  string
expiration  过期时间  int64
extendStatusBit  用户擴展状态  int32
firstLogin  是否为第一次登陸  boolean
invitationCode  邀请码，如果有，则顯示。  string
languageCn  1 简體 2 繁體  int32
languageHk  1 简體 2 繁體  int32
lineColorHk  1 紅漲綠跌 2 綠漲紅跌  int32
nickname  昵称  string
openedAccount  是否开户  boolean
phoneNumber  手机號  string
thirdBindBit  綁定位 手机 1<<0 微信 1<<1 微博 1<<2  int32
token  登录授权的 token  string

---

## 第 10 页

tradePassword  是否设置过交易密码  boolean
unionId  微信公眾平台的 unionId，如果有则顯示。  string
uuid  盈立用户注冊的 uuid，全域唯一  int64

返回示例：

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登录密码 1<<1 行情許可权 1<<2 衍生品", "firstLogin": true,
"invitationCode": 1234,
"languageCn": 0,
"languageHk": 0,
"lineColorHk":  0, "nickname": "xxx",
"openedAccount": true, "phoneNumber":
"188xxxx9188", "thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回应状态

状态码  说明
0  成功
200  OK
300100  非法请求
300102  账户被冻结，无法完成操作，如非本人操作，请联繫客服
300103  用户被刪除
300309  请輸入正确的手机號码
300701  該手机號沒有注冊
300702  密码错误次数过多账號已鎖定，请%s 分鐘后重新登录或找回密码
300703  密码错误，请重新輸入，您還可以嘗试%s 次
300705  該账户未设置登录密码，请使用短信验证码登录
300809  需要校验手机短信验证码

---

## 第 11 页

1.4 设置交易密码

接口地址 /user-server/open-api/set-trade-password

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 需帶登录态 token 使用者需要完成开户，且未设置过交易密码，否则算非法请求

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言 1 简體 2 繁體

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password 交易密码 设置、修改、重置交易密码必填，交易
密码必須是 6 位元純数位 RSA 加密（与 X-Sign 不
同秘钥）

body

true

string

oldPassword 舊交易密码 修改交易密码必填，交易密码必須是
6 位元純数位 RSA 加密（与 X-Sign 不同秘钥）

body

false

string

phoneCaptcha

手机验证码，根据验证码重置交易密码必填

body

false

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8

---

## 第 12 页

X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"oldPassword": "",
"password": "", "phoneCaptcha":
""
}

回应状态

状态码 说明 schema
0 成功
200 OK UserResponseEntity
300100 非法请求
300101 非法 TOKEN
301001 交易密码需为 6 位元純数字，请重新輸入
301003 交易密码错误，请重新輸入，您還可以嘗试%s 次
301004 交易服务异常
301005 账户被冻结，无法完成操作，如非本人操作，请联繫客服

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{
"code": 0,
"data": {},
"msg": ""

---

## 第 13 页

}

1.5 校验交易密码

接口地址 /user-server/open-api/check-trade-password

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 許可权：需要 Token

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Request-Id

頭部信息的 requestId 信息， 19 位元长度

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password

交易密码必須是 6 位元純数位 RSA 加密

（与 X-Sign 不同秘钥）

String

false

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

---

## 第 14 页

请求示例

/user-server/open-api/check-trade-password?password=123456 RES 加密

回应状态

状态码 说明 schema
0 成功
200 OK UserResponseEntity
300100 非法请求
300101 非法 TOKEN
301001 交易密码需为 6 位元純数字，请重新輸入
301002 错误次数过多交易密码已鎖定，请%s 小时后重新嘗试或找回
密码

301004 交易服务异常
310104 交易密码错误
310106 未设置交易密码

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{
"code": 0,
"data": {},
"msg": ""
}

1.6 重置登录密码

接口地址 /user-server/open-api/reset-login-password

---

## 第 15 页

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 不需要 token

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

areaCode 区域號 86 中國，852 香港，853 中國澳門，886 中
國臺灣，65 新加坡

body

false

string

password

新密码 RSA 加密（与 X-Sign 不同秘钥）

body

false

string

phoneCaptcha

手机验证码

body

false

string

phoneNumber

手机號 RSA 加密（与 X-Sign 不同秘钥）

body

false

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082

---

## 第 16 页

X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"areaCode": "86", "password": "rsa"，
"phoneCaptcha": "1234",
"phoneNumber": "188********"
}

回应状态

状态码 说明 schema
0 成功

200 OK UserResponseEntity
300100 非法请求

300304 验证次数过多，请稍后重试

300305 抱歉，验证码已过期，请重新获取

300701 該手机號沒有注冊

300707 您当前已通过客户经理完成预注冊，请通过短信验证码登
录並启动账號。

300800 短信验证码不正确，请重新輸入

300801 密码长度不能小于 8 位

300802 密码长度不能大于 24 位

300803 密码不能为純数位/字母/符號

300804 请设置正确密码，8~24 位元数位/字母/符號组合

回应参数

参数名称

说明

类型

schema

code

回应码

int32

---

## 第 17 页

data

回应體

object

msg

回应内容

string

回应示例

{

"code": 0,
"data": {},
"msg": ""

}

1.7 解鎖交易

接口地址 /user-server/open-api/trade-login

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 需要 token

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

---

## 第 18 页

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password

新密码 RSA 加密（与 X-Sign 不同秘钥）

body

true

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

回应状态

状态码 说明 schema
0 成功

200 OK UserResponseEntity
300100 非法请求

300304 验证次数过多，请稍后重试

300305 抱歉，验证码已过期，请重新获取

300701 該手机號沒有注冊

300707 您当前已通过客户经理完成预注冊，请通过短信验证码登
录並启动账號。

300800 短信验证码不正确，请重新輸入

300801 密码长度不能小于 8 位

300802 密码长度不能大于 24 位

300803 密码不能为純数位/字母/符號

300804 请设置正确密码，8~24 位元数位/字母/符號组合

---

## 第 19 页

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{

"code": 0,

"data": ,

"msg": ""

}

1.8 获取交易解鎖状态

接口地址 /user-server/open-api/get-trade-status

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 需要 token

请求参数

---

## 第 20 页

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password

新密码 RSA 加密（与 X-Sign 不同秘钥）

body

true

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

回应状态

状态码 说明 schema

0

成功

200

OK

UserResponseEntity

300100

非法请求

300304

验证次数过多，请稍后重试

300305

抱歉，验证码已过期，请重新获取

300701

該手机號沒有注冊

300707 您当前已通过客户经理完成预注冊，请通过短信验证码登录並
启动账號。

---

## 第 21 页

300800

短信验证码不正确，请重新輸入

300801

密码长度不能小于 8 位

300802

密码长度不能大于 24 位

300803

密码不能为純数位/字母/符號

300804

请设置正确密码，8~24 位元数位/字母/符號组合

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

status

订单状态，0 未解密，1 已解鎖

int32

msg

回应内容

string

回应示例

{
"code": 0, "msg": "
成功", "data": {
"status": 0
}
}

1.9 修改交易密码

接口地址 /user-server/open-api/update-trade-password

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

---

## 第 22 页

接口描述 需帶登录态 token 使用者需要完成开户，且未设置过交易密码，否则算非法请求

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言 1 简體 2 繁體

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password

交易密码 必填， 交易密码必須是 6 位元純数位

RSA 加密（与 X-Sign 不同秘钥）

body

true

string

oldPassword 舊交易密码 修改交易密码必填，交易密码必須是
6 位元純数位 RSA 加密（与 X-Sign 不同秘钥）

body

false

string

phoneCaptcha

手机验证码，根据验证码重置交易密码必填

body

false

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"oldPassword": "",
"password": "", "phoneCaptcha":
""
}

---

## 第 23 页

回应状态

状态码 说明 schema
0 成功
200 OK UserResponseEntity
300100 非法请求
300101 非法 TOKEN
301001 交易密码需为 6 位元純数字，请重新輸入
301003 交易密码错误，请重新輸入，您還可以嘗试%s 次
301004 交易服务异常
301005 账户被冻结，无法完成操作，如非本人操作，请联繫客服

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{
"code": 0,
"data": {},
"msg": ""
}

1.10 重置交易密码

接口地址 /user-server/open-api/reset-trade-password

请求方式 POST

consumes ["application/json"]

---

## 第 24 页

produces ["application/json"]

接口描述 需帶登录态 token 使用者需要完成开户，且未设置过交易密码，否则算非法请求

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言 1 简體 2 繁體

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password

交易密码 必填， 交易密码必須是 6 位元純数位

RSA 加密（与 X-Sign 不同秘钥）

body

true

string

oldPassword 舊交易密码 非必填，交易密码必須是 6 位元純
数位 RSA 加密（与 X-Sign 不同秘钥）

body

false

string

phoneCaptcha

手机验证码，根据验证码重置交易密码必填

body

false

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"oldPassword": "",

---

## 第 25 页

"password": "",
"phoneCaptcha": ""
}

回应状态

状态码 说明 schema
0 成功
200 OK UserResponseEntity
300100 非法请求
300101 非法 TOKEN
301001 交易密码需为 6 位元純数字，请重新輸入
301003 交易密码错误，请重新輸入，您還可以嘗试%s 次
301004 交易服务异常
301005 账户被冻结，无法完成操作，如非本人操作，请联繫客服

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{
"code": 0,
"data": {},
"msg": ""
}

1.11 修改登陸密码

接口地址 /user-server/open-api/update-login-password

请求方式 POST

consumes ["application/json"]

---

## 第 26 页

produces ["application/json"]

接口描述 需帶登录态 token 使用者需要已设置登陸密码，否则算非法请求

请求参数

参数名称 说明 请求类型 必填 类型

Authorization

見概述 Authorization 说明

header

true

string

X-Lang

語言 1 简體 2 繁體

header

true

string

X-Request-Id  頭部信息的 requestId 信息,长度 30 位，确保唯
一，防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string
X-Sign

签名

header

true

string

password 新登陸密码 必填 RSA 加密（与 X-Sign 不同秘
钥）

body

true

string

oldPassword 舊登陸密码 必填 RSA 加密（与 X-Sign 不同秘
钥）

body

true

string

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"oldPassword": "",
"password": "",
}

---

## 第 27 页

回应状态

状态码 说明 schema
0 成功
200 OK UserResponseEntity
300100 非法请求
300101 非法 TOKEN
300704 原登陸密码不正确
300804 请设置正确密码，8~24 位元数位/字母/符號组合
300810 新密码长度不能小于 8 位
300811 新密码长度不能大于 24 位
300812 新密码不能为純数位/字母/符號

回应参数

参数名称

说明

类型

schema

code

回应码

int32

data

回应體

object

msg

回应内容

string

回应示例

{
"code": 0,
"data": {},
"msg": ""
}

2 交易

2.1 下单

接口地址 /stock-order-server/open-api/entrust-order

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

---

## 第 28 页

接口描述 下单

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Dt 设備类型 (t1-android ， t2-ios， t3- 其他， t4-
Windows,t5-Mac)

header

true

string

X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止
重複提交实现接口冪等

header

true

string

X-Sign

RSA 签名

header

true

string
serialNo 流水號，最长 19 位，确保唯一推薦雪花演
算法生成

body

true

int64

entrustAmount

委托数量

body

true

number

entrustPrice

价格(競价单价格传 0)

body

true

number

entrustProp 委托属性 ('0'- 美股限价单 / 暗盤委托  limit
order,'d'-競价单 ,'e'-增強限价单 ,'g'-競价限价
单)

body

true

string

entrustType

委托类别(0-买，1-卖)

body

true

int32

exchangeType

交易类别(0-香港,5-美股,6-滬港通,7-深港通)

body

true

int32

stockCode

股票代码

body

true

string

password

交易密码（RDA 公开密钥加密）

body

false

string

stockName

股票名称

body

false

string

forceEntrustFlag 是否強制委托标 記，超过 9 倍 24 档下单时
forceEntrustFlag=true 可強制下单，但有可能
是废单

body

false

boolean

sessionType 交易階段标志（0/不传-正常订单交易（预
设），1-盤前，2-盤后交易，3-暗盤交易）

body

false

int32

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

---

## 第 29 页

Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"serialNo": "2000000000000000018",
"entrustAmount": "1000",
"entrustPrice": "11.0",
"entrustProp": "e",
"entrustType": "0",
"exchangeType": "0",
"stockCode": "00981",
"stockName": "00981", "forceEntrustFlag":
"false", "sessionType": "0",
"password":"Fpocc_11vTS6mS9YKYby6-
v2VNujUx_fnnMaGncHPerLh9mCP_vDIhbeE1GLNDU4arl1euay-
hiTmqmlwZlwtCMbw3Law7mx9NgVuwGVX3pXPuwYjcqxhaGZIsATHDSywxd4uZZhTCsrRua-
Ug8dgJaPDc5os7-A9sFYxbxhI6I="
}

回应状态
状态码 说明 schema
0 成功
200 OK ResponseVO«EntrustOrderResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found
406472 订单中不能包含小于 1 手数量的碎股，请交易 1
手的整数倍，或通过"碎股单"交易碎股

410200 抱歉，订单中不能包含小于 1 手数量的碎股，请
交易 1 手的整数倍，如需交易碎股请联繫客服。

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

EntrustOrderResponse

EntrustOrderResponse

entrustId

订单 id,可用于查询订单/修改订单/取消订

string

---

## 第 30 页

单

status

订单状态

int32

statusName

订单状态名称

string

·msg

状态信息

string

回应示例
{
"code": 0,
"msg": "操作成功",
"data": {
"entrustId": "1181776863632019456",
"status": 1, "statusName": "等待
提交"
}
}

2.2 委托改单/撤单

接口地址 /stock-order-server/open-api/modify-order

请求方式 POST

consumes ["application/json"]

produces ["*/*"]
接口描述 委托改单/撤单

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止
重複提交实现接口冪等

header

true

string

X-Sign

RSA 签名

header

true

string

actionType

操作类型(0-撤单，1-改单)

body

true

int32

entrustAmount

委托数量，撤单时传 0

body

true

number

entrustId

委托 Id

body

true

int64

entrustPrice

委托价格，撤单时传 0

body

true

number

---

## 第 31 页

password

交易密码（RDA 公开密钥加密）

body

false

string

forceEntrustFlag 是否強制委托标 記，超过 9 倍 24 档下单时
forceEntrustFlag=true 可強制下单，但有可能是
废单

body

false

boolean

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"actionType": 1,
"entrustAmount": 500,
"entrustId": 1181776863632019456,
"entrustPrice": 322.0,
"forceEntrustFlag": true
}

回应状态
状态码 说明 schema
0 成功
200 OK Object
201 Created
401 Unauthorized
403 Forbidden
404 Not Found
406472 订单中不能包含小于 1 手数量的碎股，请交易 1 手的整
数倍，或通过"碎股单"交易碎股

410200 抱歉，订单中不能包含小于 1 手数量的碎股，请交易 1
手的整数倍，如需交易碎股请联繫客服。

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

Object

---

## 第 32 页

entrustId

申请编號

string

status

状态

int32

statusName

状态名

string

msg

状态信息

string

回应示例
{
"code": 0,
"msg": "操作成功",
"data": {
"entrustId": "1181776863632019456",
"status": 5, "statusName": "等待
改单"
}
}

2.3 改单範圍

接口地址 /stock-order-server/open-api/modified-range

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 改单展
示範圍
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

entrustId

委托 Id

body

true

int64

newPrice

最新价-競价单也需要传最新价

body

true

number

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8

---

## 第 33 页

X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求示例
{
"entrustId": 1181776863632019456,
"newPrice": 323
}

回应状态
状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«QueryEntrustInfoResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 QueryEntrustInfoRespons e QueryEntrustInf
oResponse

businessAmount

成交数量

number

entrustAmount

原订单数量

number

modifiedUpperAmount

可修改範圍的修改上限

number

modifiedlowerAmount

可修改範圍的修改下限

number

msg

状态信息

string

回应示例
{
"code": 0,
"data": {
"businessAmount": 0,
"entrustAmount": 0,
"modifiedUpperAmount": 0,
"modifiedlowerAmount": 0
},
"msg": ""

---

## 第 34 页

}

2.4 碎股下单

接口地址 /stock-order-server/open-api/odd-entrust

请求方式 POST

consumes ["application/json"]
produces ["*/*"] 介
面描述 碎股交易请
求示例
{
"entrustAmount": 1,
"entrustPrice": 82.1,
"entrustType": 1,
"exchangeType": 0,
"stockCode": "00002"
}

请求参数
参数名称 说明 请求类型 必填 类型
Authorization 頭部信息的 token 信息 header true string
X-Lang 語言类别(1-简體，2-繁體，3-English) header true string
X-Channel 渠道 ID，由盈立分配 header true string
X-Time 时间标記 header true string
X-Dt 设備类型 (t1-android ， t2-ios ， t3- 其他， t4-
Windows,t5-Mac)
header true string
X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止重
複提交实现接口冪等
header true string
X-Sign RSA 签名 header true string
entrustAmount 委托数量 body true number
entrustPrice 价格 body true number
entrustType 委托类别(1-卖) body true int32
exchangeType 交易类别(0-香港,5-美股) body true int32
stockCode 股票代码 body true string

回应状态

---

## 第 35 页

状态码 说明 schema
200 OK
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

code

状态码

int32

data

返回體

oddId

碎股请求記录 id

string

status

订单状态

int32

statusName

订单状态名称

string

msg

状态信息

string

回应示例

2.5 碎股撤单

接口地址 /stock-order-server/open-api/odd-modify

请求方式 POST

consumes ["application/json"]

produces ["*/*"]
{
"code": 0,
"msg": "操作成功",
"data": {
"oddId": "1207553433704988672",
"status": 0,
"statusName": "待报单"
}
}

---

## 第 36 页

接口描述 碎股交易

请求示例

{

"actionType": 0,

"oddId": 1207553433704988672

}

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止重複提
交实现接口冪等

header

true

string

X-Sign

RSA 签名

header

true

string

actionType

操作类型(0-撤单)

body

true

int32

oddId

碎股委托 Id

body

true

int64

回应状态
状态码 说明
200 OK
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

---

## 第 37 页

参数名称

说明

类型

code

状态码

int32

oddId

碎股请求記录 id

string

status

订单状态

int32

statusName

订单状态名称

string

msg

状态信息

string

回应示例

2.6 最大可买、可卖数量

接口地址 /stock-order-server/open-api/trade-quantity

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 获取最
大可用数量
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string
{
"code": 0,
"msg": "操作成功",
"data": {
"oddId": "1207553433704988672",
"status": 9,
"statusName": "已撤单"
}
}

---

## 第 38 页

X-Sign

RSA 签名

header

true

string

entrustPrice

委托价格(不能为 0,競价单可不填)

body

false

number

entrustProp 委托属性('0'- 美股限价单,'d'- 競价单,'e' - 增強限价
单,'g'-競价限价单，'u'-碎股单)

body

true

string

exchangeType

交易类别(0-香港,5-美股,6-滬港通,7-深港通)

body

true

int32

stockCode

证券代码

body

true

string

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"entrustPrice": 234, "entrustProp":
"e", "exchangeType": 0,
"stockCode": "700"
}

回应状态
状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«SaleAndBuyQuantityResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 SaleAndBuyQuantityRespo
nse
SaleAndBuyQuantityRespo
nse

buyEnableAmount

最大可买数量

number

---

## 第 39 页

oddEnableAmount

最大可卖碎股数量

number

saleEnableAmount

最大可卖数量

number

saleEnableIntAmount

最大可卖整股数量

number

handAmount

每手股数

number

msg

状态信息

string

回应示例
{
"code": 0,
"msg": "操作成功",
"data": {
"saleEnableAmount": 500.00,
"saleEnableIntAmount": 500.0000,
"oddEnableAmount": 0.0000,
"buyEnableAmount": 800.00,
"handAmount": 100.0000
}
}

2.7 今日订单-分页查询

接口地址 /stock-order-server/open-api/today-entrust

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 需要资
金账號
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

exchangeType 交易类别(0-香港,5-美股, 67-A 股，100-查询所有交
易类别)

body

true

int32

---

## 第 40 页

pageNum

当前页 1 开始，预设值 1

body

false

int32

pageSize

每页结果数，预设值 10

body

false

int32

stockCode

证券代码

body

false

string

stockName

证券名称

body

false

string

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"exchangeType": 0,
"pageNum": 1,
"pageSize": 10, "stockCode": "",
"stockName": ""
}

回应状态
状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«PageInfoVO«TodayEntrustByAppResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 PageInfoVO«
TodayEntrust
ByAppRespo
PageInfoVO«Today
EntrustByAppResp
onse»

---

## 第 41 页

nse»

list

结果集合

array TodayEntrustByAp
pResponse

businessAmount

成交数量

number

businessAveragePrice

成交均价

number

serialNo

流水號

int64

createTime

委托时间

string

entrustAmount

委托数量

number

entrustId

委托 id

string

entrustNo

委托编號

string

entrustPrice

委托价格

number

entrustProp

委托属性('0'-美股限价单,'d'-競价单,'e' -增
強限价单,'g'-競价限价单,'h'-港股限价单,'j'-
特殊限价单)

string

entrustType

买卖方向,委托类型(0-买，1-卖)

int32

exchangeType

交易类别，0 港股，5 美股

int32

flag 订单类型-普通单 0-条件单 1-碎股单 2-月供
股单

string

moneyType

币種类别

int32

sessionType 交易階段标志 （0/不传-正常订单交易（ 预
设 ） ， 1- 盤前， 2- 盤后交易，  3- 暗盤交
易）

int32

status

委托状态

int32

statusName

委托状态名

string

stockCode

股票代码

string

stockName

股票简體名称

string

pageNum

当前页

int32

pageSize

每页条数

int32

total

总数

int64

msg

状态信息

string

回应示例
{
"code": 0,

---

## 第 42 页

"msg": "操作成功",
"data": {
"pageNum": 1,
"pageSize": 0,
"total": 1,
"list": [{
"entrustId": "1181776863632019456",
"entrustNo": "191",
"status": 5, "statusName": "等待改
单", "exchangeType": 0,
"entrustType": 0, "entrustProp": "e",
"entrustAmount": 700,
"businessAmount": 0,
"entrustPrice": 210,
"businessAveragePrice": 0,
"stockCode": "00700",
"stockName": "騰讯控股",
"moneyType": 2,
"createTime": "11:42:15",
"flag": "0",
"serialNo": 1233123554314,
"sessionType": 0
}]
}
}

2.8 全部订单-分页查询

接口地址 /stock-order-server/open-api/his-entrust

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 需要资
金账號
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

---

## 第 43 页

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

dateFlag

1:一周订单，2：一个月订单，3: 三个月订单，
4：近一年订单，5：今年订单，6：自选时间,7.查
询全部

body

true

string

exchangeType 交易类别(0-香港,5-美股, 67-A 股，100-查询所有交
易类别)

body

true

int32

entrustBeginDate 开始时间，如果不传时间默认从最新前一天倒序,
规则 yyyy-MM-dd

body

false

string

entrustEndDate 结束时间，如果不传时间默认从最新前一天倒序,
规则 yyyy-MM-dd

body

false

string

pageNum

当前页 1 开始，预设值 1

body

false

int32

pageSize

每页结果数，预设值 10

body

false

int32

stockCode

证券代码

body

false

string

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"dateFlag": "1",
"entrustBeginDate": "",
"entrustEndDate": "",
"exchangeType": 0,
"pageNum": 1,
"pageSize": 10,
"stockCode": ""
}

回应状态
状态码 说明 schema
0 成功 ResponseVO

---

## 第 44 页

200 OK ResponseVO«PageInfoVO«HisEntrustByAppResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

PageInfoVO«
HisEntrustBy
AppResponse
»

PageInfoVO«His
EntrustByAppRe
sponse»

list

结果集合

array HisEntrustByAp
pResponse
businessAmoun
t

成交数量

number

businessAverag
ePrice

成交均价

number

serialNo

流水號

int64

createDate

委托日期

string

createTime

委托时间

string

dayEnd

是否隔天,0 未隔天，1 已经隔天

int32

entrustAmount

委托数量

number

entrustId

委托 ID

string

entrustNo

委托编號

string

entrustPrice

委托价格

number

entrustProp

委托属性('0'-美股限价单,'d'-競价单,'e' -增強限价单,'g'-

競价限价单,'h'-港股限价单,'j'-特殊限价单)

string

entrustType

买卖方向,委托类型(0-买，1-卖)

int32

exchangeType

交易类别，0 港股，5 美股

int32

flag

订单类型-普通单 1-条件单 2-碎股单 3-月供股单 4

string

moneyType

币種类别

int32

sessionType

交易階段标志（0/不传-正常订单交易（预设），1-盤

int32

---

## 第 45 页

前，2-盤后交易，3-暗盤交易）

status

委托状态

int32

statusName

委托状态名

string

stockCode

股票代码

string

stockName

股票简體名称

string

pageNum

当前页

int32

pageSize

每页条数

int32

total

总数

int64

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"pageNum": 1,
"pageSize": 20,
"total": 2,
"list": [{
"entrustId": "1181776863632019456",
"entrustNo": "191",
"status": 5, "statusName": "等待改
单", "exchangeType": 0,
"entrustType": 0, "entrustProp": "e",
"entrustAmount": 700,
"businessAmount": 0,
"entrustPrice": 210,
"businessAveragePrice": 0,
"stockCode": "00700",
"stockName": "騰讯控股",
"moneyType": 2,
"createTime": "11:42:15",
"createDate": "20191009",
"flag": "0",
"serialNo": 1233123554314,
"sessionType": 0
}
],

---

## 第 46 页

"nowDate": "20191009"
}
}

2.9 查询订单明細

接口地址 /stock-order-server/open-api/order-detail

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 查询订
单明細
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string
appEntrustRecordDetail
Request

appEntrustRecordDetailRequest

body

true AppEntrustReco
rdDetailRequest
serialNo 流水號（委托 ID、流水號一个至少传
一个）

body

true

int64

entrustId 委托 id（委托 ID、流水號一个至少传
一个）

body

true

int64

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求示例

---

## 第 47 页

{
"serialNo": 0,
"entrustId": 0
}

回应状态

状态码

说明

schema

0

成功

ResponseVO

200

OK

ResponseVO«AppEntrustRecordDetailResponse»

201

Created

401

Unauthorized

403

Forbidden

404

Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 AppEntrustReco
rdDetailRespons
e
AppEntrustRec
ordDetailResp
onse
appEntrustRecordDet
ailInfoList

list 信息

array AppEntrustRec
ordDetailInfo

businessAmount

成交数量

number

businessAveragePrice

成交均价

number

businessBalance

成交金额

number

commissionFee

港美,佣金

string

createTime

时间

string

depositStockDay

股份到账时间

string

---

## 第 48 页

entrustId

委托記录號

int64

entrustAmount

委托数量

number

entrustBalance

委托金额

number

entrustFee

总費用

string

entrustPrice

委托价格

number

entrustProp

委托属性('0'-美股限价单,'d'-競价单,'e' -增強限价

单,'g'-競价限价单,'h'-港股限价单,'j'-特殊限价单)

string

entrustPropName

委托属性('0'-美股限价单,'d'-競价单,'e' -增強限价

单,'g'-競价限价单,'h'-港股限价单,'j'-特殊限价单)

string

moneyType

币種类别

int32

orderStatus

状态

int32

orderStatusName

状态名

string

payFee

港美，交收費

string

platformUseFee

港美,平台使用費

string

stampDutyFee

港，印花稅

string

tradingSystemUsage

港，交易系统使用費

string

transactionFee

港：交易費，美：证監會費

string

transactionLevyFee

港，交易徵費，美：交易活动費

string

document

文案信息

string

entrustType

买入卖出

int32

exchangeType

市場类型

int32

sessionType 交 易 階 段 标 志（ 0/ 不传 - 正 常 订 单 交 易（ 预
设），1-盤 前 ，2-盤 后 交 易 ，3-暗 盤 交 易 ）

int32

status

委托状态

int32

statusName

委托状态名

string

stockCode

股票代码

string

stockName

股票名称

string

msg

状态信息

string

回应示例
{
"code": 0,
"msg": "操作成功",
"data": {

---

## 第 49 页

"statusName": "全部成交",
"status": 0,
"stockCode": "00700",
"stockName": "騰讯控股",
"document": "由于和交易所清算交收，部分资料可能在交易完成的第 2 天（工作日）展示",
"appEntrustRecordDetailInfoList": [{ "entrustProp": "e",
"entrustPropName": "增強限价单",
"entrustAmount": 700,
"businessAmount": 700,
"entrustPrice": 210,
"entrustBalance": 147000,
"businessAveragePrice": 322,
"businessBalance": 225400,
"moneyType": 2,
"createTime": "2019-10-09 11:42:15",
"depositStockDay": null,
"commissionFee": null,
"platformUseFee": null,
"stampDutyFee": null, "payFee": null,
"transactionFee": null,
"transactionLevyFee": null,
"tradingSystemUsage": null,
"entrustFee": null, "orderStatus": 11,
"orderStatusName": "委托下单"
},
{
"entrustProp": "e", "entrustPropName": "增
強限价单", "entrustAmount": 700,
"businessAmount": 700,
"entrustPrice": 322,
"entrustBalance": 225400,
"businessAveragePrice": 322,
"businessBalance": 225400,
"moneyType": 2,
"createTime": "2019-10-09 14:58:03",
"depositStockDay": null,
"commissionFee": null,
"platformUseFee": null,
"stampDutyFee": null, "payFee":
null,

---

## 第 50 页

"transactionFee": null,
"transactionLevyFee": null,
"tradingSystemUsage": null,
"entrustFee": null, "orderStatus": 21,
"orderStatusName": "改单（最新订单）"
},
{
"entrustProp": "e", "entrustPropName": "增
強限价单", "entrustAmount": 700,
"businessAmount": 700,
"entrustPrice": 322,
"entrustBalance": 225400,
"businessAveragePrice": 322,
"businessBalance": 225400,
"moneyType": 2,
"createTime": "2019-10-09 15:00:30",
"depositStockDay": null,
"commissionFee": null,
"platformUseFee": null,
"stampDutyFee": null, "payFee": null,
"transactionFee": null,
"transactionLevyFee": null,
"tradingSystemUsage": null,
"entrustFee": null, "orderStatus": 0,
"orderStatusName": "全部成交（订单结束）"
}
],
"entrustType": 0,
"exchangeType": 0,
"finalStateFlag": "1",
"sessionType": 0,
"entrustId": 1181776863632019500
}
}

2.10 查询成交流水-分页查询

接口地址 /stock-order-server/open-api/stock-record

请求方式 POST

---

## 第 51 页

consumes ["application/json"] produces
["application/json"] 接口描述 需要资
金账號
请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

exchangeType 交易类别(0-香港,5-美股, 67-A 股，100-查询所有交
易类别)

body

true

int32

stockCode

股票代码

body

false

string

entrustId

委托 ID

body

false

int64
beginTime

成交开始时间，规则 yyyy-MM-dd

body

false

string
endTime

成交结束时间，规则 yyyy-MM-dd

body

false

string

pageNum

当前页 1 开始，预设值 1

body

false

int32

pageSize

每页结果数，预设值 10

body

false

int32

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求示例
{
"beginTime": "2019-10-01",
"endTime": "2019-10-10",
"entrustId": 0,
"exchangeType": 0,
"pageNum": 1,

---

## 第 52 页

"pageSize": 10,
"stockCode": "700"
}

回应状态
状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«PageInfoVO«StockRecordResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

PageInfoVO«StockRe
cordResponse»

PageInfoVO«Stoc
kRecordResponse
»

list

结果集合

array StockRecordResp
onse

businessAmount

成交数量

number

businessBalance

成交金额

number

businessPrice

成交价格

number

businessStatus

成交状态（1 成交成功，2 成交取消）

int32

businessTime

成交时间

date-time

createTime

記录创建时间

date-time

entrustId

委托記录號

int64

entrustType

委托类型(''0''- 买， 1- 卖， ''2''- 查询，
''3'- 撤单， ''4'- 補单， ''5''- 改单， 6 转
入，7 转出,8 成交取消类型)

int32

exchangeType

交易类别 ('0'-香港，'1'-上海 A，'2'-上

海 B，'3'-深圳 A，'4'-深证 B，'5'-美

股，'6'-滬股通，'7'-深港通)

int32

id

int64

moneyType

币種类型(0-人民币，1-美元，2-港币)

int32

recordId

成交流水编號

int64

---

## 第 53 页

remark

備注

string

stockCode

股票代码

string

stockName

股票名称

string

updateTime

記录最后更新时间

date-time

userId

用户 id

int64

pageNum

当前页

int32

pageSize

每页条数

int32

total

总数

int64

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"pageNum": 1,
"pageSize": 10,
"total": 133,
"list": [{
"id": 18405,
"recordId": 1139100093871222800,
"entrustId": 1139096696801153000,
"userId": 336547695646785540,
"moneyType": 2,
"exchangeType": 0,
"stockCode": "700",
"stockName": "騰讯控股",
"businessStatus": 1,
"businessPrice": 334.2,
"businessAmount": 10,
"businessTime": "2019-06-14T09:12:49.000+0000", "createTime":
"2019-06-13T09:20:00.000+0000", "updateTime": "2019-06-
13T09:20:00.000+0000",
"remark": null,
"entrustType": 0,
"businessBalance": 3342
}]
}
}

---

## 第 54 页

2.11 查询持倉

接口地址 /stock-order-server/open-api/stock-holding

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 需要资金账號

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

exchangeType

交易类别(0-香港,5-美股, 67-A 股，100-

查询所有交易类别)

body

true

int32

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

查询请求 body 示例

{
"exchangeType": 0
}

---

## 第 55 页

回应状态

状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«List«StockHolding»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

array

StockHolding

costPriceAccurate

成本价--精确

string

currentAmount

持倉数量

string

enableAmount

可卖数量

string

frozenAmount

冻结数量

string

exchangeType

交易类型

int32

oddAmount

碎股数量

string

stockCode

股票代码

string

stockName

股票名称

string

lastPrice

最新价

string

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": [{
"exchangeType": 0,
"stockCode": "19981", "stockName": "國藥麥
銀零四沽 A", "currentAmount":
"157.000000",
"oddAmount": "157.000000",

---

## 第 56 页

"lastPrice": "0.320000",
"costPriceAccurate": "0.303000000"
}]
}

2.12 查询资产

接口地址 /stock-order-server/open-api/stock-asset

请求方式 POST

consumes ["application/json"]

produces ["application/json"]

接口描述 需要资金账號

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang 語言类别 (1- 简體， 2- 繁體， 3-
English)

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间戳記

header

true

string

X-Sign

RSA 签名

header

true

string

exchangeType

交易类别(0-香港,5-美股,67-A 股)

body

true

int32

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

---

## 第 57 页

请求 body 示例

{
"exchangeType": 0
}

回应状态

状态码 说明 schema
0 成功 ResponseVO
200 OK ResponseVO«StockAssetDTO»
201 Created
401 Unauthorized +
403 Forbidden
404 Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

StockAssetDTO

StockAssetDTO

asset

总资产

string

enableBalance

可用金额

string

frozenBalance

冻结金额

string

onWayBalance

在途资金

string

stockHoldingList

持倉列表

array

StockHolding

costPriceAccurate

成本价--精确

string

currentAmount

持倉数量

string

exchangeType

交易类型

int32

oddAmount

碎股数量

string

stockCode

股票代码

string

stockName

股票名称

string

withdrawBalance

可取金额

string

msg

状态信息

string

---

## 第 58 页

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"asset": "96117771.040000",
"marketValue": "3035584.090000",
"enableBalance": "92906473.37",
"withdrawBalance": "92906473.37",
"frozenBalance": "175713.580000",
"onWayBalance": "0.000000", "stockHoldingList":
[{
"exchangeType": 0,
"stockCode": "19981", "stockName": "國藥麥
銀零四沽 A", "currentAmount":
"157.000000",
"oddAmount": "157.000000",
"lastPrice": "0.320000",
"marketValue": "50.240000",
"hisMarketValue": "0.000000",
"costPrice": "0.303",
"costPriceAccurate": "0.303000000",
"dailyBalance": "50.240000",
"dailyBalancePercent": "1.000000",
"holdingBalance": "2.669000",
"holdingBalancePercent": "0.056106",
"quoteType": "1"
}]
}
}

2.13 客户股票资产查询批量

接口地址 /stock-order-server/open-api/stock-asset-list

请求方式 POST

consumes ["application/json"] produces
["application/json"] 接口描述 需要资
金账號
请求示例

---

## 第 59 页

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"exchangeType": 100
}

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Lang

語言类别(1- 简體， 2- 繁體， 3-
English)

header

true

string

X-Sign

RSA 签名

header

true

string

X-Type

APP 类别(1-大陸版，2-港版)

header

true

string

stockAssetForAppReq

stockAssetForAppReq

body

true

StockAssetForAppReq

exchangeType

交易类别，0 港股，5 美股

body

true

int32

---

## 第 60 页

回应状态

状态码

说明

schema

0

成功

ResponseVO

200

OK

ResponseVO«List«StockAssetDTO»»

201

Created

401

Unauthorized

403

Forbidden

404

Not Found

回应参数

参数名称

说明

类型

code

状态码

int32

data

返回體

array

asset

总资产

string

enableBalance

可用金额

string

frozenBalance

冻结金额

string

marketValue

股票市值

string

onWayBalance

在途资金

string

---

## 第 61 页

stockHoldingList

持倉列表

array

costPrice

成本价

string

costPriceAccurate

成本价--精确

string

currentAmount

持倉数量

string

dailyBalance

当日盈虧金额

string

dailyBalancePercent

当日盈虧占比

string

enableAmount

可卖数量

number

exchangeType

交易类型

int32

frozenAmount

冻结数量

number

hisMarketValue

市值

string

holdingBalance

持倉盈虧金额

string

holdingBalancePercent

持倉盈虧占比

string

lastPrice

最新价

string

marketValue

市值

string

oddAmount

碎股数量

string

---

## 第 62 页

quoteType

行情許可权 0: 延时行情 1:bmp 行情

2:level1 行情 3:level2 行情

string

stockCode

股票代码

string

stockName

股票名称

string

stockOnWayBalanceDTOList

在途资金列表

array

applyType

业务类型 IpoApplyTypeEnum

int32

applyTypeName

业务类型 IpoApplyTypeEnum

string

exchangeType

市場

int32

moneyType

币種

int32

onWayBalance

在途现金

number

stockCode

股票代码

string

stockName

股票名称

string

totalDailyBalance

今日盈虧金额

string

totalDailyBalancePercent

今日盈虧占比

string

totalHoldingBalance

持倉盈虧金额

string

---

## 第 63 页

totalHoldingBalancePercent

持倉盈虧占比

string

withdrawBalance

可取金额

string

msg

状态信息

string

回应示例

{

"code": 0,

"data": [

{

"asset": "",

"enableBalance": "",

"frozenBalance": "",

"marketValue": "",

"onWayBalance": "",

"stockHoldingList": [

{

"costPrice": "",

"costPriceAccurate": "",

"currentAmount": "",

"dailyBalance": "",

"dailyBalancePercent": "",

---

## 第 64 页

"enableAmount": 0,

---

## 第 65 页

"exchangeType": 0,

"frozenAmount": 0,

"hisMarketValue": "",

"holdingBalance": "",

"holdingBalancePercent": "",

"lastPrice": "",

"marketValue": "",

"oddAmount": "",

"quoteType": "",

"stockCode": "",

"stockName": ""

}

],

"stockOnWayBalanceDTOList": [

{

"applyType": 0,

"applyTypeName": "",

"exchangeType": 0,

"moneyType": 0,

"onWayBalance": 0,

"stockCode": "",

---

## 第 66 页

"stockName": ""

---

## 第 67 页

}

],

"totalDailyBalance": "",

"totalDailyBalancePercent": "",

"totalHoldingBalance": "",

"totalHoldingBalancePercent": "",

"withdrawBalance": ""

}

],

"msg": ""

}

2.14 查询聚合资产信息

接口地址 /aggregation-server/open-api/user-asset-aggregation/v1

请求方式 POST

consumes ["application/json"] produces
["application/json"] 介 面 描 述 需要
token

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

---

## 第 68 页

X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止
重複提交实现接口冪等

header

true

string

X-Sign

RSA 签名

header

true

string
exchangeType

交易类别，0-港股，5-美股，67-A 股

body

true

int32

请求 header 示例

Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiOTMyYmFjY2U3MGU3
NDgwM2JmNjYxODk0OTM3ZDlkN2QiLCJzb3VyY2UiOiJ3ZWIiLCJ1dWlkIjozNDMwMjExNDU2ODI4NjIwODB
9.XiF0eWAmeL-pthTg--5SLObnscJcDYHaJTJZTHAucwQ
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Channel：100082
X-Request-Id: 928239187123721231232

X-Sign：body 使用 RSA 私密密钥加密

回应状态

状态码

说明

schema

0

成功

ResponseVO

200

OK

ResponseVO«OpenHoldAsset»

108008

user 服务不可用

108011

使用者信息查询接口异常

108027

stock-order 服务不可用

108028

调用客户股票资产查询接口异常

---

## 第 69 页

108029

finance-server 服务不可用

108030

获取当前客户基金持倉清单接口异常

108031

获取当前客户債券持倉清单接口异常

回应参数

参数名称

说明

类型

schema

Code

回应码 0-请求成功

int32

Data

回应體

object

OpenHoldAsset

asset

总资产

string

bondMarketValue

債券市值

string

enableBalance

可用金额

string

frozenBalance

冻结金额

string

fundMarketValue

基金市值

string

onWayBalance

在途资金

string

stockMarketValue

股票市值

string

withdrawBalance

可取金额

string

totalHoldingBalance

持倉盈虧金额

string

msg

回应内容

string

{

"code": 0,

"msg": "请求成功",
"data": {
"asset": "997457.66",

---

## 第 70 页

"stockMarketValue": "88165.000000",

"bondMarketValue": "0.00",

"fundMarketValue": "0.00",

"enableBalance": "908484.60",

"withdrawBalance": "908484.60",

"frozenBalance": "808.060000",

"onWayBalance": "0.00",

"totalHoldingBalance": "-2510.00"

}

}

3 IPO

3.1 获取 IPO 列表-分页查询

接口地址 /stock-order-server/open-api/ipo-list

请求方式 POST

consumes ["application/json"]

produces ["*/*"]
接口描述 获取 IPO 清单（不需要登陸）

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道

header

true

string

---

## 第 71 页

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

status

Tab 页类别(0-认購中，1-待上市)

body

true

int32

pageNum

当前页 1 开始, 预设值 1

body

false

int32

pageSize

每页结果数, 预设值 10

body

false

int32

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"pageNum": 1,
"pageSize": 10,
"status": 1
}

回应状态

状态码

说明

schema

200

OK

ResponseVO«PageInfoVO«AppGetIpoListResponse»»

201

Created

401

Unauthorized

403

Forbidden

404

Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 PageInfoVO«Open
ApiGetIpoListResp
PageInfoVO«OpenA
piGetIpoListRespons

---

## 第 72 页

onse»

e»

list

结果集合

array OpenApiGetIpoList
Response

bookingRatio

认購倍数

number

endTime

现金认購结束时间

yyyy-MM-dd HH:mm:ss

string

englishName

新股英文名

string

exchangeType

市場类型(0-港股)

int32

financingEndTime

融资认購结束时间

string

financingMultiple

融资倍数

int32

ipoId

IPO id

string

labelStatus

标签状态(0-已认購,1-已中签,2-未中签)

int32

latestEndtime 最晚认購截止时间(國際认購、融资认購
和现金认購截止时间最晚的时间)

string

leastAmount

起購金额

number

listingPrice

最终上市价格

number

listingTime

上市交易时间

string

moneyType

币種类型(0-人民币，1-美元，2-港币)

int32

priceMax

最高招股价

number

priceMin

最低招股价

number

publishTime

公佈中签日期

string

remainingTime

认購剩余时间（秒）

int64

serverTime

伺服器时间

string

status 新股状态 (0-待认購， 1-认購中， 2-待扣
款，3-已扣款待确认，4-已确认待公佈，
5-已公佈待上市， 6-已上市， 7-取消上
市，8-暫緩上市，9-延遲上市)

int32

statusName

状态中文名

string

stockCode

新股代码

string

stockName

新股名称

string

subscribeWay

认購方式，多種认購用 ,隔开，比如 0,1

支持现金和融资 (1-公开现金认購， 2-公

string

---

## 第 73 页

开融资认購，3-國際配售)-这个字段可以
判断是否支援融资认購

successRate

中签率

number

pageNum

当前页

int32

pageSize

每页条数

int32

total

总数

int64

msg

状态信息

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"pageNum": 1,
"pageSize": 20,
"total": 2,
"list": [{
"ipoId": "1143834475048767488",
"stockCode": "02099",
"exchangeType": 0,
"status": 1, "statusName": "认購
中",
"stockName": "中國黃金國際",
"englishName": "CHINAGOLDINTL",
"leastAmount": null, "priceMin": 7,
"priceMax": 11,
"listingPrice": 10,
"endTime": "2019-06-27",
"financingEndTime": null, "latestEndtime":
"2019-06-27",
"remainingTime": -1, "labelStatus":
null, "successRate": null,
"bookingRatio": null, "publishTime":
"2019-07-01",
"listingTime": "2019-07-02",
"moneyType": 2,

---

## 第 74 页

"serverTime": "2019-10-09 21:08:21",
"subscribeWay": "1",
"financingMultiple": 3
},
{
"ipoId": "1133576191818039296",
"stockCode": "00994",
"exchangeType": 0,
"status": 1, "statusName": "认購
中",
"stockName": "中天宏信",
"englishName": "CT VISION",
"leastAmount": null, "priceMin": 7,
"priceMax": 10,
"listingPrice": 9,
"endTime": "2019-07-29",
"financingEndTime": null, "latestEndtime":
"2019-07-29",
"remainingTime": -1,
"labelStatus": null,
"successRate": null,
"bookingRatio": 0,
"publishTime": "2019-07-30",
"listingTime": "2019-07-31",
"moneyType": 2,
"serverTime": "2019-10-09 21:08:21",
"subscribeWay": "1",
"financingMultiple": 1
}
]
}
}

3.2 获取新股詳細信息

接口地址 /stock-order-server/open-api/ipo-info

请求方式 POST

consumes ["application/json"]

produces ["*/*"]
接口描述 获取新股詳細信息

---

## 第 75 页

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道 ID，由盈立分配

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

exchangeType

市場类型(0-HK,5-US),如果 ipoId 不传，該字段必传

body

false

int32

ipoId 新股 id [ 与(stockCode&exchangeType 不能同时为空 )],
当  ipoId 有  值  ，  優  先  取  ipoId 查  询  ，
stockCode&exchangeType 条件不生效

body

false

int64

stockCode

股票代码,如果 ipoId 不传，該字段必传

body

false

string

回应状态
状态码 说明 schema
200 OK ResponseVO«appIpoInfoResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例
{
"ipoId": 1133576191528632320
}

回应参数

---

## 第 76 页

参数名称

说明

类型

schema

code

状态码

int32

data

返回體 appIpoInfoResp
onse
appIpoInfoRes
ponse

applied

用户是否已认購

boolean

beginTime

现金认購开始时间

string

bookingFee

现金认購手續費

number

bookingRatio

认購倍数

number

compFinancingSurplus

公司融资额度淨余

number

depositRate

融资比例

number

ecmEndTime

國際认購截止时间

date-time

ecmStatus ecm 新股状态(0- 待认購,1- 认購中， 2- 待扣
款，3-待扣款[未全部扣款成功 ]，4-待提交，
5-待分配，6-待返款，7-待返款[未全部返款成
功]，8-待返券，9-待返券[未全部返券成功]，
10-待 CCASS 确认，11-待上市，12-已上市，
13-暫停认購)

int32

endTime

现金认購结束时间

string

englishName

新股英文名

string

exchangeType

交易类别(0-HK,5-US)

int32

exchangeTypeName

交易类别名称

string

financingEndTime

融资认購截止时间

date-time

financingFee

融资手續費

number

financingMultiple

融资倍数

int32

financingTips

融资认購溫馨提示

string

greyFlag

是否支持暗盤（0-不支持，1-支持）

int32

greyTimeBegin

暗盤交易时间段开始，格式 HH:mm:ss

string

greyTimeEnd

暗盤交易时间段结束，格式 HH:mm:ss

string

greyTradeDate

暗盤交易日，格式 yyyy-MM-dd

string

handAmount

每手股数

number

interestBeginDate

融资认購/計息开始时间

date-time

interestDay

計息天数

int32

---

## 第 77 页

interestEndDate

融资計息结束时间

date-time

interestRate

默认融资利率

number

ipoFinancingRatios 融   资   階   梯   利   率   (json   陣
列 :[{"financing_amount_begin": 初 始 认 購 金
额  ,"financing_amount_end": 结  束  认  購  金
额 ,"interest_rate": 利率 ,"exchange_type":市場类
型,"stock_code":"新股代码"}])

array

IpoFinancingR
atio

exchange_type

市場类型

int32

financing_amount_begin

初始认購金额

number

financing_amount_end

结束认購金额

number

interest_rate

利率

number

stock_code

新股代码

string

ipoId

IPO id

string

latestEndtime 最晚认購截止时间(國際认購、融资认購和现
金认購截止时间最晚的时间)

string

leastAmount

起購金额(一手认購金额)

number

listingPrice

最终上市价格

number

listingTime

上市交易时间

string

marketValueMax

市值最大值

number

marketValueMin

市值最小值

number

moneyType

币種类型(0-人民币，1-美元，2-港币)

int32

officialBegin

官方招股开始时间

string

officialEnd

官方招股结束时间

string

priceMax

最高招股价

number

priceMin

最低招股价

number

prospectusLink

招股書连结

string

publishQuantity

发行股本

number

publishTime

公佈中签日期

string

qtyAndCharges 档位元信息(json 陣列:[{"allotted_amount": 中签
金    额    ,"applied_amount":   申    購  金
额    ,"exchange_type":      市    場    类
型,"shared_applied":申購数量,"stock_code":"新

array

IpoQtyAndCha
rges

---

## 第 78 页

股代码"," leastCash ":档位对应的最少使用现
金}])

allotted_amount

中签金额

number

applied_amount

申購金额

number

exchange_type

市場类型

int32

leastCash

档位对应的最少使用现金

int32

shared_applied

申購数量

number

stock_code

新股代码

string

remainingTime

认購剩余时间（秒）

int64

serverTime

伺服器时间

string

sponsor

保薦人

string

status 新股状态(0-待认購，1-认購中，2-待扣款，3-
已扣款待确认，4-已确认待公佈，5-已公佈待
上市，6-已上市，7-取消上市，8-暫緩上市，
9-延遲上市)

int32

statusName

状态中文名

string

stockCode

新股代码

string

stockIntroduction

股票介紹

string

stockName

新股名称

string

subscribeWay 认購方式，多種认購用 ,隔开，比如  1,2 支持
现金和融资 (1-公开现金认購， 2-公开融资认
購，3-國際配售)-这个字段可以判断是否支援
融资认購

string

successRate

中签率

number

tips

现金认購溫馨提示

string

totalQuantity

总股本

number

updateTime

更新时间

string

msg

状态信息

string

回应示例
{
"code": 0,
"msg": "操作成功",
"data": {

---

## 第 79 页

"ipoId": "1143834475048767488",
"stockCode": "02099", "stockName": "
中國黃金國際", "status": 1,
"exchangeType": 0,
"moneyType": 2,
"handAmount": null,
"bookingFee": 10,
"beginTime": "2019-06-25 09:00:00",
"endTime": "2019-06-27 12:00:00",
"publishTime": "2019-07-01 00:00:00",
"listingTime": "2019-07-02 00:00:00",
"listingPrice": null, "priceMin": null,
"priceMax": 11, "financingEndTime":
null, "interestBeginDate": null,
"interestEndDate": null,
"officialBegin": "2019-06-25 09:00:00",
"officialEnd": "2019-06-28 12:00:00",
"leastAmount": null, "successRate":
null, "bookingRatio": null, "sponsor":
"", "publishQuantity": null,
"totalQuantity": null,
"marketValueMin": null,
"marketValueMax": null,
"prospectusLink": "Http://",
"qtyAndCharges": [{
"stock_code": "2099",
"exchange_type": 0,
"shared_applied": 100,
"applied_amount": 1111.09,
"allotted_amount": 0
}],
"ipoFinancingRatios": [{
"stock_code": "2099",
"exchange_type": 0,
"financing_amount_begin": 1000,
"financing_amount_end": 10000,
"interest_rate": 0.5
},
{

---

## 第 80 页

"stock_code": "2099",
"exchange_type": 0,
"financing_amount_begin": 10001,
"financing_amount_end": 20000,
"interest_rate": 0.7
}
],
"financingMultiple": 3,
"depositRate": 0.7, "financingFee": null,
"interestDay": 0, "interestRate": null,
"compFinancingSurplus": null,
"subscribeWay": "1"
}
}

3.3ipo 新股认購

接口地址 /stock-order-server/open-api/apply-ipo

请求方式 POST

consumes ["application/json"]

produces ["*/*"]

接口描述 ipo 新股认購

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Dt 设備类型(t1-android，t2-ios，t3-其他，t4-
Windows,t5-Mac)

header

true

string

X-Request-Id 頭部信息的 requestId 信息，确保唯一，
防止重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

---

## 第 81 页

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

applyQuantity

认購数量

body

true

number

applyType

认購类型(1-现金，2-融资)

body

true

int32

ipoId

ipo 交易系统唯一编號

body

true

int64
serialNo 流水號，最长 19 位，确保唯一推薦雪花
算法生成

body

true

int64

cash

认購现金(融资认購时必填)

body

false

number

请求 header 示例

Authorization:eyJ0eXAiOiJKV1Qi LCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZ
iNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密’;

请求 body 示例

{
"applyQuantity": 100,
"applyType": 1,
"cash": 0,
"ipoId": 1133576191818039296,
"serialNo": 1182189250463484234
}

回应状态

状态码 说明 schema
200 OK ResponseVO«IpoApplyResponse»
201 Created

---

## 第 82 页

401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称 说明 类型 schema
code 状态码 int32
data 返回體 IpoApplyResponse IpoApplyResponse
applyId 申購 id string
status 申購状态(0-已提交,1-已认購,2-等待改单, 3-等待撤
銷,4-已撤銷,5-已扣款,6-待公佈中签 ,7-全部中签 ,8-
部分中签,9-未中签,10-认購失敗)
int32
msg 状态信息 string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1182192040986583040",
"status": 1
}
}

3.4ipo 改单/撤单

接口地址 /stock-order-server/open-api/modify-ipo

请求方式 POST

consumes ["application/json"]

produces ["*/*"]

接口描述 ipo 改单/撤单

---

## 第 83 页

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Request-Id 頭部信息的 requestId 信息，确保唯一，防止
重複提交实现接口冪等

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

actionType

操作类型 0-改单,1-撤单

body

true

int32

applyId

认購記录 Id

body

true

int64

applyQuantity

认購数量

body

true

number

cash

认購现金(改融资认購单，必填)

body

false

number

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

{
"actionType": 1,
"applyId": 1182192040986583040,
"applyQuantity": 0,
"cash": 0
}

回应状态

状态码 说明 schema
200 OK ResponseVO«IpoApplyResponse»

---

## 第 84 页

201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回应参数

参数名称 说明 类型 schema
code 状态码 int32

data 返回體 IpoApplyResponse IpoApplyResponse
applyId 申購 id string

status 申購状态(0-已提交,1-已认購,2-等待改单,
3-等待撤銷 ,4-已撤銷 ,5-已扣款 ,6-待公佈
中签 ,7- 全部中签 ,8- 部分中签 ,9- 未中
签,10-认購失敗)
int32

msg 状态信息 string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1182192040986583040",
"status": 4
}
}

3.5 获取客户 ipo 申購清单-分页查询

接口地址 /stock-order-server/open-api/ipo-record-list

请求方式 POST

consumes ["application/json"]

produces ["*/*"]

接口描述 获取客户 ipo 申購清单

---

## 第 85 页

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Channel

渠道

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

applyTimeMin 认 購 开 始 时 間 ， 格 式 :yyyy-MM-dd
HH:mm:ss

body

false

string

applyTimeMax 认 購 结 束 时 間 ， 格 式 :yyyy-MM-dd
HH:mm:ss

body

false

string

pageNum

当前页 1 开始，预设值 1

body

false

int32

pageSize

每页结果数，预设值 10

body

false

int32

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求示例

{
"pageNum": 1,
"pageSize": 10,
"applyTimeMin":"2019-10-12 00:00:00",
"applyTimeMax":"2020-01-30 00:00:00"
}

回应状态

状态码

说明

schema

200

OK

ResponseVO«PageInfoVO«IpoRecordListResponse»»

---

## 第 86 页

201

Created

401

Unauthorized

403

Forbidden

404

Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

PageInfoVO«IpoRe
cordListResponse»

PageInfoVO«IpoR
ecordListResponse
»

list

结果集合

array IpoRecordListRes
ponse

allottedQuantity

中签股数

number

applyAmount

认購总金额(包含手續費，不包含利息)

number

applyId

申请编號

string

applyQuantity

认購股数

number

applyType

认購类型(1-现金，2-融资)

int32

applyTypeName

认購类型(1-现金认購，2-融资认購)

string

priceMax

最高招股价

number

priceMin

最低招股价

number

listingPrice

最终上市价格

number

cash

认購现金

number

exchangeType

市場类型(0-HK,5-US)

int32

financingAmount

融资利息

number

financingBalance

融资金额

number

interestRate

融资利率

number

labelCode 状态标签码 (0-待系统确认 ,1-已认購 ,4-已撤
銷,6-待公佈中签 ,7-已中签 ,9-未中签 ,10-认購
失敗)

int32

moneyType

币種类型(0-人民币，1-美元，2-港币)

int32

publishTime

公佈中签日期

string

---

## 第 87 页

listingTime

上市交易时间(YYYY-MM-DD)

serverTime

伺服器时间

string

status 认購状态 (0-已提交 ,1-已认購 ,2-等待改单 , 3 -
等待撤銷,4-已撤銷,5-已扣款,6-待公佈中签 ,7-
全部中签,8-部分中签,9-未中签,10-认購失敗)

int32

statusName

认購状态名称

string

stockCode

股票代码

string

stockName

股票名称

string

pageNum

当前页

int32

pageSize

每页条数

int32

total

总数

int64

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"pageNum": 1,
"pageSize": 0,
"total": 34,
"list": [{
"applyId": "1147036407112679424",
"applyType": 2, "applyTypeName": "
融资认購", "stockName": "香港中华
煤氣", "stockCode": "00003",
"exchangeType": 0,
"status": 10, "statusName": "认購
失敗", "applyQuantity": 200,
"applyAmount": 4140.31, "cash": null,
"financingBalance": null, "interestRate":
null, "priceMin": 10,
"priceMax": 20,
"listingPrice": 13,
"financingAmount": 1.75,

---

## 第 88 页

"allottedQuantity": 0,
"publishTime": "2019-07-05 00:00:00",
"serverTime": null, "moneyType": 2,
"labelCode": 10
},
{
"applyId": "1147018860570537984",
"applyType": 2, "applyTypeName": "
融资认購", "stockName": "香港中华
煤氣", "stockCode": "00003",
"exchangeType": 0,
"status": 4, "statusName": "已撤
銷", "applyQuantity": 200,
"applyAmount": 4140.31, "cash": null,
"financingBalance": null, "interestRate":
null, "priceMin": 10,
"priceMax": 20,
"listingPrice": 13,
"financingAmount": 1.75, "allottedQuantity": null,
"publishTime": "2019-07-05 00:00:00",
"serverTime": null,
"moneyType": 2,
"labelCode": 4
}
]
}
}

3.6 获取客户 ipo 申購明細

接口地址 /stock-order-server/open-api/ipo-record

请求方式 POST

consumes ["application/json"]

---

## 第 89 页

produces ["*/*"]

接口描述 获取客户 ipo 申購明細

请求参数

参数名称

说明

请求类型

必填

类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

X-Channel

渠道

header

true

string

applyId

申購编號(传其中一个即可)

body

false

int64

serialNo

流水號(传其中一个即可)

body

false

int64

请求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求示例

{
"applyId": 1147036407112679424,
"serialNo": 1233123554314
}

回应状态

状态码

说明

schema

200

OK

ResponseVO«IpoRecordResponse»

201

Created

401

Unauthorized

---

## 第 90 页

403

Forbidden

404

Not Found

回应参数

参数名称

说明

类型

schema

code

状态码

int32

data

返回體

IpoRecordR
esponse

IpoRecordRes
ponse

allottedQuantity

中签股数

number

applyAmount

认購总金额(包含手續費，不包含利息)

number

applyId

申请编號

string

applyQuantity

认購股数

number

applyType

认購类型(1-现金，2-融资)

int32

applyTypeName

认購类型(1-现金认購，2-融资认購)

string

cash

认購现金

number

channel

渠道类型(1-APP 提交，2-中台提交，99-其它)

int32

createTime

认購提交时间

string

deductStatus

扣款状态(0-已冻结，1-已扣款，2-已解冻)

int32

deductStatusName

扣款状态名

string

endTime

当前认購方式截止时间

string

exchangeType

市場类型(0-HK,5-US)

int32

failReason

认購失敗原因

string

financingAmount

融资利息

number

financingBalance

融资金额

number

handlingFee

手續費

number

interestDay

計息天数

int32

interestRate

融资利率

number

ipoId

ipo 编號

string

ipoStatus

新股状态(0-待认購，1-认購中，2-待扣款，3-已扣
款待确认，4-已确认待公佈，5-已公佈待上市，6-

int32

---

## 第 91 页

已上市，7-取消上市，8-暫緩上市，9-延遲上市)

labelCode

状态标签码(0-待系统确认,1-已认購,4-已撤銷,6-待公
佈中签,7-已中签,9-未中签,10-认購失敗)

int32

moneyType

币種类型(0-人民币，1-美元，2-港币)

int32

publishTime

公佈中签日期 yyyy-MM-dd HH:mm:ss

string

refundAmount

退款金额

number

refundFlag

退款状态(0-无退款，1-待退款，2-已退款)

int32

serverTime

伺服器时间

string

status

认購状态(0-已提交,1-已认購,2-等待改单, 3 -等待撤
銷,4-已撤銷 ,5-已扣款 ,6-待公佈中签 ,7-全部中签 ,8-
部分中签,9-未中签,10-认購失敗)

int32

statusName

认購状态名称

string

stockCode

股票代码

string

stockName

股票名称

string

listingTime

上市时间 yyyy-MM-dd

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1178190341147189248",
"applyType": 1, "applyTypeName": "现
金认購", "stockName": "新城市建设发
展", "stockCode": "00456",
"exchangeType": 0,
"status": 4, "statusName": "已撤銷
", "applyQuantity": 1900.00,
"applyAmount": 34544.6300, "cash": null,
"financingBalance": null, "interestRate":
null, "financingAmount": 0.0000,
"allottedQuantity": null,
"publishTime": "2019-10-03 00:00:00",

---

## 第 92 页

"serverTime": "2019-11-01 20:33:55",
"moneyType": 2,
"labelCode": 4,
"createTime": "2019-09-29 14:10:42",
"deductStatus": 2, "deductStatusName":
"已解冻", "refundFlag": 0,
"refundAmount": null, "handlingFee":
0.0000, "failReason": null,
"endTime": "2019-09-30 11:18:00",
"ipoId": "1178148950262435840",
"interestDay": 0,
"channel": 1,
"listingTime": "2019-10-04",
"ipoStatus": 6
}
}

4 资金

4.1 查询汇率

接口地址 /stock-capital-server/open-api/currency-exchange-info

请求方式 POST

consumes ["application/json"]

produces ["*/*"]
接口描述

请求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密密钥加密

请求 body 示例

---

## 第 93 页

请求参数
参数名称 说明 请求类型 必填 类型

Authorization

頭部信息的 token 信息

header

true

string

X-Lang

語言类别(1-简體，2-繁體，3-English)

header

true

string

X-Time

时间标記

header

true

string

X-Sign

RSA 签名

header

true

string

X-Channel

渠道

header

true

string

回应状态
状态码 说明 schema
200 OK CapitalResponseVO«FetchExchangeRateResp»
201 Created

401 Unauthorized

403 Forbidden

404 Not Found

回应参数

参数名称

说明

类型

code

状态码

int32

data

返回體

array

baseMoneyType

基準币種，0:人民币 1：美元 2：港币

int32

sourceCurrency

源币種，0:人民币 1：美元 2：港币

int32

targetCurrency

目标币，0:人民币 1：美元 2：港币

int32

yxBuyRate

盈立买入汇率

number

yxSellRate

盈立卖出汇率

number

bocSellRate

中銀卖出汇率

number

bocBuyRate

中銀买入汇率

number

msg

状态信息

string

回应示例

{
"code": 0,
"msg": "操作成功",

---

## 第 94 页

5 资料字典

5.1 订单状态（Status）

编码 名称

-1

失敗

0

全部成交
"data": [
{
"sourceCurrency": 1,
"targetCurrency": 2,
"yxSellRate": 7.842,
"yxBuyRate": 7.8133,
"bocSellRate": 7.842,
"bocBuyRate": 7.8133,
"baseMoneyType": 1
},
{
"sourceCurrency": 0,
"targetCurrency": 2,
"yxSellRate": 90.335,
"yxBuyRate": 91.235,
"bocSellRate": 90.33,
"bocBuyRate": 91.24,
"baseMoneyType": 0
},
{
"sourceCurrency": 1,
"targetCurrency": 0,
"yxSellRate": 7.0817,
"yxBuyRate": 7.0148,
"bocSellRate": 7.0817,
"bocBuyRate": 7.0148,
"baseMoneyType": 1
}
]
}

---

## 第 95 页

1

等待提交

2

待成交

3

部分成交

4

等待撤单

5

等待改单

6

已撤单

7

部成撤单

8

废单

5.2 市場类型（ExchangeType）

编码 名称

0

港股

1

上海 A

2

上海 B

3

深圳 A

4

深圳 B

5

美股

6

滬港通

7

深港通

67

A 股（用于查询）

100

所有市場（用于查询）

---

## 第 96 页

5.3IPO 状态（Status）

编码

名称

0

待认購

1

认購中

2

待扣款

3

已扣款待确认

4

已确认待公佈

5

已公佈待上市

6

已上市

7

取消上市

8

暫緩上市

9

延遲上市

11

已刪除
5.4 币種（moneyType）

编码

名称

0

人民币

1

美元

2

港币
5.5 设備类别（X-Dt）

编码

名称

---

## 第 97 页

t1

安卓

t2

Ios

t3

其它

t4

Windows

t5

Mac

---
