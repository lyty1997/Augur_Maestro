# 交易開放 API 介面文檔

# V 1 . 0

# 概述

開放平台可以為個人開發者和機構客戶提供介面服務，投資者可以充分的利用盈立智投的交易服務、報價服務、帳戶服務等實現自己的投資操作。

# 接入說明：

IP 白名單，授權訪問開放平台介面的 IP 位址，只有在白名單內的 IP 才能訪問服務。

# 協議：

HTTPS 

# X-Sign

使用MD5withRSA加密演算法對Body中的內容進行加密，得到的密文經過safeBase64編碼後做為X-Sign的值放入header當中，每一個管道單獨分配公私密金鑰。

驗簽測試公開金鑰為：

需雙方商定

隱私資料加密測試公開金鑰為：

需雙方商定

URLSAFE_BASE64 演算法在 RFC4648 中有定義

最終串會使用RSA私密金鑰進行加密，之後使用RFC4648演算法編碼放入請求體或表單項中。

請求頭 X-Request-Id:

長度為19位元數位，必須確保唯一用於做冪等防重，推薦使用分散式Snowflake雪花算法生成。

# 請求示例：


http header 參數示例


```txt
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiNGZjYTA1MWNmZjQ
wNDI4NzlkNGJiYzYzYjFiYWE0MTgiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozMTgxNDA2MTEwNTc1NTc1MD
R9.gw4_AKh6NGUxWXWjzHb8G2An3aoOnSuI
Content-Type: application/json; charset=utf-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 92823918712371
X-Type: 1
X-Channel : 1001
x-Sign : 用私密金鑰對 body內容加密後的內容
```


http body 參數示例：


```json
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
```


返回示例：


```txt
{
    "code": 0,
    "data": { 
```

```json
"entrustId": "56765633083899904",
"status": 0,
"statusName": "等待提交"
},
"msg": ""
}
```

# 1 用戶

# 1.1 管道密碼登錄

手機+密碼+管道登錄：

介面位址 /user-server/open-api/login

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 


請求參數說明：


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的requestId 資訊,長度30位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>areaCode</td><td>區域號86中國,852香港,853中國澳門,886中國台灣,65新加坡</td><td>body</td><td>true</td><td>string</td></tr><tr><td>password</td><td>密碼RSA加密(與X-Sign不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>phoneNumber</td><td>手機號 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例：

```json
{
    "areaCode": 86, "password":
    "rsa", "phoneNumber": "rsa"
} 
```

# 參數說明：

<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>areaCode</td><td>區號</td><td>string</td></tr><tr><td>avatar</td><td>頭像地址</td><td>string</td></tr><tr><td>expiration</td><td>過期時間</td><td>int64</td></tr><tr><td>extendStatusBit</td><td>用戶擴展狀態</td><td>int32</td></tr><tr><td>firstLogin</td><td>是否為第一次登陸</td><td>boolean</td></tr><tr><td>nickname</td><td>昵稱</td><td>string</td></tr><tr><td>openedAccount</td><td>是否開戶</td><td>boolean</td></tr><tr><td>phoneNumber</td><td>手機號</td><td>string</td></tr><tr><td>thirdBindBit</td><td>綁定位 手機 1&lt;&lt;0 微信 1&lt;&lt;1 微博 1&lt;&lt;2</td><td>int32</td></tr><tr><td>token</td><td>登錄授權的 token</td><td>string</td></tr><tr><td>tradePassword</td><td>是否設置過交易密碼</td><td>boolean</td></tr><tr><td>unionId</td><td>微信公眾平台的 unionId,如果有則顯示。</td><td>string</td></tr><tr><td>uuid</td><td>盈立用戶註冊的 uuid,全域唯一</td><td>int64</td></tr></table>

# 返回示例：

```json
{
    "areaCode": 86,
    "avatar": "",
    "expiration": 0,
    "extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
    "nickname": "xxx", "openedAccount":
    true, "phoneNumber": "188xxxx9188",
    "thirdBindBit": 1,
    "token": "", "tradePassword":
    true, "unionId": "", "uuid": 0
}
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td></tr><tr><td>0</td><td>成功</td></tr><tr><td>200</td><td>OK</td></tr><tr><td>300100</td><td>非法請求</td></tr><tr><td>300102</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td></tr><tr><td>300103</td><td>用戶被刪除</td></tr><tr><td>300309</td><td>請輸入正確的手機號碼</td></tr><tr><td>300701</td><td>該手機號沒有註冊</td></tr><tr><td>300702</td><td>密碼錯誤次數過多帳號已鎖定,請%s分鐘後重新登錄或找回密碼</td></tr><tr><td>300703</td><td>密碼錯誤,請重新輸入,您還可以嘗試%s次</td></tr><tr><td>300705</td><td>該帳戶未設置登錄密碼,請使用短信驗證碼登錄</td></tr><tr><td>300809</td><td>需要校驗手機短信驗證碼</td></tr></table>

# 1.2 獲取手機驗證碼

介面位址 /user-server/open-api/send-phone-captcha

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 


請求參數說明：


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的requestId 資訊,長度30位,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>areaCode</td><td>區域號86中國,852香港,853中國澳門,886中國臺灣,65新加坡</td><td>body</td><td>true</td><td>string</td></tr><tr><td>type</td><td>驗證碼類型101註冊102重置密碼103更換手機號104綁定手機號105新設備登錄校驗106短信登錄</td><td>body</td><td>true</td><td>string</td></tr><tr><td>phoneNumber</td><td>手機號RSA加密(與X-Sign不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例：

```json
{
    "areaCode": 86,
    "type": 102,
    "phoneNumber": "rsa"
} 
```


出參說明：


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>areaCode</td><td>區號</td><td>string</td></tr><tr><td>avatar</td><td>頭像地址</td><td>string</td></tr><tr><td>expiration</td><td>過期時間</td><td>int64</td></tr><tr><td>extendStatusBit</td><td>用戶擴展狀態</td><td>int32</td></tr><tr><td>firstLogin</td><td>是否為第一次登陸</td><td>boolean</td></tr><tr><td>invitationCode</td><td>邀請碼,如果有,則顯示。</td><td>string</td></tr><tr><td>languageCn</td><td>1 簡體 2 繁體</td><td>int32</td></tr><tr><td>languageHk</td><td>1 簡體 2 繁體</td><td>int32</td></tr><tr><td>lineColorHk</td><td>1 紅漲綠跌 2 綠漲紅跌</td><td>int32</td></tr><tr><td>nickname</td><td>昵稱</td><td>string</td></tr><tr><td>openedAccount</td><td>是否開戶</td><td>boolean</td></tr><tr><td>phoneNumber</td><td>手機號</td><td>string</td></tr><tr><td>thirdBindBit</td><td>綁定位 手機 1&lt;&lt;0 微信 1&lt;&lt;1 微博 1&lt;&lt;2</td><td>int32</td></tr><tr><td>token</td><td>登錄授權的 token</td><td>string</td></tr><tr><td>tradePassword</td><td>是否設置過交易密碼</td><td>boolean</td></tr><tr><td>unionId</td><td>微信公眾平台的 unionId,如果有則顯示。</td><td>string</td></tr><tr><td>uuid</td><td>盈立用戶註冊的 uuid,全域唯一</td><td>int64</td></tr></table>

# 返回示例：

```json
{
    "areaCode": 86,
    "avatar": "",
    "expiration": 0,
    "extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
    "invitationCode": 1234,
    "languageCn": 0,
    "languageHk": 0,
    "lineColorHk": 0, "nickname": "xxx",
    "openedAccount": true, "phoneNumber":
    "188xxxx9188", "thirdBindBit": 1,
    "token": "", "tradePassword":
    true, "unionId": "", "uuid": 0
}
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td></tr><tr><td>0</td><td>成功</td></tr><tr><td>200</td><td>OK</td></tr><tr><td>300100</td><td>非法請求</td></tr><tr><td>300102</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td></tr><tr><td>300103</td><td>用戶被刪除</td></tr><tr><td>300309</td><td>請輸入正確的手機號碼</td></tr><tr><td>300701</td><td>該手機號沒有註冊</td></tr><tr><td>300702</td><td>密碼錯誤次數過多帳號已鎖定,請%s分鐘後重新登錄或找回密碼</td></tr><tr><td>300703</td><td>密碼錯誤,請重新輸入,您還可以嘗試%s次</td></tr><tr><td>300705</td><td>該帳戶未設置登錄密碼,請使用短信驗證碼登錄</td></tr><tr><td>300809</td><td>需要校驗手機短信驗證碼</td></tr></table>

# 1.3 管道驗證碼登錄

手機+驗證碼+管道登錄：

介面位址 /user-server/open-api/loginCaptcha

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 


請求參數說明：


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的requestId 資訊,長度30位,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>areaCode</td><td>區域號86中國,852香港,853中國澳門,886中國臺灣,65新加坡</td><td>body</td><td>true</td><td>string</td></tr><tr><td>captcha</td><td>驗證碼</td><td>body</td><td>true</td><td>string</td></tr><tr><td>phoneNumber</td><td>手機號RSA加密(與X-Sign不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例：

```json
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
```

# 參數說明：

<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>areaCode</td><td>區號</td><td>string</td></tr><tr><td>avatar</td><td>頭像地址</td><td>string</td></tr><tr><td>expiration</td><td>過期時間</td><td>int64</td></tr><tr><td>extendStatusBit</td><td>用戶擴展狀態</td><td>int32</td></tr><tr><td>firstLogin</td><td>是否為第一次登陸</td><td>boolean</td></tr><tr><td>invitationCode</td><td>邀請碼,如果有,則顯示。</td><td>string</td></tr><tr><td>languageCn</td><td>1 簡體 2 繁體</td><td>int32</td></tr><tr><td>languageHk</td><td>1 簡體 2 繁體</td><td>int32</td></tr><tr><td>lineColorHk</td><td>1 紅漲綠跌 2 綠漲紅跌</td><td>int32</td></tr><tr><td>nickname</td><td>昵稱</td><td>string</td></tr><tr><td>openedAccount</td><td>是否開戶</td><td>boolean</td></tr><tr><td>phoneNumber</td><td>手機號</td><td>string</td></tr><tr><td>thirdBindBit</td><td>綁定位 手機 1&lt;&lt;0 微信 1&lt;&lt;1 微博 1&lt;&lt;2</td><td>int32</td></tr><tr><td>token</td><td>登錄授權的 token</td><td>string</td></tr><tr><td>tradePassword</td><td>是否設置過交易密碼</td><td>boolean</td></tr><tr><td>unionId</td><td>微信公眾平台的 unionId,如果有則顯示。</td><td>string</td></tr><tr><td>uuid</td><td>盈立用戶註冊的 uuid,全域唯一</td><td>int64</td></tr></table>

# 返回示例：

```json
{
    "areaCode": 86,
    "avatar": "",
    "expiration": 0,
    "extendStatusBit": "1<<0 登錄密碼 1<<1 行情許可權 1<<2 衍生品", "firstLogin": true,
    "invitationCode": 1234,
    "languageCn": 0,
    "languageHk": 0,
    "lineColorHk": 0, "nickname": "xxx",
    "openedAccount": true, "phoneNumber":
    "188xxxx9188", "thirdBindBit": 1,
    "token": "", "tradePassword":
    true, "unionId": "", "uuid": 0
}
```

# 回應狀態

<table><tr><td>狀態碼</td><td>說明</td></tr><tr><td>0</td><td>成功</td></tr><tr><td>200</td><td>OK</td></tr><tr><td>300100</td><td>非法請求</td></tr><tr><td>300102</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td></tr><tr><td>300103</td><td>用戶被刪除</td></tr><tr><td>300309</td><td>請輸入正確的手機號碼</td></tr><tr><td>300701</td><td>該手機號沒有註冊</td></tr><tr><td>300702</td><td>密碼錯誤次數過多帳號已鎖定,請%s分鐘後重新登錄或找回密碼</td></tr><tr><td>300703</td><td>密碼錯誤,請重新輸入,您還可以嘗試%s次</td></tr><tr><td>300705</td><td>該帳戶未設置登錄密碼,請使用短信驗證碼登錄</td></tr><tr><td>300809</td><td>需要校驗手機短信驗證碼</td></tr></table>

# 1.4 設置交易密碼

介面位址 /user-server/open-api/set-trade-password

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 需帶登錄態 token 使用者需要完成開戶，且未設置過交易密碼，否則算非法請求


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言 1 簡體 2 繁體</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>交易密碼 設置、修改、重置交易密碼必填,交易密碼必須是 6 位元純數位 RSA 加密(與X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>oldPassword</td><td>舊交易密碼 修改交易密碼必填,交易密碼必須是 6 位元純數位 RSA 加密(與X-Sign 不同秘鑰)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>phoneCaptcha</td><td>手機驗證碼,根據驗證碼重置交易密碼必填</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 

X-Dt: 1 

X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"oldPassword": "", 

"password": "", "phoneCaptcha": 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300101</td><td>非法 TOKEN</td><td></td></tr><tr><td>301001</td><td>交易密碼需為 6 位元純數字,請重新輸入</td><td></td></tr><tr><td>301003</td><td>交易密碼錯誤,請重新輸入,您還可以嘗試%s 次</td><td></td></tr><tr><td>301004</td><td>交易服務異常</td><td></td></tr><tr><td>301005</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"data": {}, 

"msg": "" 

} 

# 1.5 校驗交易密碼

介面位址 /user-server/open-api/check-trade-password

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 許可權：需要 Token


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,19 位元長度</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>交易密碼必須是6 位元純數位 RSA 加密(與 X-Sign 不同秘鑰)</td><td>String</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Dt: 1 

X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

/user-server/open-api/check-trade-password?password=123456 RES 加密


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300101</td><td>非法 TOKEN</td><td></td></tr><tr><td>301001</td><td>交易密碼需為6位元純數字,請重新輸入</td><td></td></tr><tr><td>301002</td><td>錯誤次數過多交易密碼已鎖定,請%s小時後重新嘗試或找回密碼</td><td></td></tr><tr><td>301004</td><td>交易服務異常</td><td></td></tr><tr><td>310104</td><td>交易密碼錯誤</td><td></td></tr><tr><td>310106</td><td>未設置交易密碼</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "data": {},
    "msg": ""
} 
```

# 1.6 重置登錄密碼

介面位址 /user-server/open-api/reset-login-password

# 請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 不需要 token


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>areaCode</td><td>區域號 86 中國,852 香港,853 中國澳門,886 中國臺灣,65 新加坡</td><td>body</td><td>false</td><td>string</td></tr><tr><td>password</td><td>新密碼 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>phoneCaptcha</td><td>手機驗證碼</td><td>body</td><td>false</td><td>string</td></tr><tr><td>phoneNumber</td><td>手機號 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Dt: 1 

X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

# 請求 body 示例

```json
{
    "areaCode": "86", "password": "rsa",
    "phoneCaptcha": "1234",
    "phoneNumber": "188********"
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300304</td><td>驗證次數過多,請稍後重試</td><td></td></tr><tr><td>300305</td><td>抱歉,驗證碼已過期,請重新獲取</td><td></td></tr><tr><td>300701</td><td>該手機號沒有註冊</td><td></td></tr><tr><td>300707</td><td>您當前已通過客戶經理完成預註冊,請通過短信驗證碼登錄並啟動帳號。</td><td></td></tr><tr><td>300800</td><td>短信驗證碼不正確,請重新輸入</td><td></td></tr><tr><td>300801</td><td>密碼長度不能小於8位</td><td></td></tr><tr><td>300802</td><td>密碼長度不能大於24位</td><td></td></tr><tr><td>300803</td><td>密碼不能為純數位/字母/符號</td><td></td></tr><tr><td>300804</td><td>請設置正確密碼,8~24位元數位/字母/符號組合</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"data": {}, 

"msg": " 

} 

# 1.7 解鎖交易

介面位址 /user-server/open-api/trade-login

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 需要 token

# 請求參數

<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>新密碼 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

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


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300304</td><td>驗證次數過多,請稍後重試</td><td></td></tr><tr><td>300305</td><td>抱歉,驗證碼已過期,請重新獲取</td><td></td></tr><tr><td>300701</td><td>該手機號沒有註冊</td><td></td></tr><tr><td>300707</td><td>您當前已通過客戶經理完成預註冊,請通過短信驗證碼登錄並啟動帳號。</td><td></td></tr><tr><td>300800</td><td>短信驗證碼不正確,請重新輸入</td><td></td></tr><tr><td>300801</td><td>密碼長度不能小於8位</td><td></td></tr><tr><td>300802</td><td>密碼長度不能大於24位</td><td></td></tr><tr><td>300803</td><td>密碼不能為純數位/字母/符號</td><td></td></tr><tr><td>300804</td><td>請設置正確密碼,8~24位元數位/字母/符號組合</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>


回應示例


```json
{
    "code": 0,
    "data": ,
    "msg": ""
} 
```

# 1.8 獲取交易解鎖狀態

介面位址 /user-server/open-api/get-trade-status

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 需要 token

請求參數

<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>新密碼 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

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


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300304</td><td>驗證次數過多,請稍後重試</td><td></td></tr><tr><td>300305</td><td>抱歉,驗證碼已過期,請重新獲取</td><td></td></tr><tr><td>300701</td><td>該手機號沒有註冊</td><td></td></tr><tr><td>300707</td><td>您當前已通過客戶經理完成預註冊,請通過短信驗證碼登錄並啟動帳號。</td><td></td></tr><tr><td>300800</td><td>短信驗證碼不正確,請重新輸入</td><td></td></tr><tr><td>300801</td><td>密碼長度不能小於8位</td><td></td></tr><tr><td>300802</td><td>密碼長度不能大於24位</td><td></td></tr><tr><td>300803</td><td>密碼不能為純數位/字母/符號</td><td></td></tr><tr><td>300804</td><td>請設置正確密碼,8~24位元數位/字母/符號組合</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>status</td><td>訂單狀態,0 未解密,1 已解鎖</td><td>int32</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0, "msg": "
    成功", "data": {
    "status": 0
    }
}
```

# 1.9 修改交易密碼

介面位址 /user-server/open-api/update-trade-password

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言 1 簡體 2 繁體</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>交易密碼 必填,交易密碼必須是 6 位元純數位 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>oldPassword</td><td>舊交易密碼 修改交易密碼必填,交易密碼必須是 6 位元純數位 RSA 加密(與X-Sign 不同秘鑰)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>phoneCaptcha</td><td>手機驗證碼,根據驗證碼重置交易密碼必填</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

```txt
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohaib0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例

```json
{
    "oldPassword": "",
    "password": "", "phoneCaptcha":
    ""
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300101</td><td>非法 TOKEN</td><td></td></tr><tr><td>301001</td><td>交易密碼需為6位元純數字,請重新輸入</td><td></td></tr><tr><td>301003</td><td>交易密碼錯誤,請重新輸入,您還可以嘗試%s次</td><td></td></tr><tr><td>301004</td><td>交易服務異常</td><td></td></tr><tr><td>301005</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "data": {},
    "msg": ""
} 
```

# 1.10 重置交易密碼

介面位址 /user-server/open-api/reset-trade-password

請求方式 POST

consumes ["application/json"] 

介面描述 需帶登錄態 token 使用者需要完成開戶，且未設置過交易密碼，否則算非法請求


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言 1 簡體 2 繁體</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>交易密碼 必填,交易密碼必須是 6 位元純數位 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>oldPassword</td><td>舊交易密碼 非必填,交易密碼必須是 6 位元純數位 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>phoneCaptcha</td><td>手機驗證碼,根據驗證碼重置交易密碼必填</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Dt: 1 

X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"oldPassword": "", 

```txt
"password": "",
"phoneCaptcha": ""
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>User ResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300101</td><td>非法 TOKEN</td><td></td></tr><tr><td>301001</td><td>交易密碼需為6位元純數字,請重新輸入</td><td></td></tr><tr><td>301003</td><td>交易密碼錯誤,請重新輸入,您還可以嘗試%s次</td><td></td></tr><tr><td>301004</td><td>交易服務異常</td><td></td></tr><tr><td>301005</td><td>帳戶被凍結,無法完成操作,如非本人操作,請聯繫客服</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "data": {},
    "msg": ""
} 
```

# 1.11 修改登陸密碼

介面位址 /user-server/open-api/update-login-password

請求方式 POST

consumes ["application/json"] 

介面描述 需帶登錄態 token 使用者需要已設置登陸密碼，否則算非法請求


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>見概述 Authorization 說明</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言 1 簡體 2 繁體</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,長度 30 位,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>password</td><td>新登陸密碼 必填 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>oldPassword</td><td>舊登陸密碼 必填 RSA 加密(與 X-Sign 不同秘鑰)</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例

```json
{
    "oldPassword": "",
    "password": "",
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>UserResponseEntity</td></tr><tr><td>300100</td><td>非法請求</td><td></td></tr><tr><td>300101</td><td>非法 TOKEN</td><td></td></tr><tr><td>300704</td><td>原登陸密碼不正確</td><td></td></tr><tr><td>300804</td><td>請設置正確密碼,8~24 位元數位/字母/符號組合</td><td></td></tr><tr><td>300810</td><td>新密碼長度不能小於 8 位</td><td></td></tr><tr><td>300811</td><td>新密碼長度不能大於 24 位</td><td></td></tr><tr><td>300812</td><td>新密碼不能為純數位/字母/符號</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>回應碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>回應體</td><td>object</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "data": {},
    "msg": ""
} 
```

# 2 交易

# 2.1 下單

介面位址 /stock-order-server/open-api/entrust-order

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Dt</td><td>設備類型(t1-android,t2-ios,t3-其他,t4-Windows,t5-Mac)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的requestId 資訊,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>serialNo</td><td>流水號,最長 19 位,確保唯一推薦雪花演算法生成</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>entrustAmount</td><td>委託數量</td><td>body</td><td>true</td><td>number</td></tr><tr><td>entrustPrice</td><td>價格(競價單價格傳 0)</td><td>body</td><td>true</td><td>number</td></tr><tr><td>entrustProp</td><td>委託屬性(&#x27;0&#x27;-美股限價單/ 暗盤委託 limit order,&#x27;d&#x27;-競價單,&#x27;e&#x27;-增強限價單,&#x27;g&#x27;-競價限價單)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>entrustType</td><td>委託類別(0-買,1-賣)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,6-滬港通,7-深港通)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>stockCode</td><td>股票代碼</td><td>body</td><td>true</td><td>string</td></tr><tr><td>password</td><td>交易密碼(RDA 公開金鑰加密)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>stockName</td><td>股票名稱</td><td>body</td><td>false</td><td>string</td></tr><tr><td>forceEntrustFlag</td><td>是否強制委託標記,超過 9 倍 24 檔下單時 forceEntrustFlag=true 可強制下單,但有可能是廢單</td><td>body</td><td>false</td><td>boolean</td></tr><tr><td>sessionType</td><td>交易階段標誌(0/不傳-正常訂單交易(預設),1-盤前,2-盤後交易,3-暗盤交易)</td><td>body</td><td>false</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Dt: 1 

X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

```json
{
    "serialNo": "200000000000000018",
    "entrustAmount": "1000",
    "entrustPrice": "11.0",
    "entrustProp": "e",
    "entrustType": "0",
    "exchangeType": "0",
    "stockCode": "00981",
    "stockName": "00981", "forceEntrustFlag":
    "false", "sessionType": "0",
    "password":"Fpocc_11vTS6mS9YKYby6-v2VNujUx_fnnMaGncHPerLh9mCP_vDIhbeE1GLNDU4arl1euay-hiTmqmlwZlwtCMbw3Law7mx9NgVuwGVX3pXPuwYjcqxhaGZIsATHDSywxd4uZZhTCsrRua-Ug8dgJaPDc5os7-A9sFYxbxhI6I="
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«EntrustOrderResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr><tr><td>406472</td><td>訂單中不能包含小於1手數量的碎股,請交易1手的整數倍,或通過&quot;碎股單&quot;交易碎股</td><td></td></tr><tr><td>410200</td><td>抱歉,訂單中不能包含小於1手數量的碎股,請交易1手的整數倍,如需交易碎股請聯繫客服。</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>EntrustOrderResponse</td><td>EntrustOrderResponse</td></tr><tr><td>entrustId</td><td>訂單 id,可用於查詢訂單/修改訂單/取消訂單</td><td>string</td><td></td></tr><tr><td>status</td><td>訂單狀態</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>訂單狀態名稱</td><td>string</td><td></td></tr><tr><td>·msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "entrustId": "1181776863632019456",
    "status": 1, "statusName": "等待提交"
    }
}
```

# 2.2 委託改單/撤單

介面位址 /stock-order-server/open-api/modify-order

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 委託改單/撤單


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>actionType</td><td>操作類型(0-撤單,1-改單)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>entrustAmount</td><td>委託數量,撤單時傳 0</td><td>body</td><td>true</td><td>number</td></tr><tr><td>entrustId</td><td>委託 Id</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>entrustPrice</td><td>委託價格,撤單時傳 0</td><td>body</td><td>true</td><td>number</td></tr><tr><td>password</td><td>交易密碼(RDA公開金鑰加密)</td><td>body</td><td>false</td><td>string</td></tr><tr><td>forceEntrustFlag</td><td>是否強制委託標記,超過9倍24檔下單時 forceEntrustFlag=true 可強制下單,但有可能是廢單</td><td>body</td><td>false</td><td>boolean</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Request-Id: 928239187123721231232 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"actionType": 1, 

"entrustAmount": 500, 

"entrustId": 1181776863632019456, 

"entrustPrice": 322.0, 

"forceEntrustFlag": true 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td></td></tr><tr><td>200</td><td>OK</td><td>Object</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr><tr><td>406472</td><td>訂單中不能包含小於1手數量的碎股,請交易1手的整數倍,或通過&quot;碎股單&quot;交易碎股</td><td></td></tr><tr><td>410200</td><td>抱歉,訂單中不能包含小於1手數量的碎股,請交易1手的整數倍,如需交易碎股請聯繫客服。</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>Object</td><td></td></tr><tr><td>entrustId</td><td>申請編號</td><td>string</td><td></td></tr><tr><td>status</td><td>狀態</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>狀態名</td><td>string</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "entrustId": "1181776863632019456",
    "status": 5, "statusName": "等待改單"
    }
}
```

# 2.3 改單範圍

介面位址 /stock-order-server/open-api/modified-range

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 改單展

示範圍


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>entrustId</td><td>委託 Id</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>newPrice</td><td>最新價-競價單也需要傳最新價</td><td>body</td><td>true</td><td>number</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 

X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求示例

{ 

"entrustId": 1181776863632019456, 

"newPrice": 323 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«QueryEntrustInfoResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>QueryEntrustInfoResponse</td><td>QueryEntrustInfoResponse</td></tr><tr><td>businessAmount</td><td>成交數量</td><td>number</td><td></td></tr><tr><td>entrustAmount</td><td>原訂單數量</td><td>number</td><td></td></tr><tr><td>modifiedUpperAmount</td><td>可修改範圍的修改上限</td><td>number</td><td></td></tr><tr><td>modifiedlowerAmount</td><td>可修改範圍的修改下限</td><td>number</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"data": { 

"businessAmount": 0, 

"entrustAmount": 0, 

"modifiedUpperAmount": 0, 

"modifiedlowerAmount": 0 

}, 

"msg": "" 

} 

# 2.4 碎股下單

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


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Dt</td><td>設備類型 (t1-android,t2-ios,t3-其他,t4-Windows,t5-Mac)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>entrustAmount</td><td>委託數量</td><td>body</td><td>true</td><td>number</td></tr><tr><td>entrustPrice</td><td>價格</td><td>body</td><td>true</td><td>number</td></tr><tr><td>entrustType</td><td>委託類別(1-賣)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>stockCode</td><td>股票代碼</td><td>body</td><td>true</td><td>string</td></tr></table>

回應狀態

<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td></td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td></tr><tr><td>data</td><td>返回體</td><td></td></tr><tr><td>oddId</td><td>碎股請求記錄 id</td><td>string</td></tr><tr><td>status</td><td>訂單狀態</td><td>int32</td></tr><tr><td>statusName</td><td>訂單狀態名稱</td><td>string</td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "oddId": "1207553433704988672",
    "status": 0,
    "statusName": "待报单"
    }
}
```

# 2.5 碎股撤單

介面位址 /stock-order-server/open-api/odd-modify

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

# 介面描述 碎股交易

# 請求示例

{ 

"actionType": 0, 

"oddId": 1207553433704988672 

} 


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>actionType</td><td>操作類型(0-撤單)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>oddId</td><td>碎股委託 Id</td><td>body</td><td>true</td><td>int64</td></tr></table>


回應狀態


<table><tr><td>狀態碼</td><td>說明</td></tr><tr><td>200</td><td>OK</td></tr><tr><td>201</td><td>Created</td></tr><tr><td>401</td><td>Unauthorized</td></tr><tr><td>403</td><td>Forbidden</td></tr><tr><td>404</td><td>Not Found</td></tr></table>

# 回應參數

<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td></tr><tr><td>oddId</td><td>碎股請求記錄 id</td><td>string</td></tr><tr><td>status</td><td>訂單狀態</td><td>int32</td></tr><tr><td>statusName</td><td>訂單狀態名稱</td><td>string</td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td></tr></table>


回應示例


```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "oddId": "1207553433704988672",
    "status": 9,
    "statusName": "已撤单"
    }
}
```

# 2.6 最大可買、可賣數量

介面位址 /stock-order-server/open-api/trade-quantity

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 獲取最

大可用數量


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>entrustPrice</td><td>委託價格(不能為0,競價單可不填)</td><td>body</td><td>false</td><td>number</td></tr><tr><td>entrustProp</td><td>委託屬性('0'-美股限價單,'d'-競價單,'e'-增強限價單,'g'-競價限價單,'u'-碎股單)</td><td>body</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,6-滬港通,7-深港通)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>stockCode</td><td>證券代碼</td><td>body</td><td>true</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"entrustPrice": 234, "entrustProp": 

"e", "exchangeType": 0, 

"stockCode": "700" 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«SaleAndBuyQuantityResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>SaleAndBuyQuantityResponse</td><td>SaleAndBuyQuantityResponse</td></tr><tr><td>buyEnableAmount</td><td>最大可買數量</td><td>number</td><td></td></tr><tr><td>oddEnableAmount</td><td>最大可賣碎股數量</td><td>number</td><td></td></tr><tr><td>saleEnableAmount</td><td>最大可賣數量</td><td>number</td><td></td></tr><tr><td>saleEnableIntAmount</td><td>最大可賣整股數量</td><td>number</td><td></td></tr><tr><td>handAmount</td><td>每手股數</td><td>number</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
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
```

# 2.7 今日訂單-分頁查詢

介面位址 /stock-order-server/open-api/today-entrust

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 需要資

金帳號


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,67-A股,100-查詢所有交易類別)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>pageNum</td><td>當前頁1開始,預設值1</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>pageSize</td><td>每頁結果數,預設值10</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>stockCode</td><td>證券代碼</td><td>body</td><td>false</td><td>string</td></tr><tr><td>stockName</td><td>證券名稱</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"exchangeType": 0, 

"pageNum": 1, 

"pageSize": 10, "stockCode": "", 

"stockName": "" 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«PageInfoVO«TodayEntrustByAppResponse»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>PageInfoVO«TodayEntrustByAppResponse»</td><td>PageInfoVO«TodayEntrustByAppResp onse»</td></tr><tr><td>list</td><td>結果集合</td><td>array</td><td>TodayEntrustByAppResponse</td></tr><tr><td>businessAmount</td><td>成交數量</td><td>number</td><td></td></tr><tr><td>businessAveragePrice</td><td>成交均價</td><td>number</td><td></td></tr><tr><td>serialNo</td><td>流水號</td><td>int64</td><td></td></tr><tr><td>createTime</td><td>委託時間</td><td>string</td><td></td></tr><tr><td>entrustAmount</td><td>委託數量</td><td>number</td><td></td></tr><tr><td>entrustId</td><td>委託 id</td><td>string</td><td></td></tr><tr><td>entrustNo</td><td>委託編號</td><td>string</td><td></td></tr><tr><td>entrustPrice</td><td>委託價格</td><td>number</td><td></td></tr><tr><td>entrustProp</td><td>委託屬性('0'-美股限價單,'d'-競價單,'e'-增強限價單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)</td><td>string</td><td></td></tr><tr><td>entrustType</td><td>買賣方向,委託類型(0-買,1-賣)</td><td>int32</td><td></td></tr><tr><td>exchangeType</td><td>交易類別,0 港股,5 美股</td><td>int32</td><td></td></tr><tr><td>flag</td><td>訂單類型-普通單 0-條件單 1-碎股單 2-月供股單</td><td>string</td><td></td></tr><tr><td>moneyType</td><td>幣種類別</td><td>int32</td><td></td></tr><tr><td>sessionType</td><td>交易階段標誌(0/不傳-正常訂單交易(預設),1-盤前,2-盤後交易,3-暗盤交易)</td><td>int32</td><td></td></tr><tr><td>status</td><td>委託狀態</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>委託狀態名</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票簡體名稱</td><td>string</td><td></td></tr><tr><td>pageNum</td><td>當前頁</td><td>int32</td><td></td></tr><tr><td>pageSize</td><td>每頁條數</td><td>int32</td><td></td></tr><tr><td>total</td><td>總數</td><td>int64</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

```json
"msg": "操作成功",
"data": {
    "pageNum": 1,
    "pageSize": 0,
    "total": 1,
    "list": [
    {
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
    }
    ]
}
```

# 2.8 全部訂單-分頁查詢

介面位址 /stock-order-server/open-api/his-entrust

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 需要資

金帳號


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>dateFlag</td><td>1:一周訂單,2:一個月訂單,3:三個月訂單,4:近一年訂單,5:今年訂單,6:自選時間,7.查詢全部</td><td>body</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,67-A股,100-查詢所有交易類別)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>entrustBeginDate</td><td>開始時間,如果不傳時間默認從最新前一天倒序,規則 yyyy-MM-dd</td><td>body</td><td>false</td><td>string</td></tr><tr><td>entrustEndDate</td><td>結束時間,如果不傳時間默認從最新前一天倒序,規則 yyyy-MM-dd</td><td>body</td><td>false</td><td>string</td></tr><tr><td>pageNum</td><td>當前頁1開始,預設值1</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>pageSize</td><td>每頁結果數,預設值10</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>stockCode</td><td>證券代碼</td><td>body</td><td>false</td><td>string</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

```javascript
"dateFlag": "1",
"entrustBeginDate": "",
"entrustEndDate": "",
"exchangeType": 0,
"pageNum": 1,
"pageSize": 10,
"stockCode": "" 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«PageInfoVO«HisEntrustByAppResponse»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>PageInfoVO«HisEntrustByAppResponse»</td><td>PageInfoVO«HisEntrustByAppResponse»</td></tr><tr><td>list</td><td>結果集合</td><td>array</td><td>HisEntrustByAppResponse</td></tr><tr><td>businessAmount</td><td>成交數量</td><td>number</td><td></td></tr><tr><td>businessAveragePrice</td><td>成交均價</td><td>number</td><td></td></tr><tr><td>serialNo</td><td>流水號</td><td>int64</td><td></td></tr><tr><td>createDate</td><td>委託日期</td><td>string</td><td></td></tr><tr><td>createTime</td><td>委託時間</td><td>string</td><td></td></tr><tr><td>dayEnd</td><td>是否隔天,0未隔天,1已經隔天</td><td>int32</td><td></td></tr><tr><td>entrustAmount</td><td>委託數量</td><td>number</td><td></td></tr><tr><td>entrustId</td><td>委託ID</td><td>string</td><td></td></tr><tr><td>entrustNo</td><td>委託編號</td><td>string</td><td></td></tr><tr><td>entrustPrice</td><td>委託價格</td><td>number</td><td></td></tr><tr><td>entrustProp</td><td>委託屬性('0'-美股限價單,'d'-競價單,'e'-增強限價單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)</td><td>string</td><td></td></tr><tr><td>entrustType</td><td>買賣方向,委託類型(0-買,1-賣)</td><td>int32</td><td></td></tr><tr><td>exchangeType</td><td>交易類別,0港股,5美股</td><td>int32</td><td></td></tr><tr><td>flag</td><td>訂單類型-普通單1-條件單2-碎股單3-月供股單4</td><td>string</td><td></td></tr><tr><td>moneyType</td><td>幣種類別</td><td>int32</td><td></td></tr><tr><td>sessionType</td><td>交易階段標誌(0/不傳-正常訂單交易(預設),1-盤前,2-盤後交易,3-暗盤交易)</td><td>int32</td><td></td></tr><tr><td>status</td><td>委託狀態</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>委託狀態名</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票簡體名稱</td><td>string</td><td></td></tr><tr><td>pageNum</td><td>當前頁</td><td>int32</td><td></td></tr><tr><td>pageSize</td><td>每頁條數</td><td>int32</td><td></td></tr><tr><td>total</td><td>總數</td><td>int64</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 2,
    "list": [
    {
    "entrustId": "1181776863632019456",
    "entrustNo": "191",
    "status": 5, "statusName": "等待改單", "exchangeType": 0,
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
    ]
    ],
```

```txt
"nowDate": "20191009"
}
} 
```

# 2.9 查詢訂單明細

介面位址 /stock-order-server/open-api/order-detail

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 查詢訂

單明細


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>appEntrustRecordDetail Request</td><td>appEntrustRecordDetailRequest</td><td>body</td><td>true</td><td>AppEntrustRecordDetailRequest</td></tr><tr><td>serialNo</td><td>流水號(委託 ID、流水號一個至少傳一個)</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>entrustId</td><td>委託 id(委託 ID、流水號一個至少傳一個)</td><td>body</td><td>true</td><td>int64</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求示例

{ } 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«AppEntrustRecordDetailResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>AppEntrustRecordDetailResponse</td><td>AppEntrustRecordDetailResponse</td></tr><tr><td>appEntrustRecordDetailInfoList</td><td>list 信息</td><td>array</td><td>AppEntrustRecordDetailInfo</td></tr><tr><td>businessAmount</td><td>成交數量</td><td>number</td><td></td></tr><tr><td>businessAveragePrice</td><td>成交均價</td><td>number</td><td></td></tr><tr><td>businessBalance</td><td>成交金額</td><td>number</td><td></td></tr><tr><td>commissionFee</td><td>港美,佣金</td><td>string</td><td></td></tr><tr><td>createTime</td><td>時間</td><td>string</td><td></td></tr><tr><td>depositStockDay</td><td>股份到賬時間</td><td>string</td><td></td></tr><tr><td>entrustId</td><td>委託記錄號</td><td>int64</td><td></td></tr><tr><td>entrustAmount</td><td>委託數量</td><td>number</td><td></td></tr><tr><td>entrustBalance</td><td>委託金額</td><td>number</td><td></td></tr><tr><td>entrustFee</td><td>總費用</td><td>string</td><td></td></tr><tr><td>entrustPrice</td><td>委託價格</td><td>number</td><td></td></tr><tr><td>entrustProp</td><td>委託屬性('0'-美股限價單,'d'-競價單,'e'-增強限價單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)</td><td>string</td><td></td></tr><tr><td>entrustPropName</td><td>委託屬性('0'-美股限價單,'d'-競價單,'e'-增強限價單,'g'-競價限價單,'h'-港股限價單,'j'-特殊限價單)</td><td>string</td><td></td></tr><tr><td>moneyType</td><td>幣種類別</td><td>int32</td><td></td></tr><tr><td>orderStatus</td><td>狀態</td><td>int32</td><td></td></tr><tr><td>orderStatusName</td><td>狀態名</td><td>string</td><td></td></tr><tr><td>payFee</td><td>港美,交收費</td><td>string</td><td></td></tr><tr><td>platformUseFee</td><td>港美,平台使用費</td><td>string</td><td></td></tr><tr><td>stampDutyFee</td><td>港,印花稅</td><td>string</td><td></td></tr><tr><td>tradingSystemUsage</td><td>港,交易系統使用費</td><td>string</td><td></td></tr><tr><td>transactionFee</td><td>港:交易費,美:證監會費</td><td>string</td><td></td></tr><tr><td>transactionLevyFee</td><td>港,交易徵費,美:交易活動費</td><td>string</td><td></td></tr><tr><td>document</td><td>文案信息</td><td>string</td><td></td></tr><tr><td>entrustType</td><td>買入賣出</td><td>int32</td><td></td></tr><tr><td>exchangeType</td><td>市場類型</td><td>int32</td><td></td></tr><tr><td>sessionType</td><td>交易階段標誌(0/不傳-正常訂單交易(預設),1盤前,2盤後交易,3暗盤交易)</td><td>int32</td><td></td></tr><tr><td>status</td><td>委託狀態</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>委託狀態名</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"msg": "操作成功",

"data": { 

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

```json
{
    "transactionFee": null,
    "transactionLevyFee": null,
    "tradingSystemUsage": null,
    "entrustFee": null, "orderStatus": 21,
    "orderStatusName": "改單（最新訂單）"
},
{
    "entrustProp": "e", "entrustPropName": "增強限價單", "entrustAmount": 700,
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
```

# 2.10 查詢成交流水-分頁查詢

介面位址 /stock-order-server/open-api/stock-record

請求方式 POST

# 金帳號


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,67-A股,100-查詢所有交易類別)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>stockCode</td><td>股票代碼</td><td>body</td><td>false</td><td>string</td></tr><tr><td>entrustId</td><td>委託 ID</td><td>body</td><td>false</td><td>int64</td></tr><tr><td>beginTime</td><td>成交開始時間,規則 yyyy-MM-dd</td><td>body</td><td>false</td><td>string</td></tr><tr><td>endTime</td><td>成交結束時間,規則 yyyy-MM-dd</td><td>body</td><td>false</td><td>string</td></tr><tr><td>pageNum</td><td>當前頁 1 開始,預設值 1</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>pageSize</td><td>每頁結果數,預設值 10</td><td>body</td><td>false</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求示例

"beginTime": "2019-10-01", 

"endTime": "2019-10-10", 

"entrustId": 0, 

"exchangeType": 0, 

"pageNum": 1, 

"pageSize": 10, 

"stockCode": "700" 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«PageInfoVO«StockRecordResponse»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>PageInfoVO«StockRecordResponse»</td><td>PageInfoVO«Stoc kRecordResponse »</td></tr><tr><td>list</td><td>結果集合</td><td>array</td><td>StockRecordResponse</td></tr><tr><td>businessAmount</td><td>成交數量</td><td>number</td><td></td></tr><tr><td>businessBalance</td><td>成交金額</td><td>number</td><td></td></tr><tr><td>businessPrice</td><td>成交價格</td><td>number</td><td></td></tr><tr><td>businessStatus</td><td>成交狀態(1 成交成功,2 成交取消)</td><td>int32</td><td></td></tr><tr><td>businessTime</td><td>成交時間</td><td>date-time</td><td></td></tr><tr><td>createTime</td><td>記錄創建時間</td><td>date-time</td><td></td></tr><tr><td>entrustId</td><td>委託記錄號</td><td>int64</td><td></td></tr><tr><td>entrustType</td><td>委託類型("0"-買,1-賣,"2"-查詢,"3'-撤單,"4'-補單,"5"-改單,6轉入,7轉出,8 成交取消類型)</td><td>int32</td><td></td></tr><tr><td>exchangeType</td><td>交易類別('0'-香港,'1'-上海A,'2'-上海B,'3'-深圳A,'4'-深證B,'5'-美股,'6'-滬股通,'7'-深港通)</td><td>int32</td><td></td></tr><tr><td>id</td><td></td><td>int64</td><td></td></tr><tr><td>moneyType</td><td>幣種類型(0-人民幣,1-美元,2-港幣)</td><td>int32</td><td></td></tr><tr><td>recordId</td><td>成交流水編號</td><td>int64</td><td></td></tr><tr><td>remark</td><td>備註</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>updateTime</td><td>記錄最後更新時間</td><td>date-time</td><td></td></tr><tr><td>userId</td><td>用戶 id</td><td>int64</td><td></td></tr><tr><td>pageNum</td><td>當前頁</td><td>int32</td><td></td></tr><tr><td>pageSize</td><td>每頁條數</td><td>int32</td><td></td></tr><tr><td>total</td><td>總數</td><td>int64</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "pageNum": 1,
    "pageSize": 10,
    "total": 133,
    "list": [
    {
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
    "businessTime": "2019-06-14T09:12:49.000+0000", "createTime": "2019-06-13T09:20:00.000+0000", "updateTime": "2019-06-13T09:20:00.000+0000",
    "remark": null,
    "entrustType": 0,
    "businessBalance": 3342
    }]
    }
}
```

# 2.11 查詢持倉

介面位址 /stock-order-server/open-api/stock-holding

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 需要資金帳號


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td></td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td></td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td></td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td></td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td></td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td></td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,67-A股,100-查詢所有交易類別)</td><td></td><td>body</td><td>true</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 查詢請求 body 示例

{ 

"exchangeType": 0 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«List«StockHolding»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>array</td><td>StockHolding</td></tr><tr><td>costPriceAccurate</td><td>成本價--精確</td><td>string</td><td></td></tr><tr><td>currentAmount</td><td>持倉數量</td><td>string</td><td></td></tr><tr><td>enableAmount</td><td>可賣數量</td><td>string</td><td></td></tr><tr><td>frozenAmount</td><td>凍結數量</td><td>string</td><td></td></tr><tr><td>exchangeType</td><td>交易類型</td><td>int32</td><td></td></tr><tr><td>oddAmount</td><td>碎股數量</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>lastPrice</td><td>最新價</td><td>string</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"msg": "操作成功",

"data": [{ 

"exchangeType": 0, 

"stockCode": "19981", "stockName": "國藥麥

銀零四沽 A", "currentAmount":

"157.000000", 

"oddAmount": "157.000000", 

```jsonl
"lastPrice": "0.320000",
"costPriceAccurate": "0.303000000"
} 
```

# 2.12 查詢資產

介面位址 /stock-order-server/open-api/stock-asset

請求方式 POST

consumes ["application/json"] 

produces ["application/json"] 

介面描述 需要資金帳號


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別 (1-簡體, 2-繁體, 3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間戳記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別(0-香港,5-美股,67-A股)</td><td>body</td><td>true</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

```json
{
    "exchangeType": 0
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«StockAssetDTO»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td>+</td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>StockAssetDTO</td><td>StockAssetDTO</td></tr><tr><td>asset</td><td>總資產</td><td>string</td><td></td></tr><tr><td>enableBalance</td><td>可用金額</td><td>string</td><td></td></tr><tr><td>frozenBalance</td><td>凍結金額</td><td>string</td><td></td></tr><tr><td>onWayBalance</td><td>在途資金</td><td>string</td><td></td></tr><tr><td>stockHoldingList</td><td>持倉列表</td><td>array</td><td>StockHolding</td></tr><tr><td>costPriceAccurate</td><td>成本價--精確</td><td>string</td><td></td></tr><tr><td>currentAmount</td><td>持倉數量</td><td>string</td><td></td></tr><tr><td>exchangeType</td><td>交易類型</td><td>int32</td><td></td></tr><tr><td>oddAmount</td><td>碎股數量</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>withdrawBalance</td><td>可取金額</td><td>string</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>


回應示例


```json
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
    "stockCode": "19981", "stockName": "國藥麥銀零四沽 A", "currentAmount": "157.000000",
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
```

# 2.13 客戶股票資產查詢批量

介面位址 /stock-order-server/open-api/stock-asset-list

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介面描述 需要資

金帳號

請求示例

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"exchangeType": 100 

} 


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Type</td><td>APP 類別(1-大陸版,2-港版)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>stockAssetForAppReq</td><td>stockAssetForAppReq</td><td>body</td><td>true</td><td>StockAssetForAppReq</td></tr><tr><td>exchangeType</td><td>交易類別,0 港股,5 美股</td><td>body</td><td>true</td><td>int32</td></tr></table>


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«List«StockAssetDTO»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td></tr><tr><td>data</td><td>返回體</td><td>array</td></tr><tr><td>asset</td><td>總資產</td><td>string</td></tr><tr><td>enableBalance</td><td>可用金額</td><td>string</td></tr><tr><td>frozenBalance</td><td>凍結金額</td><td>string</td></tr><tr><td>marketValue</td><td>股票市值</td><td>string</td></tr><tr><td>onWayBalance</td><td>在途資金</td><td>string</td></tr><tr><td>stockHoldingList</td><td>持倉列表</td><td>array</td></tr><tr><td>costPrice</td><td>成本價</td><td>string</td></tr><tr><td>costPriceAccurate</td><td>成本價--精確</td><td>string</td></tr><tr><td>currentAmount</td><td>持倉數量</td><td>string</td></tr><tr><td>dailyBalance</td><td>當日盈虧金額</td><td>string</td></tr><tr><td>dailyBalancePercent</td><td>當日盈虧占比</td><td>string</td></tr><tr><td>enableAmount</td><td>可賣數量</td><td>number</td></tr><tr><td>exchangeType</td><td>交易類型</td><td>int32</td></tr><tr><td>frozenAmount</td><td>凍結數量</td><td>number</td></tr><tr><td>hisMarketValue</td><td>市值</td><td>string</td></tr><tr><td>holdingBalance</td><td>持倉盈虧金額</td><td>string</td></tr><tr><td>holdingBalancePercent</td><td>持倉盈虧占比</td><td>string</td></tr><tr><td>lastPrice</td><td>最新價</td><td>string</td></tr><tr><td>marketValue</td><td>市值</td><td>string</td></tr><tr><td>oddAmount</td><td>碎股數量</td><td>string</td></tr><tr><td>quoteType</td><td>行情許可權 0: 延時行情 1:bmp 行情 2:level1 行情 3:level2 行情</td><td>string</td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td></tr><tr><td>stockOnWayBalanceDTOList</td><td>在途資金列表</td><td>array</td></tr><tr><td>applyType</td><td>業務類型 IpoApplyTypeEnum</td><td>int32</td></tr><tr><td>applyTypeName</td><td>業務類型 IpoApplyTypeEnum</td><td>string</td></tr><tr><td>exchangeType</td><td>市場</td><td>int32</td></tr><tr><td>moneyType</td><td>幣種</td><td>int32</td></tr><tr><td>onWayBalance</td><td>在途現金</td><td>number</td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td></tr><tr><td>totalDailyBalance</td><td>今日盈虧金額</td><td>string</td></tr><tr><td>totalDailyBalancePercent</td><td>今日盈虧占比</td><td>string</td></tr><tr><td>totalHoldingBalance</td><td>持倉盈虧金額</td><td>string</td></tr><tr><td>totalHoldingBalancePercent</td><td>持倉盈虧占比</td><td>string</td></tr><tr><td>withdrawBalance</td><td>可取金額</td><td>string</td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td></tr></table>

回應示例

```json
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
```

"enableAmount": 0, 

```javascript
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
```


"stockOnWayBalanceDTOList": [


```json
{
    "applyType": 0,
    "applyTypeName": "",
    "exchangeType": 0,
    "moneyType": 0,
    "onWayBalance": 0,
    "stockCode": "", 
```

"stockName": "" 

```jsonl
},
"totalDailyBalance": "",
"totalDailyBalancePercent": "",
"totalHoldingBalance": "",
"totalHoldingBalancePercent": "",
"withdrawBalance": ""
}
],
"msg": ""
} 
```

# 2.14 查詢聚合資產資訊

介面位址 /aggregation-server/open-api/user-asset-aggregation/v1

請求方式 POST

consumes ["application/json"] produces 

["application/json"] 介 面 描 述 需 要

token 


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的requestId 資訊,確保唯一,防止重複提交實現介面幕等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>交易類別,0-港股,5-美股,67-A股</td><td>body</td><td>true</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiOTMyYmFjY2U3MGU3 

NDgwM2JmNjYxODk0OTM3ZDlkN2QiLCJzb3VyY2UiOiJ3ZWIiLCJ1dWlkIjozNDMwMjExNDU2ODI4NjIwODB 

9.XiF0eWAmeL-pthTg--5SLObnscJcDYHaJTJZTHAucwQ 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Channel：100082 

X-Request-Id: 928239187123721231232 

X-Sign：body 使用 RSA 私密金鑰加密


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>0</td><td>成功</td><td>ResponseVO</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«OpenHoldAsset»</td></tr><tr><td>108008</td><td>user 服務不可用</td><td></td></tr><tr><td>108011</td><td>使用者資訊查詢介面異常</td><td></td></tr><tr><td>108027</td><td>stock-order 服務不可用</td><td></td></tr><tr><td>108028</td><td>調用客戶股票資產查詢介面異常</td><td></td></tr><tr><td>108029</td><td>finance-server 服務不可用</td><td></td></tr><tr><td>108030</td><td>獲取當前客戶基金持倉清單介面異常</td><td></td></tr><tr><td>108031</td><td>獲取當前客戶債券持倉清單介面異常</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>Code</td><td>回應碼0-請求成功</td><td>int32</td><td></td></tr><tr><td>Data</td><td>回應體</td><td>object</td><td>OpenHoldAsset</td></tr><tr><td>asset</td><td>總資產</td><td>string</td><td></td></tr><tr><td>bondMarketValue</td><td>債券市值</td><td>string</td><td></td></tr><tr><td>enableBalance</td><td>可用金額</td><td>string</td><td></td></tr><tr><td>frozenBalance</td><td>凍結金額</td><td>string</td><td></td></tr><tr><td>fundMarketValue</td><td>基金市值</td><td>string</td><td></td></tr><tr><td>onWayBalance</td><td>在途資金</td><td>string</td><td></td></tr><tr><td>stockMarketValue</td><td>股票市值</td><td>string</td><td></td></tr><tr><td>withdrawBalance</td><td>可取金額</td><td>string</td><td></td></tr><tr><td>totalHoldingBalance</td><td>持倉盈虧金額</td><td>string</td><td></td></tr><tr><td>msg</td><td>回應內容</td><td>string</td><td></td></tr></table>

{ 

"code": 0, 

"msg": "請求成功",

"data": { 

"asset": "997457.66", 

```json
"stockMarketValue": "88165.000000",
"bondMarketValue": "0.00",
"fundMarketValue": "0.00",
"enableBalance": "908484.60",
"withdrawBalance": "908484.60",
"frozenBalance": "808.060000",
"onWayBalance": "0.00",
"totalHoldingBalance": "-2510.00"
} 
```

# 3 IPO

# 3.1 獲取 IPO 列表-分頁查詢

介面位址 /stock-order-server/open-api/ipo-list

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 獲取IPO清單（不需要登陸）


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>status</td><td>Tab 頁類別(0-認購中,1-待上市)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>pageNum</td><td>當前頁 1 開始,預設值 1</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>pageSize</td><td>每頁結果數,預設值 10</td><td>body</td><td>false</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求 body 示例

{ 

"pageNum": 1, 

"pageSize": 10, 

"status": 1 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«PageInfoVO«AppGetIpoListResponse»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>PageInfoVO«OpenApiGetIpoListResponse»</td><td>PageInfoVO«OpenApiGetIpoListRespe»</td></tr><tr><td>list</td><td>結果集合</td><td>array</td><td>OpenApiGetIpoList Response</td></tr><tr><td>bookingRatio</td><td>認購倍數</td><td>number</td><td></td></tr><tr><td>endTime</td><td>現金認購結束時間 yyyy-MM-dd HH:mm:ss</td><td>string</td><td></td></tr><tr><td>englishName</td><td>新股英文名</td><td>string</td><td></td></tr><tr><td>exchangeType</td><td>市場類型(0-港股)</td><td>int32</td><td></td></tr><tr><td>financingEndTime</td><td>融資認購結束時間</td><td>string</td><td></td></tr><tr><td>financingMultiple</td><td>融資倍數</td><td>int32</td><td></td></tr><tr><td>ipoId</td><td>IPO id</td><td>string</td><td></td></tr><tr><td>labelStatus</td><td>標籤狀態(0-已認購,1-已中簽,2-未中簽)</td><td>int32</td><td></td></tr><tr><td>latestEndtime</td><td>最晚認購截止時間(國際認購、融資認購和現金認購截止時間最晚的時間)</td><td>string</td><td></td></tr><tr><td>leastAmount</td><td>起購金額</td><td>number</td><td></td></tr><tr><td>listingPrice</td><td>最終上市價格</td><td>number</td><td></td></tr><tr><td>listingTime</td><td>上市交易時間</td><td>string</td><td></td></tr><tr><td>moneyType</td><td>幣種類型(0-人民幣,1-美元,2-港幣)</td><td>int32</td><td></td></tr><tr><td>priceMax</td><td>最高招股價</td><td>number</td><td></td></tr><tr><td>priceMin</td><td>最低招股價</td><td>number</td><td></td></tr><tr><td>publishTime</td><td>公佈中簽日期</td><td>string</td><td></td></tr><tr><td>remainingTime</td><td>認購剩餘時間(秒)</td><td>int64</td><td></td></tr><tr><td>serverTime</td><td>伺服器時間</td><td>string</td><td></td></tr><tr><td>status</td><td>新股狀態(0-待認購,1-認購中,2-待扣款,3-已扣款待確認,4-已確認待公佈,5-已公佈待上市,6-已上市,7-取消上市,8-暫緩上市,9-延遲上市)</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>狀態中文名</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>新股代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>新股名稱</td><td>string</td><td></td></tr><tr><td>subscribeWay</td><td>認購方式,多種認購用,隔開,比如0,1支持現金和融資(1-公開現金認購,2-公開融資認購,3-國際配售)-這個欄位可以判斷是否支援融資認購</td><td>string</td><td></td></tr><tr><td>successRate</td><td>中簽率</td><td>number</td><td></td></tr><tr><td>pageNum</td><td>當前頁</td><td>int32</td><td></td></tr><tr><td>pageSize</td><td>每頁條數</td><td>int32</td><td></td></tr><tr><td>total</td><td>總數</td><td>int64</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td></td><td></td></tr></table>

# 回應示例

{ 

```txt
"code": 0,
"msg": "操作成功",
"data": {
    "pageNum": 1,
    "pageSize": 20,
    "total": 2,
    "list": [ {
```

```javascript
"ipoId": "1143834475048767488",
"stockCode": "02099",
"exchangeType": 0,
"status": 1, "statusName": "認購中",
"stockName": "中國黃金國際",
"englishName": "CHINAGOLDINTL",
"leastAmount": null, "priceMin": 7,
"priceMax": 11,
"listingPrice": 10,
"endTime": "2019-06-27",
"financingEndTime": null, "latestEndtime": "2019-06-27",
"remainingTime": -1, "labelStatus": null, "successRate": null,
"bookingRatio": null, "publishTime": "2019-07-01",
"listingTime": "2019-07-02",
"moneyType": 2,
```

```txt
"serverTime": "2019-10-09 21:08:21",
"subscribeWay": "1",
"financingMultiple": 3
},
{
    "ipolId": "1133576191818039296",
    "stockCode": "00994",
    "exchangeType": 0,
    "status": 1, "statusName": "認購中",
    "stockName": "中天宏信",
    "englishName": "CT VISION",
    "leastAmount": null, "priceMin": 7,
    "priceMax": 10,
    "listingPrice": 9,
    "endTime": "2019-07-29",
    "financingEndTime": null, "latestEndtime": "2019-07-29",
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
```

# 3.2 獲取新股詳細資訊

介面位址 /stock-order-server/open-api/ipo-info

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 獲取新股詳細資訊


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道 ID,由盈立分配</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>exchangeType</td><td>市場類型(0-HK,5-US),如果 ipoId 不傳,該欄位必傳</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>ipoId</td><td>新股 id [ 與(stockCode&amp;exchangeType 不能同時為空 )],當 ipoId 有值,優先取 ipoId 查詢,stockCode&amp;exchangeType 條件不生效</td><td>body</td><td>false</td><td>int64</td></tr><tr><td>stockCode</td><td>股票代碼,如果 ipoId 不傳,該欄位必傳</td><td>body</td><td>false</td><td>string</td></tr></table>


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«appIpoInfoResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohaib0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFID
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例

```json
{
    "ipoId": 1133576191528632320
} 
```

# 回應參數

<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>appIpoInfoResponse</td><td>appIpoInfoResponse</td></tr><tr><td>applied</td><td>用戶是否已認購</td><td>boolean</td><td></td></tr><tr><td>beginTime</td><td>現金認購開始時間</td><td>string</td><td></td></tr><tr><td>bookingFee</td><td>現金認購手續費</td><td>number</td><td></td></tr><tr><td>bookingRatio</td><td>認購倍數</td><td>number</td><td></td></tr><tr><td>compFinancingSurplus</td><td>公司融資額度淨餘</td><td>number</td><td></td></tr><tr><td>depositRate</td><td>融資比例</td><td>number</td><td></td></tr><tr><td>ecmEndTime</td><td>國際認購截止時間</td><td>date-time</td><td></td></tr><tr><td>ecmStatus</td><td>ecm 新股狀態(0-待認購,1-認購中,2-待扣款,3-待扣款[未全部扣款成功],4-待提交,5-待分配,6-待返款,7-待返款[未全部返款成功],8-待返券,9-待返券[未全部返券成功],10-待 CCASS 確認,11-待上市,12-已上市,13-暫停認購)</td><td>int32</td><td></td></tr><tr><td>endTime</td><td>現金認購結束時間</td><td>string</td><td></td></tr><tr><td>englishName</td><td>新股英文名</td><td>string</td><td></td></tr><tr><td>exchangeType</td><td>交易類別(0-HK,5-US)</td><td>int32</td><td></td></tr><tr><td>exchangeTypeName</td><td>交易類別名稱</td><td>string</td><td></td></tr><tr><td>financingEndTime</td><td>融資認購截止時間</td><td>date-time</td><td></td></tr><tr><td>financingFee</td><td>融資手續費</td><td>number</td><td></td></tr><tr><td>financingMultiple</td><td>融資倍數</td><td>int32</td><td></td></tr><tr><td>financingTips</td><td>融資認購溫馨提示</td><td>string</td><td></td></tr><tr><td>greyFlag</td><td>是否支持暗盤(0-不支持,1-支持)</td><td>int32</td><td></td></tr><tr><td>greyTimeBegin</td><td>暗盤交易時間段開始,格式 HH:mm:ss</td><td>string</td><td></td></tr><tr><td>greyTimeEnd</td><td>暗盤交易時間段結束,格式 HH:mm:ss</td><td>string</td><td></td></tr><tr><td>greyTradeDate</td><td>暗盤交易日,格式 yyyy-MM-dd</td><td>string</td><td></td></tr><tr><td>handAmount</td><td>每手股數</td><td>number</td><td></td></tr><tr><td>interestBeginDate</td><td>融資認購/計息開始時間</td><td>date-time</td><td></td></tr><tr><td>interestDay</td><td>計息天數</td><td>int32</td><td></td></tr><tr><td>interestEndDate</td><td>融資計息結束時間</td><td>date-time</td><td></td></tr><tr><td>interestRate</td><td>默認融資利率</td><td>number</td><td></td></tr><tr><td>ipoFinancingRatios</td><td>融資階梯利率 (json 陣列 :[{"financing_amount_begin": 初始認購金額,"financing_amount_end": 結束認購金額,"interest_rate": 利率,"exchange_type": 市場類型,"stock_code":"新股代碼"}])</td><td>array</td><td>IpoFinancingRatio</td></tr><tr><td>exchange_type</td><td>市場類型</td><td>int32</td><td></td></tr><tr><td>financing_amount_begin</td><td>初始認購金額</td><td>number</td><td></td></tr><tr><td>financing_amount_end</td><td>結束認購金額</td><td>number</td><td></td></tr><tr><td>interest_rate</td><td>利率</td><td>number</td><td></td></tr><tr><td>stock_code</td><td>新股代碼</td><td>string</td><td></td></tr><tr><td>ipoId</td><td>IPO id</td><td>string</td><td></td></tr><tr><td>latestEndtime</td><td>最晚認購截止時間(國際認購、融資認購和現金認購截止時間最晚的時間)</td><td>string</td><td></td></tr><tr><td>leastAmount</td><td>起購金額(一手認購金額)</td><td>number</td><td></td></tr><tr><td>listingPrice</td><td>最終上市價格</td><td>number</td><td></td></tr><tr><td>listingTime</td><td>上市交易時間</td><td>string</td><td></td></tr><tr><td>marketValueMax</td><td>市值最大值</td><td>number</td><td></td></tr><tr><td>marketValueMin</td><td>市值最小值</td><td>number</td><td></td></tr><tr><td>moneyType</td><td>幣種類型(0-人民幣,1-美元,2-港幣)</td><td>int32</td><td></td></tr><tr><td>officialBegin</td><td>官方招股開始時間</td><td>string</td><td></td></tr><tr><td>officialEnd</td><td>官方招股結束時間</td><td>string</td><td></td></tr><tr><td>priceMax</td><td>最高招股價</td><td>number</td><td></td></tr><tr><td>priceMin</td><td>最低招股價</td><td>number</td><td></td></tr><tr><td>prospectusLink</td><td>招股書連結</td><td>string</td><td></td></tr><tr><td>publishQuantity</td><td>發行股本</td><td>number</td><td></td></tr><tr><td>publishTime</td><td>公佈中簽日期</td><td>string</td><td></td></tr><tr><td>qtyAndCharges</td><td>檔位元資訊(json 陣列:["allotted_amount": 中簽金額,"applied_amount": 申購金額,"exchange_type": 市場類型,"shared_applied":申購數量,"stock_code":"新</td><td>array</td><td>IpoQtyAndCharges</td></tr><tr><td></td><td>股代碼", "leastCash": 檔位對應的最少使用現金])</td><td></td><td></td></tr><tr><td>allotted_amount</td><td>中簽金額</td><td>number</td><td></td></tr><tr><td>applied_amount</td><td>申購金額</td><td>number</td><td></td></tr><tr><td>exchange_type</td><td>市場類型</td><td>int32</td><td></td></tr><tr><td>leastCash</td><td>檔位對應的最少使用現金</td><td>int32</td><td></td></tr><tr><td>shared_applied</td><td>申購數量</td><td>number</td><td></td></tr><tr><td>stock_code</td><td>新股代碼</td><td>string</td><td></td></tr><tr><td>remainingTime</td><td>認購剩餘時間 (秒)</td><td>int64</td><td></td></tr><tr><td>serverTime</td><td>伺服器時間</td><td>string</td><td></td></tr><tr><td>sponsor</td><td>保薦人</td><td>string</td><td></td></tr><tr><td>status</td><td>新股狀態(0-待認購, 1-認購中, 2-待扣款, 3-已扣款待確認, 4-已確認待公佈, 5-已公佈待上市, 6-已上市, 7-取消上市, 8-暫緩上市, 9-延遲上市)</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>狀態中文名</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>新股代碼</td><td>string</td><td></td></tr><tr><td>stockIntroduction</td><td>股票介紹</td><td>string</td><td></td></tr><tr><td>stockName</td><td>新股名稱</td><td>string</td><td></td></tr><tr><td>subscribeWay</td><td>認購方式, 多種認購用, 隔開, 比如 1,2 支持現金和融資(1-公開現金認購, 2-公開融資認購, 3-國際配售)-這個欄位可以判斷是否支援融資認購</td><td>string</td><td></td></tr><tr><td>successRate</td><td>中簽率</td><td>number</td><td></td></tr><tr><td>tips</td><td>現金認購溫馨提示</td><td>string</td><td></td></tr><tr><td>totalQuantity</td><td>總股本</td><td>number</td><td></td></tr><tr><td>updateTime</td><td>更新時間</td><td>string</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

"code": 0, 

"msg": "操作成功",

"data": { 

```csv
"ipoId": "1143834475048767488",
"stockCode": "02099", "stockName": "中國黃金國際", "status": 1,
"exchangeType": 0,
"moneyType": 2,
"handAmount": null,
"bookingFee": 10,
"beginTime": "2019-06-25 09:00:00",
"endTime": "2019-06-27 12:00:00",
"publishTime": "2019-07-01 00:00:00",
"listingTime": "2019-07-02 00:00:00",
"listingPrice": null, "priceMin": null,
"priceMax": 11, "financingEndTime": null, "interestBeginDate": null,
"interestEndDate": null,
"officialBegin": "2019-06-25 09:00:00",
"officialEnd": "2019-06-28 12:00:00",
"leastAmount": null, "successRate": null, "bookingRatio": null, "sponsor": "",
"publishQuantity": null,
"totalQuantity": null,
"marketValueMin": null,
"marketValueMax": null,
"prospectusLink": "Http://",
"qtyAndCharges": [
{
    "stock_code": "2099",
    "exchange_type": 0,
    "shared_applied": 100,
    "applied_amount": 1111.09,
    "allotted_amount": 0
},
"ipoFinancingRatios": [
{
    "stock_code": "2099",
    "exchange_type": 0,
    "financing_amount_begin": 1000,
    "financing_amount_end": 10000,
    "interest_rate": 0.5
},
{
```

```jsonl
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
```

# 3.3ipo 新股認購

介面位址 /stock-order-server/open-api/apply-ipo

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 ipo新股認購


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Dt</td><td>設備類型(t1-android,t2-ios,t3-其他,t4-Windows,t5-Mac)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>applyQuantity</td><td>認購數量</td><td>body</td><td>true</td><td>number</td></tr><tr><td>applyType</td><td>認購類型(1-現金,2-融資)</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>ipoId</td><td>ipo交易系統唯一編號</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>serialNo</td><td>流水號,最長19位,確保唯一推薦雪花演算法生成</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>cash</td><td>認購現金(融資認購時必填)</td><td>body</td><td>false</td><td>number</td></tr></table>

# 請求 header 示例

```yaml
Authorization:eyJ0eXAiOiJKV1Qi LCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZ iNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj B9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Dt: 1
X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密' ;
```

# 請求 body 示例

```json
{
    "applyQuantity": 100,
    "applyType": 1,
    "cash": 0,
    "ipoId": 1133576191818039296,
    "serialNo": 1182189250463484234
} 
```

# 回應狀態

<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«IpoApplyResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>IpoApplyResponse</td><td>IpoApplyResponse</td></tr><tr><td>applyId</td><td>申購 id</td><td>string</td><td></td></tr><tr><td>status</td><td>申購狀態(0-已提交,1-已認購,2-等待改單,3-等待撤銷,4-已撤銷,5-已扣款,6-待公佈中簽,7-全部中簽,8-部分中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "applyId": "1182192040986583040",
    "status": 1
    }
}
```

# 3.4ipo 改單/撤單

介面位址 /stock-order-server/open-api/modify-ipo

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 ipo改單/撤單


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Request-Id</td><td>頭部資訊的 requestId 資訊,確保唯一,防止重複提交實現介面幂等</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>actionType</td><td>操作類型 0-改單,1-撤單</td><td>body</td><td>true</td><td>int32</td></tr><tr><td>applyId</td><td>認購記錄 Id</td><td>body</td><td>true</td><td>int64</td></tr><tr><td>applyQuantity</td><td>認購數量</td><td>body</td><td>true</td><td>number</td></tr><tr><td>cash</td><td>認購現金(改融資認購單,必填)</td><td>body</td><td>false</td><td>number</td></tr></table>

# 請求 header 示例

```txt
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi
NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj
B 9.cvuohaib0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD
Content-Type: application/json;charset=UTF-8 X-Lang: 1
X-Request-Id: 928239187123721231232
X-Type: 1
X-Channel : 100082
X-Sign : body 使用 RSA 私密金鑰加密
```

# 請求 body 示例

```json
{
    "actionType": 1,
    "applyId": 1182192040986583040,
    "applyQuantity": 0,
    "cash": 0
} 
```


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«IpoApplyResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>IpoApplyResponse</td><td>IpoApplyResponse</td></tr><tr><td>applyId</td><td>申購 id</td><td>string</td><td></td></tr><tr><td>status</td><td>申購狀態(0-已提交,1-已認購,2-等待改單,3-等待撤銷,4-已撤銷,5-已扣款,6-待公佈中簽,7-全部中簽,8-部分中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

```json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
    "applyId": "1182192040986583040",
    "status": 4
    }
}
```

# 3.5 獲取客戶 ipo 申購清單-分頁查詢

介面位址 /stock-order-server/open-api/ipo-record-list

請求方式 POST

consumes ["application/json"] 

produces ["*/*"] 

介面描述 獲取客戶ipo申購清單


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>applyTimeMin</td><td>認購開始時間,格式:yyyy-MM-dd HH:mm:ss</td><td>body</td><td>false</td><td>string</td></tr><tr><td>applyTimeMax</td><td>認購結束時間,格式:yyyy-MM-dd HH:mm:ss</td><td>body</td><td>false</td><td>string</td></tr><tr><td>pageNum</td><td>當前頁 1 開始,預設值 1</td><td>body</td><td>false</td><td>int32</td></tr><tr><td>pageSize</td><td>每頁結果數,預設值 10</td><td>body</td><td>false</td><td>int32</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求示例

{ 

"pageNum": 1, 

"pageSize": 10, 

"applyTimeMin":"2019-10-12 00:00:00", 

"applyTimeMax":"2020-01-30 00:00:00" 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«PageInfoVO«IpoRecordListResponse»»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>PageInfoVO«IpoRecordListResponse»</td><td>PageInfoVO«IpoRecordListResponse»</td></tr><tr><td>list</td><td>結果集合</td><td>array</td><td>IpoRecordListResponse</td></tr><tr><td>allottedQuantity</td><td>中簽股數</td><td>number</td><td></td></tr><tr><td>applyAmount</td><td>認購總金額(包含手續費,不包含利息)</td><td>number</td><td></td></tr><tr><td>applyId</td><td>申請編號</td><td>string</td><td></td></tr><tr><td>applyQuantity</td><td>認購股數</td><td>number</td><td></td></tr><tr><td>applyType</td><td>認購類型(1-現金,2-融資)</td><td>int32</td><td></td></tr><tr><td>applyTypeName</td><td>認購類型(1-現金認購,2-融資認購)</td><td>string</td><td></td></tr><tr><td>priceMax</td><td>最高招股價</td><td>number</td><td></td></tr><tr><td>priceMin</td><td>最低招股價</td><td>number</td><td></td></tr><tr><td>listingPrice</td><td>最終上市價格</td><td>number</td><td></td></tr><tr><td>cash</td><td>認購現金</td><td>number</td><td></td></tr><tr><td>exchangeType</td><td>市場類型(0-HK,5-US)</td><td>int32</td><td></td></tr><tr><td>financingAmount</td><td>融資利息</td><td>number</td><td></td></tr><tr><td>financingBalance</td><td>融資金額</td><td>number</td><td></td></tr><tr><td>interestRate</td><td>融資利率</td><td>number</td><td></td></tr><tr><td>labelCode</td><td>狀態標籤碼(0-待系統確認,1-已認購,4-已撤銷,6-待公佈中簽,7-已中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>moneyType</td><td>幣種類型(0-人民幣,1-美元,2-港幣)</td><td>int32</td><td></td></tr><tr><td>publishTime</td><td>公佈中簽日期</td><td>string</td><td></td></tr><tr><td>listingTime</td><td>上市交易時間(YYYY-MM-DD)</td><td></td><td></td></tr><tr><td>serverTime</td><td>伺服器時間</td><td>string</td><td></td></tr><tr><td>status</td><td>認購狀態(0-已提交,1-已認購,2-等待改單,3-等待撤銷,4-已撤銷,5-已扣款,6-待公佈中簽,7-全部中簽,8-部分中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>認購狀態名稱</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>pageNum</td><td>當前頁</td><td>int32</td><td></td></tr><tr><td>pageSize</td><td>每頁條數</td><td>int32</td><td></td></tr><tr><td>total</td><td>總數</td><td>int64</td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

```txt
"code": 0,
"msg": "操作成功",
"data": {
    "pageNum": 1,
    "pageSize": 0,
    "total": 34,
    "list": [ {
```

```javascript
"applyId": "1147036407112679424",
"applyType": 2, "applyTypeName": "融資認購", "stockName": "香港中華煤氣", "stockCode": "00003",
"exchangeType": 0,
"status": 10, "statusName": "認購失敗", "applyQuantity": 200,
"applyAmount": 4140.31, "cash": null,
"financingBalance": null, "interestRate": null, "priceMin": 10,
"priceMax": 20,
"listingPrice": 13,
"financingAmount": 1.75,
```

```json
"allottedQuantity": 0,
"publishTime": "2019-07-05 00:00:00",
"serverTime": null, "moneyType": 2,
"labelCode": 10
},
{
"applyId": "1147018860570537984",
"applyType": 2, "applyTypeName": "融資認購", "stockName": "香港中華煤氣", "stockCode": "00003",
"exchangeType": 0,
"status": 4, "statusName": "已撤銷", "applyQuantity": 200,
"applyAmount": 4140.31, "cash": null,
"financingBalance": null, "interestRate": null, "priceMin": 10,
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
```

# 3.6 獲取客戶 ipo 申購明細

介面位址 /stock-order-server/open-api/ipo-record

請求方式 POST

consumes ["application/json"] 

# 介面描述 獲取客戶ipo申購明細


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr><tr><td>applyId</td><td>申購編號(傳其中一個即可)</td><td>body</td><td>false</td><td>int64</td></tr><tr><td>serialNo</td><td>流水號(傳其中一個即可)</td><td>body</td><td>false</td><td>int64</td></tr></table>

# 請求 header 示例

Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZi 

NDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNj 

B 9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD 

Content-Type: application/json;charset=UTF-8 X-Lang: 1 

X-Type: 1 

X-Channel：100082 

X-Sign：body 使用 RSA 私密金鑰加密

# 請求示例

{ 

"applyId": 1147036407112679424, 

"serialNo": 1233123554314 

} 


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>ResponseVO«IpoRecordResponse»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td><td>schema</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td><td></td></tr><tr><td>data</td><td>返回體</td><td>IpoRecordResponse</td><td>IpoRecordResponse</td></tr><tr><td>allottedQuantity</td><td>中簽股數</td><td>number</td><td></td></tr><tr><td>applyAmount</td><td>認購總金額(包含手續費,不包含利息)</td><td>number</td><td></td></tr><tr><td>applyId</td><td>申請編號</td><td>string</td><td></td></tr><tr><td>applyQuantity</td><td>認購股數</td><td>number</td><td></td></tr><tr><td>applyType</td><td>認購類型(1-現金,2-融資)</td><td>int32</td><td></td></tr><tr><td>applyTypeName</td><td>認購類型(1-現金認購,2-融資認購)</td><td>string</td><td></td></tr><tr><td>cash</td><td>認購現金</td><td>number</td><td></td></tr><tr><td>channel</td><td>管道類型(1-APP提交,2-中台提交,99-其它)</td><td>int32</td><td></td></tr><tr><td>createTime</td><td>認購提交時間</td><td>string</td><td></td></tr><tr><td>deductStatus</td><td>扣款狀態(0-已凍結,1-已扣款,2-已解凍)</td><td>int32</td><td></td></tr><tr><td>deductStatusName</td><td>扣款狀態名</td><td>string</td><td></td></tr><tr><td>endTime</td><td>當前認購方式截止時間</td><td>string</td><td></td></tr><tr><td>exchangeType</td><td>市場類型(0-HK,5-US)</td><td>int32</td><td></td></tr><tr><td>failReason</td><td>認購失敗原因</td><td>string</td><td></td></tr><tr><td>financingAmount</td><td>融資利息</td><td>number</td><td></td></tr><tr><td>financingBalance</td><td>融資金額</td><td>number</td><td></td></tr><tr><td>handlingFee</td><td>手續費</td><td>number</td><td></td></tr><tr><td>interestDay</td><td>計息天數</td><td>int32</td><td></td></tr><tr><td>interestRate</td><td>融資利率</td><td>number</td><td></td></tr><tr><td>ipoId</td><td>ipo 編號</td><td>string</td><td></td></tr><tr><td>ipoStatus</td><td>新股狀態(0-待認購,1-認購中,2-待扣款,3-已扣款待確認,4-已確認待公佈,5-已公佈待上市,6-已上市,7-取消上市,8-暫緩上市,9-延遲上市)</td><td>int32</td><td></td></tr><tr><td>labelCode</td><td>狀態標籤碼(0-待系統確認,1-已認購,4-已撤銷,6-待公佈中簽,7-已中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>moneyType</td><td>幣種類型(0-人民幣,1-美元,2-港幣)</td><td>int32</td><td></td></tr><tr><td>publishTime</td><td>公佈中簽日期 yyyy-MM-dd HH:mm:ss</td><td>string</td><td></td></tr><tr><td>refundAmount</td><td>退款金額</td><td>number</td><td></td></tr><tr><td>refundFlag</td><td>退款狀態(0-無退款,1-待退款,2-已退款)</td><td>int32</td><td></td></tr><tr><td>serverTime</td><td>伺服器時間</td><td>string</td><td></td></tr><tr><td>status</td><td>認購狀態(0-已提交,1-已認購,2-等待改單,3-等待撤銷,4-已撤銷,5-已扣款,6-待公佈中簽,7-全部中簽,8-部分中簽,9-未中簽,10-認購失敗)</td><td>int32</td><td></td></tr><tr><td>statusName</td><td>認購狀態名稱</td><td>string</td><td></td></tr><tr><td>stockCode</td><td>股票代碼</td><td>string</td><td></td></tr><tr><td>stockName</td><td>股票名稱</td><td>string</td><td></td></tr><tr><td>listingTime</td><td>上市時間 yyyy-MM-dd</td><td></td><td></td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td><td></td></tr></table>

# 回應示例

{ 

```javascript
"code": 0,
"msg": "操作成功",
"data": {
    "applyId": "1178190341147189248",
    "applyType": 1, "applyTypeName": "現金認購", "stockName": "新城市建設發展", "stockCode": "00456",
    "exchangeType": 0,
    "status": 4, "statusName": "已撤銷",
    "applyQuantity": 1900.00,
    "applyAmount": 34544.6300, "cash": null,
    "financingBalance": null, "interestRate": null, "financingAmount": 0.0000,
    "allottedQuantity": null,
    "publishTime": "2019-10-03 00:00:00",
```

```javascript
"serverTime": "2019-11-01 20:33:55",
"moneyType": 2,
 BelgiumCode": 4,
 "createTime": "2019-09-29 14:10:42",
 "deductStatus": 2, "deductStatusName": "已解凍", "refundFlag": 0,
 "refundAmount": null, "handlingFee": 0.0000, "failReason": null,
 "endTime": "2019-09-30 11:18:00",
 "ipoId": "1178148950262435840",
 "interestDay": 0,
 "channel": 1,
 "listingTime": "2019-10-04",
 "ipoStatus": 6
 }
```

# 4 資金

# 4.1 查詢匯率

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


請求參數


<table><tr><td>參數名稱</td><td>說明</td><td>請求類型</td><td>必填</td><td>類型</td></tr><tr><td>Authorization</td><td>頭部資訊的 token 資訊</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Lang</td><td>語言類別(1-簡體,2-繁體,3-English)</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Time</td><td>時間標記</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Sign</td><td>RSA 簽名</td><td>header</td><td>true</td><td>string</td></tr><tr><td>X-Channel</td><td>管道</td><td>header</td><td>true</td><td>string</td></tr></table>


回應狀態


<table><tr><td>狀態碼</td><td>說明</td><td>schema</td></tr><tr><td>200</td><td>OK</td><td>CapitalResponseVO«FetchExchangeRateResp»</td></tr><tr><td>201</td><td>Created</td><td></td></tr><tr><td>401</td><td>Unauthorized</td><td></td></tr><tr><td>403</td><td>Forbidden</td><td></td></tr><tr><td>404</td><td>Not Found</td><td></td></tr></table>


回應參數


<table><tr><td>參數名稱</td><td>說明</td><td>類型</td></tr><tr><td>code</td><td>狀態碼</td><td>int32</td></tr><tr><td>data</td><td>返回體</td><td>array</td></tr><tr><td>baseMoneyType</td><td>基準幣種,0:人民幣1:美元2:港幣</td><td>int32</td></tr><tr><td>sourceCurrency</td><td>源幣種,0:人民幣1:美元2:港幣</td><td>int32</td></tr><tr><td>targetCurrency</td><td>目標幣,0:人民幣1:美元2:港幣</td><td>int32</td></tr><tr><td>yxBuyRate</td><td>盈立買入匯率</td><td>number</td></tr><tr><td>yxSellRate</td><td>盈立賣出匯率</td><td>number</td></tr><tr><td>bocSellRate</td><td>中銀賣出匯率</td><td>number</td></tr><tr><td>bocBuyRate</td><td>中銀買入匯率</td><td>number</td></tr><tr><td>msg</td><td>狀態資訊</td><td>string</td></tr></table>

# 回應示例

{ 

"code": 0, 

"msg": "操作成功",

```txt
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
] 
```

# 5 資料字典

# 5.1 訂單狀態（Status）

<table><tr><td>編碼</td><td>名稱</td></tr><tr><td>-1</td><td>失敗</td></tr><tr><td>0</td><td>全部成交</td></tr><tr><td>1</td><td>等待提交</td></tr><tr><td>2</td><td>待成交</td></tr><tr><td>3</td><td>部分成交</td></tr><tr><td>4</td><td>等待撤單</td></tr><tr><td>5</td><td>等待改單</td></tr><tr><td>6</td><td>已撤單</td></tr><tr><td>7</td><td>部成撤單</td></tr><tr><td>8</td><td>廢單</td></tr></table>

# 5.2 市場類型（ExchangeType）

<table><tr><td>編碼</td><td>名稱</td></tr><tr><td>0</td><td>港股</td></tr><tr><td>1</td><td>上海 A</td></tr><tr><td>2</td><td>上海 B</td></tr><tr><td>3</td><td>深圳 A</td></tr><tr><td>4</td><td>深圳 B</td></tr><tr><td>5</td><td>美股</td></tr><tr><td>6</td><td>滬港通</td></tr><tr><td>7</td><td>深港通</td></tr><tr><td>67</td><td>A 股(用於查詢)</td></tr><tr><td>100</td><td>所有市場(用於查詢)</td></tr></table>

# 5.3IPO 狀態（Status）

<table><tr><td>編碼</td><td>名稱</td></tr><tr><td>0</td><td>待認購</td></tr><tr><td>1</td><td>認購中</td></tr><tr><td>2</td><td>待扣款</td></tr><tr><td>3</td><td>已扣款待確認</td></tr><tr><td>4</td><td>已確認待公佈</td></tr><tr><td>5</td><td>已公佈待上市</td></tr><tr><td>6</td><td>已上市</td></tr><tr><td>7</td><td>取消上市</td></tr><tr><td>8</td><td>暫緩上市</td></tr><tr><td>9</td><td>延遲上市</td></tr><tr><td>11</td><td>已刪除</td></tr></table>

# 5.4 幣種（moneyType）

<table><tr><td>編碼</td><td>名稱</td></tr><tr><td>0</td><td>人民幣</td></tr><tr><td>1</td><td>美元</td></tr><tr><td>2</td><td>港幣</td></tr></table>

# 5.5 設備類別（X-Dt）

<table><tr><td>編碼</td><td>名稱</td></tr><tr><td>t1</td><td>安卓</td></tr><tr><td>t2</td><td>Ios</td></tr><tr><td>t3</td><td>其它</td></tr><tr><td>t4</td><td>Windows</td></tr><tr><td>t5</td><td>Mac</td></tr></table>