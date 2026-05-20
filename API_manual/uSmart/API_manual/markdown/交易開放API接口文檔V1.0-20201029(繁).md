# 交易開放API接口文檔V1.0-20201029(繁)

- 来源 PDF：`../交易開放API接口文檔V1.0-20201029(繁).pdf`
- 页数：97
- 转换说明：自动文本抽取，保留页码分隔；接口字段、表格和示例代码请与原 PDF 交叉核对。

---

## 第 1 页

交易開放 API 介面文檔
V 1 . 0

概述

開放平台可以為個人開發者和機構客戶提供介面服務，投資者可以充分的利用盈立智
投的交易服務、報價服務、帳戶服務等實現自己的投資操作。

接入說明：

IP 白名單，授權訪問開放平台介面的 IP 位址，只有在白名單內的 IP 才能訪問服務。

協議：

HTTPS

X-Sign

使用 MD5withRSA 加密演算法對 Body 中的內容進行加密，得到的密文經過 safeBase64 編碼
後做為 X-Sign 的值放入 header 當中，每一個管道單獨分配公私密金鑰。

驗簽測試公開金鑰為：

需雙方商定

隱私資料加密測試公開金鑰為：

需雙方商定

URLSAFE_BASE64 演算法在 RFC4648 中有定義

最終串會使用 RSA 私密金鑰進行加密，之後使用 RFC4648 演算法編碼放入請求體或表
單項中。

請求頭 X-Request-Id:

---

## 第 2 页

長度為 19 位元數位，必須確保唯一用於做冪等防重，推薦使用分散式 Snowflake 雪花算法
生成。

請求示例：

http header 參數示例

Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiNGZjYTA1MWNmZjQ
wNDI4NzlkNGJiYzYzYjFiYWE0MTgiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozMTgxNDA2MTEwNTc1NTc1MD
R9.gw4_AKh6NGUxWXWjzHb8G2An3ao0nSuI
Content-Type: application/json; charset=utf-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 92823918712371
X-Type: 1
X-Channel：1001
x-Sign：用私密金鑰對 body 內容加密後的內容

http body 參數示例：

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

1 用戶

1.1 管道密碼登錄
手機+密碼+管道登錄：

介面位址 /user-server/open-api/login

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

請求參數說明：

參數名稱  說明  請求類型  必填  類型

X-Lang

語言類別(1-簡體，2-繁體，
3-English)

header

true

string

X-Request-Id

頭部資訊的  requestId 資訊,長
度 30 位，確保唯一，防止重
複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

簽名

header

true

string

areaCode

區域號 86 中國， 852 香港，
853 中國澳門，  886 中國 台
灣，65 新加坡

body

true

string

password

密碼 RSA 加密（與 X-Sign 不
同秘鑰）

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

手機號 RSA 加密（與 X-Sign
不同秘鑰）

body

true

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例：

{
"areaCode": 86, "password":
"rsa", "phoneNumber": "rsa"
}

參數說明：

參數名稱  說明  類型
areaCode  區號  string
avatar  頭像地址  string
expiration  過期時間  int64
extendStatusBit  用戶擴展狀態  int32
firstLogin  是否為第一次登陸  boolean
nickname  昵稱  string
openedAccount  是否開戶  boolean
phoneNumber  手機號  string
thirdBindBit  綁定位 手機 1<<0 微信 1<<1 微博 1<<2  int32
token  登錄授權的 token  string
tradePassword  是否設置過交易密碼  boolean
unionId  微信公眾平台的 unionId，如果有則顯示。  string
uuid  盈立用戶註冊的 uuid，全域唯一  int64

返回示例：

---

## 第 5 页

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
"nickname": "xxx", "openedAccount":
true, "phoneNumber": "188xxxx9188",
"thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回應狀態

狀態碼  說明
0  成功
200  OK
300100  非法請求
300102  帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服
300103  用戶被刪除
300309  請輸入正確的手機號碼
300701  該手機號沒有註冊
300702  密碼錯誤次數過多帳號已鎖定，請%s 分鐘後重新登錄或找回密碼
300703  密碼錯誤，請重新輸入，您還可以嘗試%s 次
300705  該帳戶未設置登錄密碼，請使用短信驗證碼登錄
300809  需要校驗手機短信驗證碼
1.2 獲取手機驗證碼
介面位址 /user-server/open-api/send-phone-captcha

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

請求參數說明：

參數名稱  說明  請求類型  必填  類型

X-Lang

語言類別(1-簡體，2-繁體，
3-English)

header

true

string

---

## 第 6 页

X-Request-Id

頭部資訊的  requestId 資訊,長
度 30 位，確保唯一，防止重
複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

簽名

header

true

string

areaCode

區域號 86 中國， 852 香港，
853 中國澳門，  886 中國臺
灣，65 新加坡

body

true

string

type

驗證碼類型 101 註冊 102 重置
密碼 103 更換手機號 104 綁定
手機號  105 新設備登錄 校驗
106 短信登錄

body

true

string

phoneNumber

手機號 RSA 加密（與 X-Sign
不同秘鑰）

body

true

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例：

{
"areaCode": 86,
"type": 102,
"phoneNumber": "rsa"
}

---

## 第 7 页

出參說明：

參數名稱  說明  類型
areaCode  區號  string
avatar  頭像地址  string
expiration  過期時間  int64
extendStatusBit  用戶擴展狀態  int32
firstLogin  是否為第一次登陸  boolean
invitationCode  邀請碼，如果有，則顯示。  string
languageCn  1 簡體 2 繁體  int32
languageHk  1 簡體 2 繁體  int32
lineColorHk  1 紅漲綠跌 2 綠漲紅跌  int32
nickname  昵稱  string
openedAccount  是否開戶  boolean
phoneNumber  手機號  string
thirdBindBit  綁定位 手機 1<<0 微信 1<<1 微博 1<<2  int32
token  登錄授權的 token  string
tradePassword  是否設置過交易密碼  boolean
unionId  微信公眾平台的 unionId，如果有則顯示。  string
uuid  盈立用戶註冊的 uuid，全域唯一  int64

返回示例：

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
"invitationCode": 1234,
"languageCn": 0,
"languageHk": 0,
"lineColorHk":  0, "nickname": "xxx",
"openedAccount": true, "phoneNumber":
"188xxxx9188", "thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回應狀態

狀態碼  說明
0  成功

---

## 第 8 页

200  OK
300100  非法請求
300102  帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服
300103  用戶被刪除
300309  請輸入正確的手機號碼
300701  該手機號沒有註冊
300702  密碼錯誤次數過多帳號已鎖定，請%s 分鐘後重新登錄或找回密碼
300703  密碼錯誤，請重新輸入，您還可以嘗試%s 次
300705  該帳戶未設置登錄密碼，請使用短信驗證碼登錄
300809  需要校驗手機短信驗證碼

1.3 管道驗證碼登錄
手機+驗證碼+管道登錄：

介面位址 /user-server/open-api/loginCaptcha

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

請求參數說明：

參數名稱  說明  請求類型  必填  類型

X-Lang

語言類別(1-簡體，2-繁體，
3-English)

header

true

string

X-Request-Id

頭部資訊的  requestId 資訊,長
度 30 位，確保唯一，防止重
複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

簽名

header

true

string

areaCode

區域號 86 中國， 852 香港，
853 中國澳門，  886 中國臺
灣，65 新加坡

body

true

string

captcha

驗證碼

body

true

string

phoneNumber

手機號 RSA 加密（與 X-Sign

body

true

string

---

## 第 9 页

不同秘鑰）

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例：

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

參數說明：

參數名稱  說明  類型
areaCode  區號  string
avatar  頭像地址  string
expiration  過期時間  int64
extendStatusBit  用戶擴展狀態  int32
firstLogin  是否為第一次登陸  boolean
invitationCode  邀請碼，如果有，則顯示。  string
languageCn  1 簡體 2 繁體  int32
languageHk  1 簡體 2 繁體  int32
lineColorHk  1 紅漲綠跌 2 綠漲紅跌  int32
nickname  昵稱  string
openedAccount  是否開戶  boolean
phoneNumber  手機號  string
thirdBindBit  綁定位 手機 1<<0 微信 1<<1 微博 1<<2  int32
token  登錄授權的 token  string

---

## 第 10 页

tradePassword  是否設置過交易密碼  boolean
unionId  微信公眾平台的 unionId，如果有則顯示。  string
uuid  盈立用戶註冊的 uuid，全域唯一  int64

返回示例：

{
"areaCode": 86,
"avatar": "",
"expiration": 0,
"extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
"invitationCode": 1234,
"languageCn": 0,
"languageHk": 0,
"lineColorHk":  0, "nickname": "xxx",
"openedAccount": true, "phoneNumber":
"188xxxx9188", "thirdBindBit": 1,
"token": "", "tradePassword":
true, "unionId":  "", "uuid": 0
}

回應狀態

狀態碼  說明
0  成功
200  OK
300100  非法請求
300102  帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服
300103  用戶被刪除
300309  請輸入正確的手機號碼
300701  該手機號沒有註冊
300702  密碼錯誤次數過多帳號已鎖定，請%s 分鐘後重新登錄或找回密碼
300703  密碼錯誤，請重新輸入，您還可以嘗試%s 次
300705  該帳戶未設置登錄密碼，請使用短信驗證碼登錄
300809  需要校驗手機短信驗證碼

---

## 第 11 页

1.4 設置交易密碼

介面位址 /user-server/open-api/set-trade-password

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 需帶登錄態 token 使用者需要完成開戶，且未設置過交易密碼，否則算非法請求

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言 1 簡體 2 繁體

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password 交易密碼 設置、修改、重置交易密碼必填，交易
密碼必須是 6 位元純數位 RSA 加密（與 X-Sign 不
同秘鑰）

body

true

string

oldPassword 舊交易密碼 修改交易密碼必填，交易密碼必須是
6 位元純數位 RSA 加密（與 X-Sign 不同秘鑰）

body

false

string

phoneCaptcha

手機驗證碼，根據驗證碼重置交易密碼必填

body

false

string

請求 header 示例

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
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"oldPassword": "",
"password": "", "phoneCaptcha":
""
}

回應狀態

狀態碼 說明 schema
0 成功
200 OK UserResponseEntity
300100 非法請求
300101 非法 TOKEN
301001 交易密碼需為 6 位元純數字，請重新輸入
301003 交易密碼錯誤，請重新輸入，您還可以嘗試%s 次
301004 交易服務異常
301005 帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{
"code": 0,
"data": {},
"msg": ""

---

## 第 13 页

}

1.5 校驗交易密碼

介面位址 /user-server/open-api/check-trade-password

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 許可權：需要 Token

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Request-Id

頭部資訊的 requestId 資訊， 19 位元長度

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password

交易密碼必須是 6 位元純數位 RSA 加密

（與 X-Sign 不同秘鑰）

String

false

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

---

## 第 14 页

請求示例

/user-server/open-api/check-trade-password?password=123456 RES 加密

回應狀態

狀態碼 說明 schema
0 成功
200 OK UserResponseEntity
300100 非法請求
300101 非法 TOKEN
301001 交易密碼需為 6 位元純數字，請重新輸入
301002 錯誤次數過多交易密碼已鎖定，請%s 小時後重新嘗試或找回
密碼

301004 交易服務異常
310104 交易密碼錯誤
310106 未設置交易密碼

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{
"code": 0,
"data": {},
"msg": ""
}

1.6 重置登錄密碼

介面位址 /user-server/open-api/reset-login-password

---

## 第 15 页

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 不需要 token

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

areaCode 區域號 86 中國，852 香港，853 中國澳門，886 中
國臺灣，65 新加坡

body

false

string

password

新密碼 RSA 加密（與 X-Sign 不同秘鑰）

body

false

string

phoneCaptcha

手機驗證碼

body

false

string

phoneNumber

手機號 RSA 加密（與 X-Sign 不同秘鑰）

body

false

string

請求 header 示例

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

X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"areaCode": "86", "password": "rsa"，
"phoneCaptcha": "1234",
"phoneNumber": "188********"
}

回應狀態

狀態碼 說明 schema
0 成功

200 OK UserResponseEntity
300100 非法請求

300304 驗證次數過多，請稍後重試

300305 抱歉，驗證碼已過期，請重新獲取

300701 該手機號沒有註冊

300707 您當前已通過客戶經理完成預註冊，請通過短信驗證碼登
錄並啟動帳號。

300800 短信驗證碼不正確，請重新輸入

300801 密碼長度不能小於 8 位

300802 密碼長度不能大於 24 位

300803 密碼不能為純數位/字母/符號

300804 請設置正確密碼，8~24 位元數位/字母/符號組合

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

---

## 第 17 页

data

回應體

object

msg

回應內容

string

回應示例

{

"code": 0,
"data": {},
"msg": ""

}

1.7 解鎖交易

介面位址 /user-server/open-api/trade-login

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 需要 token

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

---

## 第 18 页

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password

新密碼 RSA 加密（與 X-Sign 不同秘鑰）

body

true

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

回應狀態

狀態碼 說明 schema
0 成功

200 OK UserResponseEntity
300100 非法請求

300304 驗證次數過多，請稍後重試

300305 抱歉，驗證碼已過期，請重新獲取

300701 該手機號沒有註冊

300707 您當前已通過客戶經理完成預註冊，請通過短信驗證碼登
錄並啟動帳號。

300800 短信驗證碼不正確，請重新輸入

300801 密碼長度不能小於 8 位

300802 密碼長度不能大於 24 位

300803 密碼不能為純數位/字母/符號

300804 請設置正確密碼，8~24 位元數位/字母/符號組合

---

## 第 19 页

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{

"code": 0,

"data": ,

"msg": ""

}

1.8 獲取交易解鎖狀態

介面位址 /user-server/open-api/get-trade-status

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 需要 token

請求參數

---

## 第 20 页

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password

新密碼 RSA 加密（與 X-Sign 不同秘鑰）

body

true

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

回應狀態

狀態碼 說明 schema

0

成功

200

OK

UserResponseEntity

300100

非法請求

300304

驗證次數過多，請稍後重試

300305

抱歉，驗證碼已過期，請重新獲取

300701

該手機號沒有註冊

300707 您當前已通過客戶經理完成預註冊，請通過短信驗證碼登錄並
啟動帳號。

---

## 第 21 页

300800

短信驗證碼不正確，請重新輸入

300801

密碼長度不能小於 8 位

300802

密碼長度不能大於 24 位

300803

密碼不能為純數位/字母/符號

300804

請設置正確密碼，8~24 位元數位/字母/符號組合

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

status

訂單狀態，0 未解密，1 已解鎖

int32

msg

回應內容

string

回應示例

{
"code": 0, "msg": "
成功", "data": {
"status": 0
}
}

1.9 修改交易密碼

介面位址 /user-server/open-api/update-trade-password

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

---

## 第 22 页

介面描述 需帶登錄態 token 使用者需要完成開戶，且未設置過交易密碼，否則算非法請求

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言 1 簡體 2 繁體

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password

交易密碼 必填， 交易密碼必須是 6 位元純數位

RSA 加密（與 X-Sign 不同秘鑰）

body

true

string

oldPassword 舊交易密碼 修改交易密碼必填，交易密碼必須是
6 位元純數位 RSA 加密（與 X-Sign 不同秘鑰）

body

false

string

phoneCaptcha

手機驗證碼，根據驗證碼重置交易密碼必填

body

false

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"oldPassword": "",
"password": "", "phoneCaptcha":
""
}

---

## 第 23 页

回應狀態

狀態碼 說明 schema
0 成功
200 OK UserResponseEntity
300100 非法請求
300101 非法 TOKEN
301001 交易密碼需為 6 位元純數字，請重新輸入
301003 交易密碼錯誤，請重新輸入，您還可以嘗試%s 次
301004 交易服務異常
301005 帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{
"code": 0,
"data": {},
"msg": ""
}

1.10 重置交易密碼

介面位址 /user-server/open-api/reset-trade-password

請求方式 POST

consumes ["application/json"]

---

## 第 24 页

produces ["application/json"]

介面描述 需帶登錄態 token 使用者需要完成開戶，且未設置過交易密碼，否則算非法請求

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言 1 簡體 2 繁體

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password

交易密碼 必填， 交易密碼必須是 6 位元純數位

RSA 加密（與 X-Sign 不同秘鑰）

body

true

string

oldPassword 舊交易密碼 非必填，交易密碼必須是 6 位元純
數位 RSA 加密（與 X-Sign 不同秘鑰）

body

false

string

phoneCaptcha

手機驗證碼，根據驗證碼重置交易密碼必填

body

false

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"oldPassword": "",

---

## 第 25 页

"password": "",
"phoneCaptcha": ""
}

回應狀態

狀態碼 說明 schema
0 成功
200 OK UserResponseEntity
300100 非法請求
300101 非法 TOKEN
301001 交易密碼需為 6 位元純數字，請重新輸入
301003 交易密碼錯誤，請重新輸入，您還可以嘗試%s 次
301004 交易服務異常
301005 帳戶被凍結，無法完成操作，如非本人操作，請聯繫客服

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{
"code": 0,
"data": {},
"msg": ""
}

1.11 修改登陸密碼

介面位址 /user-server/open-api/update-login-password

請求方式 POST

consumes ["application/json"]

---

## 第 26 页

produces ["application/json"]

介面描述 需帶登錄態 token 使用者需要已設置登陸密碼，否則算非法請求

請求參數

參數名稱 說明 請求類型 必填 類型

Authorization

見概述 Authorization 說明

header

true

string

X-Lang

語言 1 簡體 2 繁體

header

true

string

X-Request-Id  頭部資訊的 requestId 資訊,長度 30 位，確保唯
一，防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string
X-Sign

簽名

header

true

string

password 新登陸密碼 必填 RSA 加密（與 X-Sign 不同秘
鑰）

body

true

string

oldPassword 舊登陸密碼 必填 RSA 加密（與 X-Sign 不同秘
鑰）

body

true

string

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"oldPassword": "",
"password": "",
}

---

## 第 27 页

回應狀態

狀態碼 說明 schema
0 成功
200 OK UserResponseEntity
300100 非法請求
300101 非法 TOKEN
300704 原登陸密碼不正確
300804 請設置正確密碼，8~24 位元數位/字母/符號組合
300810 新密碼長度不能小於 8 位
300811 新密碼長度不能大於 24 位
300812 新密碼不能為純數位/字母/符號

回應參數

參數名稱

說明

類型

schema

code

回應碼

int32

data

回應體

object

msg

回應內容

string

回應示例

{
"code": 0,
"data": {},
"msg": ""
}

2 交易

2.1 下單

介面位址 /stock-order-server/open-api/entrust-order

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

---

## 第 28 页

介面描述 下單

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Dt 設備類型 (t1-android ， t2-ios， t3- 其他， t4-
Windows,t5-Mac)

header

true

string

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止
重複提交實現介面冪等

header

true

string

X-Sign

RSA 簽名

header

true

string
serialNo 流水號，最長 19 位，確保唯一推薦雪花演
算法生成

body

true

int64

entrustAmount

委託數量

body

true

number

entrustPrice

價格(競價單價格傳 0)

body

true

number

entrustProp 委託屬性 ('0'- 美股限價單 / 暗盤委託  limit
order,'d'-競價單 ,'e'-增強限價單 ,'g'-競價限價
單)

body

true

string

entrustType

委託類別(0-買，1-賣)

body

true

int32

exchangeType

交易類別(0-香港,5-美股,6-滬港通,7-深港通)

body

true

int32

stockCode

股票代碼

body

true

string

password

交易密碼（RDA 公開金鑰加密）

body

false

string

stockName

股票名稱

body

false

string

forceEntrustFlag 是否強制委託標 記，超過 9 倍 24 檔下單時
forceEntrustFlag=true 可強制下單，但有可能
是廢單

body

false

boolean

sessionType 交易階段標誌（0/不傳-正常訂單交易（預
設），1-盤前，2-盤後交易，3-暗盤交易）

body

false

int32

請求 header 示例
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
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
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

回應狀態
狀態碼 說明 schema
0 成功
200 OK ResponseVO«EntrustOrderResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found
406472 訂單中不能包含小於 1 手數量的碎股，請交易 1
手的整數倍，或通過"碎股單"交易碎股

410200 抱歉，訂單中不能包含小於 1 手數量的碎股，請
交易 1 手的整數倍，如需交易碎股請聯繫客服。

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

EntrustOrderResponse

EntrustOrderResponse

entrustId

訂單 id,可用於查詢訂單/修改訂單/取消訂

string

---

## 第 30 页

單

status

訂單狀態

int32

statusName

訂單狀態名稱

string

·msg

狀態資訊

string

回應示例
{
"code": 0,
"msg": "操作成功",
"data": {
"entrustId": "1181776863632019456",
"status": 1, "statusName": "等待
提交"
}
}

2.2 委託改單/撤單

介面位址 /stock-order-server/open-api/modify-order

請求方式 POST

consumes ["application/json"]

produces ["*/*"]
介面描述 委託改單/撤單

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止
重複提交實現介面冪等

header

true

string

X-Sign

RSA 簽名

header

true

string

actionType

操作類型(0-撤單，1-改單)

body

true

int32

entrustAmount

委託數量，撤單時傳 0

body

true

number

entrustId

委託 Id

body

true

int64

entrustPrice

委託價格，撤單時傳 0

body

true

number

---

## 第 31 页

password

交易密碼（RDA 公開金鑰加密）

body

false

string

forceEntrustFlag 是否強制委託標 記，超過 9 倍 24 檔下單時
forceEntrustFlag=true 可強制下單，但有可能是
廢單

body

false

boolean

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"actionType": 1,
"entrustAmount": 500,
"entrustId": 1181776863632019456,
"entrustPrice": 322.0,
"forceEntrustFlag": true
}

回應狀態
狀態碼 說明 schema
0 成功
200 OK Object
201 Created
401 Unauthorized
403 Forbidden
404 Not Found
406472 訂單中不能包含小於 1 手數量的碎股，請交易 1 手的整
數倍，或通過"碎股單"交易碎股

410200 抱歉，訂單中不能包含小於 1 手數量的碎股，請交易 1
手的整數倍，如需交易碎股請聯繫客服。

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

Object

---

## 第 32 页

entrustId

申請編號

string

status

狀態

int32

statusName

狀態名

string

msg

狀態資訊

string

回應示例
{
"code": 0,
"msg": "操作成功",
"data": {
"entrustId": "1181776863632019456",
"status": 5, "statusName": "等待
改單"
}
}

2.3 改單範圍

介面位址 /stock-order-server/open-api/modified-range

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 改單展
示範圍
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

entrustId

委託 Id

body

true

int64

newPrice

最新價-競價單也需要傳最新價

body

true

number

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8

---

## 第 33 页

X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求示例
{
"entrustId": 1181776863632019456,
"newPrice": 323
}

回應狀態
狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«QueryEntrustInfoResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體 QueryEntrustInfoRespons e QueryEntrustInf
oResponse

businessAmount

成交數量

number

entrustAmount

原訂單數量

number

modifiedUpperAmount

可修改範圍的修改上限

number

modifiedlowerAmount

可修改範圍的修改下限

number

msg

狀態資訊

string

回應示例
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

2.4 碎股下單

介面位址 /stock-order-server/open-api/odd-entrust

請求方式 POST

consumes ["application/json"]
produces ["*/*"] 介
面描述 碎股交易請
求示例
{
"entrustAmount": 1,
"entrustPrice": 82.1,
"entrustType": 1,
"exchangeType": 0,
"stockCode": "00002"
}

請求參數
參數名稱 說明 請求類型 必填 類型
Authorization 頭部資訊的 token 資訊 header true string
X-Lang 語言類別(1-簡體，2-繁體，3-English) header true string
X-Channel 管道 ID，由盈立分配 header true string
X-Time 時間標記 header true string
X-Dt 設備類型 (t1-android ， t2-ios ， t3- 其他， t4-
Windows,t5-Mac)
header true string
X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止重
複提交實現介面冪等
header true string
X-Sign RSA 簽名 header true string
entrustAmount 委託數量 body true number
entrustPrice 價格 body true number
entrustType 委託類別(1-賣) body true int32
exchangeType 交易類別(0-香港,5-美股) body true int32
stockCode 股票代碼 body true string

回應狀態

---

## 第 35 页

狀態碼 說明 schema
200 OK
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

code

狀態碼

int32

data

返回體

oddId

碎股請求記錄 id

string

status

訂單狀態

int32

statusName

訂單狀態名稱

string

msg

狀態資訊

string

回應示例

2.5 碎股撤單

介面位址 /stock-order-server/open-api/odd-modify

請求方式 POST

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

介面描述 碎股交易

請求示例

{

"actionType": 0,

"oddId": 1207553433704988672

}

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止重複提
交實現介面冪等

header

true

string

X-Sign

RSA 簽名

header

true

string

actionType

操作類型(0-撤單)

body

true

int32

oddId

碎股委託 Id

body

true

int64

回應狀態
狀態碼 說明
200 OK
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

---

## 第 37 页

參數名稱

說明

類型

code

狀態碼

int32

oddId

碎股請求記錄 id

string

status

訂單狀態

int32

statusName

訂單狀態名稱

string

msg

狀態資訊

string

回應示例

2.6 最大可買、可賣數量

介面位址 /stock-order-server/open-api/trade-quantity

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 獲取最
大可用數量
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

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

RSA 簽名

header

true

string

entrustPrice

委託價格(不能為 0,競價單可不填)

body

false

number

entrustProp 委託屬性('0'- 美股限價單,'d'- 競價單,'e' - 增強限價
單,'g'-競價限價單，'u'-碎股單)

body

true

string

exchangeType

交易類別(0-香港,5-美股,6-滬港通,7-深港通)

body

true

int32

stockCode

證券代碼

body

true

string

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"entrustPrice": 234, "entrustProp":
"e", "exchangeType": 0,
"stockCode": "700"
}

回應狀態
狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«SaleAndBuyQuantityResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體 SaleAndBuyQuantityRespo
nse
SaleAndBuyQuantityRespo
nse

buyEnableAmount

最大可買數量

number

---

## 第 39 页

oddEnableAmount

最大可賣碎股數量

number

saleEnableAmount

最大可賣數量

number

saleEnableIntAmount

最大可賣整股數量

number

handAmount

每手股數

number

msg

狀態資訊

string

回應示例
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

2.7 今日訂單-分頁查詢

介面位址 /stock-order-server/open-api/today-entrust

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 需要資
金帳號
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

exchangeType 交易類別(0-香港,5-美股, 67-A 股，100-查詢所有交
易類別)

body

true

int32

---

## 第 40 页

pageNum

當前頁 1 開始，預設值 1

body

false

int32

pageSize

每頁結果數，預設值 10

body

false

int32

stockCode

證券代碼

body

false

string

stockName

證券名稱

body

false

string

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"exchangeType": 0,
"pageNum": 1,
"pageSize": 10, "stockCode": "",
"stockName": ""
}

回應狀態
狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«PageInfoVO«TodayEntrustByAppResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

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

結果集合

array TodayEntrustByAp
pResponse

businessAmount

成交數量

number

businessAveragePrice

成交均價

number

serialNo

流水號

int64

createTime

委託時間

string

entrustAmount

委託數量

number

entrustId

委託 id

string

entrustNo

委託編號

string

entrustPrice

委託價格

number

entrustProp

委託屬性('0'-美股限價單,'d'-競價單,'e' -增
強限價單,'g'-競價限價單,'h'-港股限價單,'j'-
特殊限價單)

string

entrustType

買賣方向,委託類型(0-買，1-賣)

int32

exchangeType

交易類別，0 港股，5 美股

int32

flag 訂單類型-普通單 0-條件單 1-碎股單 2-月供
股單

string

moneyType

幣種類別

int32

sessionType 交易階段標誌 （0/不傳-正常訂單交易（ 預
設 ） ， 1- 盤前， 2- 盤後交易，  3- 暗盤交
易）

int32

status

委託狀態

int32

statusName

委託狀態名

string

stockCode

股票代碼

string

stockName

股票簡體名稱

string

pageNum

當前頁

int32

pageSize

每頁條數

int32

total

總數

int64

msg

狀態資訊

string

回應示例
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
單", "exchangeType": 0,
"entrustType": 0, "entrustProp": "e",
"entrustAmount": 700,
"businessAmount": 0,
"entrustPrice": 210,
"businessAveragePrice": 0,
"stockCode": "00700",
"stockName": "騰訊控股",
"moneyType": 2,
"createTime": "11:42:15",
"flag": "0",
"serialNo": 1233123554314,
"sessionType": 0
}]
}
}

2.8 全部訂單-分頁查詢

介面位址 /stock-order-server/open-api/his-entrust

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 需要資
金帳號
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

---

## 第 43 页

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

dateFlag

1:一周訂單，2：一個月訂單，3: 三個月訂單，
4：近一年訂單，5：今年訂單，6：自選時間,7.查
詢全部

body

true

string

exchangeType 交易類別(0-香港,5-美股, 67-A 股，100-查詢所有交
易類別)

body

true

int32

entrustBeginDate 開始時間，如果不傳時間默認從最新前一天倒序,
規則 yyyy-MM-dd

body

false

string

entrustEndDate 結束時間，如果不傳時間默認從最新前一天倒序,
規則 yyyy-MM-dd

body

false

string

pageNum

當前頁 1 開始，預設值 1

body

false

int32

pageSize

每頁結果數，預設值 10

body

false

int32

stockCode

證券代碼

body

false

string

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"dateFlag": "1",
"entrustBeginDate": "",
"entrustEndDate": "",
"exchangeType": 0,
"pageNum": 1,
"pageSize": 10,
"stockCode": ""
}

回應狀態
狀態碼 說明 schema
0 成功 ResponseVO

---

## 第 44 页

200 OK ResponseVO«PageInfoVO«HisEntrustByAppResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

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

結果集合

array HisEntrustByAp
pResponse
businessAmoun
t

成交數量

number

businessAverag
ePrice

成交均價

number

serialNo

流水號

int64

createDate

委託日期

string

createTime

委託時間

string

dayEnd

是否隔天,0 未隔天，1 已經隔天

int32

entrustAmount

委託數量

number

entrustId

委託 ID

string

entrustNo

委託編號

string

entrustPrice

委託價格

number

entrustProp

委託屬性('0'-美股限價單,'d'-競價單,'e' -增強限價單,'g'-

競價限價單,'h'-港股限價單,'j'-特殊限價單)

string

entrustType

買賣方向,委託類型(0-買，1-賣)

int32

exchangeType

交易類別，0 港股，5 美股

int32

flag

訂單類型-普通單 1-條件單 2-碎股單 3-月供股單 4

string

moneyType

幣種類別

int32

sessionType

交易階段標誌（0/不傳-正常訂單交易（預設），1-盤

int32

---

## 第 45 页

前，2-盤後交易，3-暗盤交易）

status

委託狀態

int32

statusName

委託狀態名

string

stockCode

股票代碼

string

stockName

股票簡體名稱

string

pageNum

當前頁

int32

pageSize

每頁條數

int32

total

總數

int64

msg

狀態資訊

string

回應示例

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
單", "exchangeType": 0,
"entrustType": 0, "entrustProp": "e",
"entrustAmount": 700,
"businessAmount": 0,
"entrustPrice": 210,
"businessAveragePrice": 0,
"stockCode": "00700",
"stockName": "騰訊控股",
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

2.9 查詢訂單明細

介面位址 /stock-order-server/open-api/order-detail

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 查詢訂
單明細
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string
appEntrustRecordDetail
Request

appEntrustRecordDetailRequest

body

true AppEntrustReco
rdDetailRequest
serialNo 流水號（委託 ID、流水號一個至少傳
一個）

body

true

int64

entrustId 委託 id（委託 ID、流水號一個至少傳
一個）

body

true

int64

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求示例

---

## 第 47 页

{
"serialNo": 0,
"entrustId": 0
}

回應狀態

狀態碼

說明

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

回應參數

參數名稱

說明

類型

schema

code

狀態碼

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

成交數量

number

businessAveragePrice

成交均價

number

businessBalance

成交金額

number

commissionFee

港美,佣金

string

createTime

時間

string

depositStockDay

股份到賬時間

string

---

## 第 48 页

entrustId

委託記錄號

int64

entrustAmount

委託數量

number

entrustBalance

委託金額

number

entrustFee

總費用

string

entrustPrice

委託價格

number

entrustProp

委託屬性('0'-美股限價單,'d'-競價單,'e' -增強限價

單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)

string

entrustPropName

委託屬性('0'-美股限價單,'d'-競價單,'e' -增強限價

單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)

string

moneyType

幣種類別

int32

orderStatus

狀態

int32

orderStatusName

狀態名

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

港，交易系統使用費

string

transactionFee

港：交易費，美：證監會費

string

transactionLevyFee

港，交易徵費，美：交易活動費

string

document

文案信息

string

entrustType

買入賣出

int32

exchangeType

市場類型

int32

sessionType 交 易 階 段 標 誌（ 0/ 不傳 - 正 常 訂 單 交 易（ 預
設），1-盤 前 ，2-盤 後 交 易 ，3-暗 盤 交 易 ）

int32

status

委託狀態

int32

statusName

委託狀態名

string

stockCode

股票代碼

string

stockName

股票名稱

string

msg

狀態資訊

string

回應示例
{
"code": 0,
"msg": "操作成功",
"data": {

---

## 第 49 页

"statusName": "全部成交",
"status": 0,
"stockCode": "00700",
"stockName": "騰訊控股",
"document": "由於和交易所清算交收，部分資料可能在交易完成的第 2 天（工作日）展示",
"appEntrustRecordDetailInfoList": [{ "entrustProp": "e",
"entrustPropName": "增強限價單",
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
"orderStatusName": "委託下單"
},
{
"entrustProp": "e", "entrustPropName": "增
強限價單", "entrustAmount": 700,
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
"orderStatusName": "改單（最新訂單）"
},
{
"entrustProp": "e", "entrustPropName": "增
強限價單", "entrustAmount": 700,
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
"orderStatusName": "全部成交（訂單結束）"
}
],
"entrustType": 0,
"exchangeType": 0,
"finalStateFlag": "1",
"sessionType": 0,
"entrustId": 1181776863632019500
}
}

2.10 查詢成交流水-分頁查詢

介面位址 /stock-order-server/open-api/stock-record

請求方式 POST

---

## 第 51 页

consumes ["application/json"] produces
["application/json"] 介面描述 需要資
金帳號
請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

exchangeType 交易類別(0-香港,5-美股, 67-A 股，100-查詢所有交
易類別)

body

true

int32

stockCode

股票代碼

body

false

string

entrustId

委託 ID

body

false

int64
beginTime

成交開始時間，規則 yyyy-MM-dd

body

false

string
endTime

成交結束時間，規則 yyyy-MM-dd

body

false

string

pageNum

當前頁 1 開始，預設值 1

body

false

int32

pageSize

每頁結果數，預設值 10

body

false

int32

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求示例
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

回應狀態
狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«PageInfoVO«StockRecordResponse»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

PageInfoVO«StockRe
cordResponse»

PageInfoVO«Stoc
kRecordResponse
»

list

結果集合

array StockRecordResp
onse

businessAmount

成交數量

number

businessBalance

成交金額

number

businessPrice

成交價格

number

businessStatus

成交狀態（1 成交成功，2 成交取消）

int32

businessTime

成交時間

date-time

createTime

記錄創建時間

date-time

entrustId

委託記錄號

int64

entrustType

委託類型(''0''- 買， 1- 賣， ''2''- 查詢，
''3'- 撤單， ''4'- 補單， ''5''- 改單， 6 轉
入，7 轉出,8 成交取消類型)

int32

exchangeType

交易類別 ('0'-香港，'1'-上海 A，'2'-上

海 B，'3'-深圳 A，'4'-深證 B，'5'-美

股，'6'-滬股通，'7'-深港通)

int32

id

int64

moneyType

幣種類型(0-人民幣，1-美元，2-港幣)

int32

recordId

成交流水編號

int64

---

## 第 53 页

remark

備註

string

stockCode

股票代碼

string

stockName

股票名稱

string

updateTime

記錄最後更新時間

date-time

userId

用戶 id

int64

pageNum

當前頁

int32

pageSize

每頁條數

int32

total

總數

int64

msg

狀態資訊

string

回應示例

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
"stockName": "騰訊控股",
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

2.11 查詢持倉

介面位址 /stock-order-server/open-api/stock-holding

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 需要資金帳號

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

exchangeType

交易類別(0-香港,5-美股, 67-A 股，100-

查詢所有交易類別)

body

true

int32

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

查詢請求 body 示例

{
"exchangeType": 0
}

---

## 第 55 页

回應狀態

狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«List«StockHolding»»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

array

StockHolding

costPriceAccurate

成本價--精確

string

currentAmount

持倉數量

string

enableAmount

可賣數量

string

frozenAmount

凍結數量

string

exchangeType

交易類型

int32

oddAmount

碎股數量

string

stockCode

股票代碼

string

stockName

股票名稱

string

lastPrice

最新價

string

msg

狀態資訊

string

回應示例

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

2.12 查詢資產

介面位址 /stock-order-server/open-api/stock-asset

請求方式 POST

consumes ["application/json"]

produces ["application/json"]

介面描述 需要資金帳號

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang 語言類別 (1- 簡體， 2- 繁體， 3-
English)

header

true

string

X-Channel

管道

header

true

string

X-Time

時間戳記

header

true

string

X-Sign

RSA 簽名

header

true

string

exchangeType

交易類別(0-香港,5-美股,67-A 股)

body

true

int32

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

---

## 第 57 页

請求 body 示例

{
"exchangeType": 0
}

回應狀態

狀態碼 說明 schema
0 成功 ResponseVO
200 OK ResponseVO«StockAssetDTO»
201 Created
401 Unauthorized +
403 Forbidden
404 Not Found

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

StockAssetDTO

StockAssetDTO

asset

總資產

string

enableBalance

可用金額

string

frozenBalance

凍結金額

string

onWayBalance

在途資金

string

stockHoldingList

持倉列表

array

StockHolding

costPriceAccurate

成本價--精確

string

currentAmount

持倉數量

string

exchangeType

交易類型

int32

oddAmount

碎股數量

string

stockCode

股票代碼

string

stockName

股票名稱

string

withdrawBalance

可取金額

string

msg

狀態資訊

string

---

## 第 58 页

回應示例

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

2.13 客戶股票資產查詢批量

介面位址 /stock-order-server/open-api/stock-asset-list

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介面描述 需要資
金帳號
請求示例

---

## 第 59 页

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"exchangeType": 100
}

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Lang

語言類別(1- 簡體， 2- 繁體， 3-
English)

header

true

string

X-Sign

RSA 簽名

header

true

string

X-Type

APP 類別(1-大陸版，2-港版)

header

true

string

stockAssetForAppReq

stockAssetForAppReq

body

true

StockAssetForAppReq

exchangeType

交易類別，0 港股，5 美股

body

true

int32

---

## 第 60 页

回應狀態

狀態碼

說明

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

回應參數

參數名稱

說明

類型

code

狀態碼

int32

data

返回體

array

asset

總資產

string

enableBalance

可用金額

string

frozenBalance

凍結金額

string

marketValue

股票市值

string

onWayBalance

在途資金

string

---

## 第 61 页

stockHoldingList

持倉列表

array

costPrice

成本價

string

costPriceAccurate

成本價--精確

string

currentAmount

持倉數量

string

dailyBalance

當日盈虧金額

string

dailyBalancePercent

當日盈虧占比

string

enableAmount

可賣數量

number

exchangeType

交易類型

int32

frozenAmount

凍結數量

number

hisMarketValue

市值

string

holdingBalance

持倉盈虧金額

string

holdingBalancePercent

持倉盈虧占比

string

lastPrice

最新價

string

marketValue

市值

string

oddAmount

碎股數量

string

---

## 第 62 页

quoteType

行情許可權 0: 延時行情 1:bmp 行情

2:level1 行情 3:level2 行情

string

stockCode

股票代碼

string

stockName

股票名稱

string

stockOnWayBalanceDTOList

在途資金列表

array

applyType

業務類型 IpoApplyTypeEnum

int32

applyTypeName

業務類型 IpoApplyTypeEnum

string

exchangeType

市場

int32

moneyType

幣種

int32

onWayBalance

在途現金

number

stockCode

股票代碼

string

stockName

股票名稱

string

totalDailyBalance

今日盈虧金額

string

totalDailyBalancePercent

今日盈虧占比

string

totalHoldingBalance

持倉盈虧金額

string

---

## 第 63 页

totalHoldingBalancePercent

持倉盈虧占比

string

withdrawBalance

可取金額

string

msg

狀態資訊

string

回應示例

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

2.14 查詢聚合資產資訊

介面位址 /aggregation-server/open-api/user-asset-aggregation/v1

請求方式 POST

consumes ["application/json"] produces
["application/json"] 介 面 描 述 需要
token

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

---

## 第 68 页

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止
重複提交實現介面冪等

header

true

string

X-Sign

RSA 簽名

header

true

string
exchangeType

交易類別，0-港股，5-美股，67-A 股

body

true

int32

請求 header 示例

Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiOTMyYmFjY2U3MGU3
NDgwM2JmNjYxODk0OTM3ZDlkN2QiLCJzb3VyY2UiOiJ3ZWIiLCJ1dWlkIjozNDMwMjExNDU2ODI4NjIwODB
9.XiF0eWAmeL-pthTg--5SLObnscJcDYHaJTJZTHAucwQ
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Channel：100082
X-Request-Id: 928239187123721231232

X-Sign：body 使用 RSA 私密金鑰加密

回應狀態

狀態碼

說明

schema

0

成功

ResponseVO

200

OK

ResponseVO«OpenHoldAsset»

108008

user 服務不可用

108011

使用者資訊查詢介面異常

108027

stock-order 服務不可用

108028

調用客戶股票資產查詢介面異常

---

## 第 69 页

108029

finance-server 服務不可用

108030

獲取當前客戶基金持倉清單介面異常

108031

獲取當前客戶債券持倉清單介面異常

回應參數

參數名稱

說明

類型

schema

Code

回應碼 0-請求成功

int32

Data

回應體

object

OpenHoldAsset

asset

總資產

string

bondMarketValue

債券市值

string

enableBalance

可用金額

string

frozenBalance

凍結金額

string

fundMarketValue

基金市值

string

onWayBalance

在途資金

string

stockMarketValue

股票市值

string

withdrawBalance

可取金額

string

totalHoldingBalance

持倉盈虧金額

string

msg

回應內容

string

{

"code": 0,

"msg": "請求成功",
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

3.1 獲取 IPO 列表-分頁查詢

介面位址 /stock-order-server/open-api/ipo-list

請求方式 POST

consumes ["application/json"]

produces ["*/*"]
介面描述 獲取 IPO 清單（不需要登陸）

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道

header

true

string

---

## 第 71 页

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

status

Tab 頁類別(0-認購中，1-待上市)

body

true

int32

pageNum

當前頁 1 開始, 預設值 1

body

false

int32

pageSize

每頁結果數, 預設值 10

body

false

int32

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"pageNum": 1,
"pageSize": 10,
"status": 1
}

回應狀態

狀態碼

說明

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

回應參數

參數名稱

說明

類型

schema

code

狀態碼

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

結果集合

array OpenApiGetIpoList
Response

bookingRatio

認購倍數

number

endTime

現金認購結束時間

yyyy-MM-dd HH:mm:ss

string

englishName

新股英文名

string

exchangeType

市場類型(0-港股)

int32

financingEndTime

融資認購結束時間

string

financingMultiple

融資倍數

int32

ipoId

IPO id

string

labelStatus

標籤狀態(0-已認購,1-已中簽,2-未中簽)

int32

latestEndtime 最晚認購截止時間(國際認購、融資認購
和現金認購截止時間最晚的時間)

string

leastAmount

起購金額

number

listingPrice

最終上市價格

number

listingTime

上市交易時間

string

moneyType

幣種類型(0-人民幣，1-美元，2-港幣)

int32

priceMax

最高招股價

number

priceMin

最低招股價

number

publishTime

公佈中簽日期

string

remainingTime

認購剩餘時間（秒）

int64

serverTime

伺服器時間

string

status 新股狀態 (0-待認購， 1-認購中， 2-待扣
款，3-已扣款待確認，4-已確認待公佈，
5-已公佈待上市， 6-已上市， 7-取消上
市，8-暫緩上市，9-延遲上市)

int32

statusName

狀態中文名

string

stockCode

新股代碼

string

stockName

新股名稱

string

subscribeWay

認購方式，多種認購用 ,隔開，比如 0,1

支持現金和融資 (1-公開現金認購， 2-公

string

---

## 第 73 页

開融資認購，3-國際配售)-這個欄位可以
判斷是否支援融資認購

successRate

中簽率

number

pageNum

當前頁

int32

pageSize

每頁條數

int32

total

總數

int64

msg

狀態資訊

回應示例

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
"status": 1, "statusName": "認購
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
"status": 1, "statusName": "認購
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

3.2 獲取新股詳細資訊

介面位址 /stock-order-server/open-api/ipo-info

請求方式 POST

consumes ["application/json"]

produces ["*/*"]
介面描述 獲取新股詳細資訊

---

## 第 75 页

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道 ID，由盈立分配

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

exchangeType

市場類型(0-HK,5-US),如果 ipoId 不傳，該欄位必傳

body

false

int32

ipoId 新股 id [ 與(stockCode&exchangeType 不能同時為空 )],
當  ipoId 有  值  ，  優  先  取  ipoId 查  詢  ，
stockCode&exchangeType 條件不生效

body

false

int64

stockCode

股票代碼,如果 ipoId 不傳，該欄位必傳

body

false

string

回應狀態
狀態碼 說明 schema
200 OK ResponseVO«appIpoInfoResponse»
201 Created
401 Unauthorized
403 Forbidden
404 Not Found

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例
{
"ipoId": 1133576191528632320
}

回應參數

---

## 第 76 页

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體 appIpoInfoResp
onse
appIpoInfoRes
ponse

applied

用戶是否已認購

boolean

beginTime

現金認購開始時間

string

bookingFee

現金認購手續費

number

bookingRatio

認購倍數

number

compFinancingSurplus

公司融資額度淨餘

number

depositRate

融資比例

number

ecmEndTime

國際認購截止時間

date-time

ecmStatus ecm 新股狀態(0- 待認購,1- 認購中， 2- 待扣
款，3-待扣款[未全部扣款成功 ]，4-待提交，
5-待分配，6-待返款，7-待返款[未全部返款成
功]，8-待返券，9-待返券[未全部返券成功]，
10-待 CCASS 確認，11-待上市，12-已上市，
13-暫停認購)

int32

endTime

現金認購結束時間

string

englishName

新股英文名

string

exchangeType

交易類別(0-HK,5-US)

int32

exchangeTypeName

交易類別名稱

string

financingEndTime

融資認購截止時間

date-time

financingFee

融資手續費

number

financingMultiple

融資倍數

int32

financingTips

融資認購溫馨提示

string

greyFlag

是否支持暗盤（0-不支持，1-支持）

int32

greyTimeBegin

暗盤交易時間段開始，格式 HH:mm:ss

string

greyTimeEnd

暗盤交易時間段結束，格式 HH:mm:ss

string

greyTradeDate

暗盤交易日，格式 yyyy-MM-dd

string

handAmount

每手股數

number

interestBeginDate

融資認購/計息開始時間

date-time

interestDay

計息天數

int32

---

## 第 77 页

interestEndDate

融資計息結束時間

date-time

interestRate

默認融資利率

number

ipoFinancingRatios 融   資   階   梯   利   率   (json   陣
列 :[{"financing_amount_begin": 初 始 認 購 金
額  ,"financing_amount_end": 結  束  認  購  金
額 ,"interest_rate": 利率 ,"exchange_type":市場類
型,"stock_code":"新股代碼"}])

array

IpoFinancingR
atio

exchange_type

市場類型

int32

financing_amount_begin

初始認購金額

number

financing_amount_end

結束認購金額

number

interest_rate

利率

number

stock_code

新股代碼

string

ipoId

IPO id

string

latestEndtime 最晚認購截止時間(國際認購、融資認購和現
金認購截止時間最晚的時間)

string

leastAmount

起購金額(一手認購金額)

number

listingPrice

最終上市價格

number

listingTime

上市交易時間

string

marketValueMax

市值最大值

number

marketValueMin

市值最小值

number

moneyType

幣種類型(0-人民幣，1-美元，2-港幣)

int32

officialBegin

官方招股開始時間

string

officialEnd

官方招股結束時間

string

priceMax

最高招股價

number

priceMin

最低招股價

number

prospectusLink

招股書連結

string

publishQuantity

發行股本

number

publishTime

公佈中簽日期

string

qtyAndCharges 檔位元資訊(json 陣列:[{"allotted_amount": 中簽
金    額    ,"applied_amount":   申    購  金
額    ,"exchange_type":      市    場    類
型,"shared_applied":申購數量,"stock_code":"新

array

IpoQtyAndCha
rges

---

## 第 78 页

股代碼"," leastCash ":檔位對應的最少使用現
金}])

allotted_amount

中簽金額

number

applied_amount

申購金額

number

exchange_type

市場類型

int32

leastCash

檔位對應的最少使用現金

int32

shared_applied

申購數量

number

stock_code

新股代碼

string

remainingTime

認購剩餘時間（秒）

int64

serverTime

伺服器時間

string

sponsor

保薦人

string

status 新股狀態(0-待認購，1-認購中，2-待扣款，3-
已扣款待確認，4-已確認待公佈，5-已公佈待
上市，6-已上市，7-取消上市，8-暫緩上市，
9-延遲上市)

int32

statusName

狀態中文名

string

stockCode

新股代碼

string

stockIntroduction

股票介紹

string

stockName

新股名稱

string

subscribeWay 認購方式，多種認購用 ,隔開，比如  1,2 支持
現金和融資 (1-公開現金認購， 2-公開融資認
購，3-國際配售)-這個欄位可以判斷是否支援
融資認購

string

successRate

中簽率

number

tips

現金認購溫馨提示

string

totalQuantity

總股本

number

updateTime

更新時間

string

msg

狀態資訊

string

回應示例
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

3.3ipo 新股認購

介面位址 /stock-order-server/open-api/apply-ipo

請求方式 POST

consumes ["application/json"]

produces ["*/*"]

介面描述 ipo 新股認購

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Dt 設備類型(t1-android，t2-ios，t3-其他，t4-
Windows,t5-Mac)

header

true

string

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，
防止重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

---

## 第 81 页

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

applyQuantity

認購數量

body

true

number

applyType

認購類型(1-現金，2-融資)

body

true

int32

ipoId

ipo 交易系統唯一編號

body

true

int64
serialNo 流水號，最長 19 位，確保唯一推薦雪花
演算法生成

body

true

int64

cash

認購現金(融資認購時必填)

body

false

number

請求 header 示例

Authorization:eyJ0eXAiOiJKV1Qi LCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZ
iNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密’;

請求 body 示例

{
"applyQuantity": 100,
"applyType": 1,
"cash": 0,
"ipoId": 1133576191818039296,
"serialNo": 1182189250463484234
}

回應狀態

狀態碼 說明 schema
200 OK ResponseVO«IpoApplyResponse»
201 Created

---

## 第 82 页

401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱 說明 類型 schema
code 狀態碼 int32
data 返回體 IpoApplyResponse IpoApplyResponse
applyId 申購 id string
status 申購狀態(0-已提交,1-已認購,2-等待改單, 3-等待撤
銷,4-已撤銷,5-已扣款,6-待公佈中簽 ,7-全部中簽 ,8-
部分中簽,9-未中簽,10-認購失敗)
int32
msg 狀態資訊 string

回應示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1182192040986583040",
"status": 1
}
}

3.4ipo 改單/撤單

介面位址 /stock-order-server/open-api/modify-ipo

請求方式 POST

consumes ["application/json"]

produces ["*/*"]

介面描述 ipo 改單/撤單

---

## 第 83 页

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Request-Id 頭部資訊的 requestId 資訊，確保唯一，防止
重複提交實現介面冪等

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

actionType

操作類型 0-改單,1-撤單

body

true

int32

applyId

認購記錄 Id

body

true

int64

applyQuantity

認購數量

body

true

number

cash

認購現金(改融資認購單，必填)

body

false

number

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

{
"actionType": 1,
"applyId": 1182192040986583040,
"applyQuantity": 0,
"cash": 0
}

回應狀態

狀態碼 說明 schema
200 OK ResponseVO«IpoApplyResponse»

---

## 第 84 页

201 Created
401 Unauthorized
403 Forbidden
404 Not Found

回應參數

參數名稱 說明 類型 schema
code 狀態碼 int32

data 返回體 IpoApplyResponse IpoApplyResponse
applyId 申購 id string

status 申購狀態(0-已提交,1-已認購,2-等待改單,
3-等待撤銷 ,4-已撤銷 ,5-已扣款 ,6-待公佈
中簽 ,7- 全部中簽 ,8- 部分中簽 ,9- 未中
簽,10-認購失敗)
int32

msg 狀態資訊 string

回應示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1182192040986583040",
"status": 4
}
}

3.5 獲取客戶 ipo 申購清單-分頁查詢

介面位址 /stock-order-server/open-api/ipo-record-list

請求方式 POST

consumes ["application/json"]

produces ["*/*"]

介面描述 獲取客戶 ipo 申購清單

---

## 第 85 页

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Channel

管道

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

applyTimeMin 認 購 開 始 時 間 ， 格 式 :yyyy-MM-dd
HH:mm:ss

body

false

string

applyTimeMax 認 購 結 束 時 間 ， 格 式 :yyyy-MM-dd
HH:mm:ss

body

false

string

pageNum

當前頁 1 開始，預設值 1

body

false

int32

pageSize

每頁結果數，預設值 10

body

false

int32

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求示例

{
"pageNum": 1,
"pageSize": 10,
"applyTimeMin":"2019-10-12 00:00:00",
"applyTimeMax":"2020-01-30 00:00:00"
}

回應狀態

狀態碼

說明

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

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

PageInfoVO«IpoRe
cordListResponse»

PageInfoVO«IpoR
ecordListResponse
»

list

結果集合

array IpoRecordListRes
ponse

allottedQuantity

中簽股數

number

applyAmount

認購總金額(包含手續費，不包含利息)

number

applyId

申請編號

string

applyQuantity

認購股數

number

applyType

認購類型(1-現金，2-融資)

int32

applyTypeName

認購類型(1-現金認購，2-融資認購)

string

priceMax

最高招股價

number

priceMin

最低招股價

number

listingPrice

最終上市價格

number

cash

認購現金

number

exchangeType

市場類型(0-HK,5-US)

int32

financingAmount

融資利息

number

financingBalance

融資金額

number

interestRate

融資利率

number

labelCode 狀態標籤碼 (0-待系統確認 ,1-已認購 ,4-已撤
銷,6-待公佈中簽 ,7-已中簽 ,9-未中簽 ,10-認購
失敗)

int32

moneyType

幣種類型(0-人民幣，1-美元，2-港幣)

int32

publishTime

公佈中簽日期

string

---

## 第 87 页

listingTime

上市交易時間(YYYY-MM-DD)

serverTime

伺服器時間

string

status 認購狀態 (0-已提交 ,1-已認購 ,2-等待改單 , 3 -
等待撤銷,4-已撤銷,5-已扣款,6-待公佈中簽 ,7-
全部中簽,8-部分中簽,9-未中簽,10-認購失敗)

int32

statusName

認購狀態名稱

string

stockCode

股票代碼

string

stockName

股票名稱

string

pageNum

當前頁

int32

pageSize

每頁條數

int32

total

總數

int64

msg

狀態資訊

string

回應示例

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
融資認購", "stockName": "香港中華
煤氣", "stockCode": "00003",
"exchangeType": 0,
"status": 10, "statusName": "認購
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
融資認購", "stockName": "香港中華
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

3.6 獲取客戶 ipo 申購明細

介面位址 /stock-order-server/open-api/ipo-record

請求方式 POST

consumes ["application/json"]

---

## 第 89 页

produces ["*/*"]

介面描述 獲取客戶 ipo 申購明細

請求參數

參數名稱

說明

請求類型

必填

類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

X-Channel

管道

header

true

string

applyId

申購編號(傳其中一個即可)

body

false

int64

serialNo

流水號(傳其中一個即可)

body

false

int64

請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求示例

{
"applyId": 1147036407112679424,
"serialNo": 1233123554314
}

回應狀態

狀態碼

說明

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

回應參數

參數名稱

說明

類型

schema

code

狀態碼

int32

data

返回體

IpoRecordR
esponse

IpoRecordRes
ponse

allottedQuantity

中簽股數

number

applyAmount

認購總金額(包含手續費，不包含利息)

number

applyId

申請編號

string

applyQuantity

認購股數

number

applyType

認購類型(1-現金，2-融資)

int32

applyTypeName

認購類型(1-現金認購，2-融資認購)

string

cash

認購現金

number

channel

管道類型(1-APP 提交，2-中台提交，99-其它)

int32

createTime

認購提交時間

string

deductStatus

扣款狀態(0-已凍結，1-已扣款，2-已解凍)

int32

deductStatusName

扣款狀態名

string

endTime

當前認購方式截止時間

string

exchangeType

市場類型(0-HK,5-US)

int32

failReason

認購失敗原因

string

financingAmount

融資利息

number

financingBalance

融資金額

number

handlingFee

手續費

number

interestDay

計息天數

int32

interestRate

融資利率

number

ipoId

ipo 編號

string

ipoStatus

新股狀態(0-待認購，1-認購中，2-待扣款，3-已扣
款待確認，4-已確認待公佈，5-已公佈待上市，6-

int32

---

## 第 91 页

已上市，7-取消上市，8-暫緩上市，9-延遲上市)

labelCode

狀態標籤碼(0-待系統確認,1-已認購,4-已撤銷,6-待公
佈中簽,7-已中簽,9-未中簽,10-認購失敗)

int32

moneyType

幣種類型(0-人民幣，1-美元，2-港幣)

int32

publishTime

公佈中簽日期 yyyy-MM-dd HH:mm:ss

string

refundAmount

退款金額

number

refundFlag

退款狀態(0-無退款，1-待退款，2-已退款)

int32

serverTime

伺服器時間

string

status

認購狀態(0-已提交,1-已認購,2-等待改單, 3 -等待撤
銷,4-已撤銷 ,5-已扣款 ,6-待公佈中簽 ,7-全部中簽 ,8-
部分中簽,9-未中簽,10-認購失敗)

int32

statusName

認購狀態名稱

string

stockCode

股票代碼

string

stockName

股票名稱

string

listingTime

上市時間 yyyy-MM-dd

msg

狀態資訊

string

回應示例

{
"code": 0,
"msg": "操作成功",
"data": {
"applyId": "1178190341147189248",
"applyType": 1, "applyTypeName": "現
金認購", "stockName": "新城市建設發
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
"已解凍", "refundFlag": 0,
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

4 資金

4.1 查詢匯率

介面位址 /stock-capital-server/open-api/currency-exchange-info

請求方式 POST

consumes ["application/json"]

produces ["*/*"]
介面描述

請求 header 示例
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Type: 1
X-Channel：100082
X-Sign：body 使用 RSA 私密金鑰加密

請求 body 示例

---

## 第 93 页

請求參數
參數名稱 說明 請求類型 必填 類型

Authorization

頭部資訊的 token 資訊

header

true

string

X-Lang

語言類別(1-簡體，2-繁體，3-English)

header

true

string

X-Time

時間標記

header

true

string

X-Sign

RSA 簽名

header

true

string

X-Channel

管道

header

true

string

回應狀態
狀態碼 說明 schema
200 OK CapitalResponseVO«FetchExchangeRateResp»
201 Created

401 Unauthorized

403 Forbidden

404 Not Found

回應參數

參數名稱

說明

類型

code

狀態碼

int32

data

返回體

array

baseMoneyType

基準幣種，0:人民幣 1：美元 2：港幣

int32

sourceCurrency

源幣種，0:人民幣 1：美元 2：港幣

int32

targetCurrency

目標幣，0:人民幣 1：美元 2：港幣

int32

yxBuyRate

盈立買入匯率

number

yxSellRate

盈立賣出匯率

number

bocSellRate

中銀賣出匯率

number

bocBuyRate

中銀買入匯率

number

msg

狀態資訊

string

回應示例

{
"code": 0,
"msg": "操作成功",

---

## 第 94 页

5 資料字典

5.1 訂單狀態（Status）

編碼 名稱

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

等待撤單

5

等待改單

6

已撤單

7

部成撤單

8

廢單

5.2 市場類型（ExchangeType）

編碼 名稱

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

A 股（用於查詢）

100

所有市場（用於查詢）

---

## 第 96 页

5.3IPO 狀態（Status）

編碼

名稱

0

待認購

1

認購中

2

待扣款

3

已扣款待確認

4

已確認待公佈

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
5.4 幣種（moneyType）

編碼

名稱

0

人民幣

1

美元

2

港幣
5.5 設備類別（X-Dt）

編碼

名稱

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
