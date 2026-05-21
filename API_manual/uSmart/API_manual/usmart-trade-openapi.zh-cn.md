# uSmart 账户交易开放 API

> Source URL: https://api-doc.usmart8.com/zh-cn/trade.html
>
> Fetched: 2026-05-21
>
> Truth source: uSmart official web documentation. Do not replace facts in this file with deleted PDF/MinerU output unless a newer official source is provided.

<div class="theme-default-content content__default">

# 交易OPEN API接口

\[toc\]

## 版本记录

| 日期       | 版本号 | 修改说明                                                                                                                                                                                                                                                                                                                                                          |
|------------|--------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2020-05-06 | 1.1    | 1、 添加获取融资股数接口(trade-margin-quantity)2、 查询资产接口(stock-asset)添加marginpurchasePower，mortgageMarketValue，debitBalance，anticipatedInterest，riskStatusCode，riskStatusName，mv，pv，creditAmount字段3、 最大可买、可卖数量接口(trade-quantity)添加cashEnableAmountcashEnableIntAmount，cashPurchasingPowermaxPurchasingPower，fundAccoutType字段 |
| 2020-05-08 | 1.2    | 1、 查询资产接口(stock-asset)添加追缴保证金字段。2、 添加margin-detail获取客户融资账户详情接口                                                                                                                                                                                                                                                                    |
| 2020-05-09 | 1.3    | 1、新增根据市场查找账户类型接口                                                                                                                                                                                                                                                                                                                                   |
| 2020-05-09 | 1.4    | 1、 删除4.2客户资金流水接口2、 添加4.2获取历史记录接口3、 添加4.3客户出金撤销接口                                                                                                                                                                                                                                                                                 |
| 2020-05-12 | 1.5    | 1、 4.11 stock-holding添加盈亏字段返回2、 4.12 stock-asset添加盈亏字段返回3、 4.13 stock-asset添加盈亏字段返回                                                                                                                                                                                                                                                    |
| 2020-05-20 | 1.6    | 1、1.13获取email验证码2、1.14机构用户邮箱验证码登录                                                                                                                                                                                                                                                                                                               |
| 2020-06-09 | 1.7    | 1、1.15机构用户邮箱激活                                                                                                                                                                                                                                                                                                                                           |
| 2020-06-10 | 1.8    | 1、1.16 机构用户邮箱校验2、1.17 机构用户邮箱校验                                                                                                                                                                                                                                                                                                                  |
| 2020-06-24 | 1.9    | 1、新增1.13\~1.21机构户登录接口                                                                                                                                                                                                                                                                                                                                   |
| 2020-07-01 | 1.10   | 1、添加3.7额度不足时确认现金认购数量接口                                                                                                                                                                                                                                                                                                                          |
| 2020-07-06 | 1.11   | 1、删除机构户登录接口，以单独文档的形式提供                                                                                                                                                                                                                                                                                                                       |
| 2020-08-04 | 1.12   | 1、2.15补充出参，2.1补充下单市场区分，添加IPO新股状态                                                                                                                                                                                                                                                                                                             |
| 2020-09-21 | 1.13   | 1、2.16添加持仓盈亏                                                                                                                                                                                                                                                                                                                                               |
| 2020-10-21 | 1.14   | 1、无                                                                                                                                                                                                                                                                                                                                                             |
| 2020-10-27 | 1.14   | 1、增加孖展部分获取股票抵押比率接口                                                                                                                                                                                                                                                                                                                               |
| 2021-02-25 | 1.15   | 1、新增资金账号查询融资利率接口                                                                                                                                                                                                                                                                                                                                   |
| 2023-07-19 | 1.16   | 1、密码登录、验证码登录接口支持邮箱账号类型（仅限官网申请渠道）                                                                                                                                                                                                                                                                                                   |
| 2025-06-10 | 1.17   | 1、新增7.1 MA-下单接口。2、新增7.2 MA-撤单接口。3、新增7.3 MA-订单列表接口。4、新增7.4 MA-订单详情接口。5、新增7.5 MA-获取购买力接口。                                                                                                                                                                                                                            |
| 2025-08-25 | 1.18   | 1、新增8.1 期权-下单接口。2、新增8.2 期权-改单接口。3、新增 期权-8.3撤单接口。4、新增8.4 期权-获取下单购买力接口。5、新增8.5 期权-获取改单购买力接口。6、新增8.6 期权-改单状态查询接口。7、新增8.7 期权-今日订单列表接口。8、新增8.8 期权-订单详情接口。                                                                                                          |

## 概述

-   开放平台可以为个人开发者和机构客户提供接口服务，投资者可以充分的利用盈立智投的交易服务、行情服务、账户服务等实现自己的投资应用。

-   协议：

HTTPS

-   X-Sign

使用MD5withRSA加密算法对Body中的内容进行加密，得到的密文经过safeBase64编码后做为X-Sign的值放入header当中，每一个渠道单独分配公私钥。

-   验签测试公钥为：

需双方商定

-   隐私数据加密测试公钥为：

需双方商定

-   URLSAFE\_BASE64算法在RFC4648中有定义

最终串会使用RSA私钥进行加密，之后使用RFC4648算法编码放入请求体或表单项中。

-   请求头X-Request-Id:

长度为19位数字，必须确保唯一用于做幂等防重，推荐使用[分布式Snowflake雪花算法<img src="data:image/svg+xml;base64,PHN2ZyBhcmlhLWhpZGRlbj0idHJ1ZSIgY2xhc3M9Imljb24gb3V0Ym91bmQiIGZvY3VzYWJsZT0iZmFsc2UiIGhlaWdodD0iMTUiIHZpZXdib3g9IjAgMCAxMDAgMTAwIiB3aWR0aD0iMTUiIHg9IjBweCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIiB5PSIwcHgiPjxwYXRoIGQ9Ik0xOC44LDg1LjFoNTZsMCwwYzIuMiwwLDQtMS44LDQtNHYtMzJoLTh2MjhoLTQ4di00OGgyOHYtOGgtMzJsMCwwYy0yLjIsMC00LDEuOC00LDR2NTZDMTQuOCw4My4zLDE2LjYsODUuMSwxOC44LDg1LjF6IiBmaWxsPSJjdXJyZW50Q29sb3IiPjwvcGF0aD4gPHBvbHlnb24gZmlsbD0iY3VycmVudENvbG9yIiBwb2ludHM9IjQ1LjcsNDguNyA1MS4zLDU0LjMgNzcuMiwyOC41IDc3LjIsMzcuMiA4NS4yLDM3LjIgODUuMiwxNC45IDYyLjgsMTQuOSA2Mi44LDIyLjkgNzEuNSwyMi45Ij48L3BvbHlnb24+PC9zdmc+" class="icon outbound" /> <span class="sr-only">(opens new window)</span>](https://www.cnblogs.com/yanduanduan/p/10038345.html)生成。

-   请求示例：

http header参数示例

<div class="language-java extra-class">

``` language-java
Authorization: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiNGZjYTA1MWNmZjQwNDI4NzlkNGJiYzYzYjFiYWE0MTgiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozMTgxNDA2MTEwNTc1NTc1MDR9.gw4_AKh6NGUxWXWjzHb8G2An3ao0nSuI

Content-Type: application/json; charset=utf-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 92823918712371

X-Type: 1

X-Channel：1001

x-Sign：用私钥对body内容加密后的内容
```

</div>

-   http body参数示例：

<div class="language-json extra-class">

``` language-json
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

</div>

返回示例：

<div class="language-json extra-class">

``` language-json
{
    "code": 0,
    "data": {
        "entrustId": "56765633083899904",
        "status": 0,
        "statusName": "等待提交"
    },
    "msg": ""
}
```

</div>

## 1 登录、密码及用户信息

### 1.1渠道密码登录

-   手机/邮箱+密码+渠道登录：

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/login`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/login`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   请求参数说明：

| 参数名称     | 说明                                                                                        | 请求类型 | 必填  | 类型   |
|--------------|---------------------------------------------------------------------------------------------|----------|-------|--------|
| X-Lang       | 语言类别(1-简体，2-繁体，3-English)                                                         | header   | true  | string |
| X-Request-Id | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等                        | header   | true  | string |
| X-Channel    | 渠道                                                                                        | header   | true  | string |
| X-Time       | 时间戳                                                                                      | header   | true  | string |
| X-Sign       | 签名                                                                                        | header   | true  | string |
| areaCode     | 区域号86中国，852香港，853中国澳门，886中国台湾，65新加坡。当使用手机号登录时，区号为必填。 | body     | false | string |
| password     | 密码RSA加密（与X-Sign不同秘钥）                                                             | body     | true  | string |
| phoneNumber  | 手机号/邮箱RSA加密（与X-Sign不同秘钥）                                                      | body     | true  | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232
 
X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例：

<div class="language-json extra-class">

``` language-json
{

    "areaCode": 86,

    "password": "rsa",

    "phoneNumber": "rsa"

}
```

</div>

-   出参说明：

| 参数名称        | 说明                                                 | 类型    |
|-----------------|------------------------------------------------------|---------|
| areaCode        | 区号                                                 | string  |
| avatar          | 头像地址                                             | string  |
| expiration      | 过期时间                                             | int64   |
| extendStatusBit | 用戶扩展状态                                         | int32   |
| firstLogin      | 是否为第一次登录                                     | boolean |
| nickname        | 昵称                                                 | string  |
| openedAccount   | 是否开户                                             | boolean |
| phoneNumber     | 手机号                                               | string  |
| thirdBindBit    | 绑定位 手机1&lt;&lt;0 微信 1&lt;&lt;1 微博1&lt;&lt;2 | int32   |
| token           | 登录鉴权的token                                      | string  |
| tradePassword   | 是否设置过交易密码                                   | boolean |
| unionId         | 微信公众平台的unionId，如果有则显示。                | string  |
| uuid            | 盈立用户注册的uuid，全局唯一                         | int64   |

-   返回示例：

<div class="language-json extra-class">

``` language-json
{

    "areaCode": 86,

    "avatar": "",

    "expiration": 0,

    "extendStatusBit": "1<<0 登录密码 1<<1 行情权限 1<<2 衍生品",

    "firstLogin": true,

    "nickname": "xxx",

    "openedAccount": true,

    "phoneNumber": "188xxxx9188",

    "thirdBindBit": 1,

    "token": "",

    "tradePassword": true,

    "unionId": "",

    "uuid": 0

}
```

</div>

-   响应状态

| 状态码 | 说明                                                     |
|--------|----------------------------------------------------------|
| 0      | 成功                                                     |
| 200    | OK                                                       |
| 300100 | 非法请求                                                 |
| 300102 | 账户被冻结，无法完成操作，如非本人操作，请联系客服       |
| 300103 | 用户被删除                                               |
| 300309 | 请输入正确的手机号码                                     |
| 300701 | 该手机号没有注册                                         |
| 300702 | 密码错误次数过多帐号已锁定，请%s分钟后重新登录或找回密码 |
| 300703 | 密码错误，请重新输入，您还可以尝试%s次                   |
| 300705 | 该帐户未设置登录密码，请使用短信验证码登录               |
| 300809 | 需要校验手机短信验证码                                   |

### 1.2获取手机/邮箱验证码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/send-phone-captcha`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/send-phone-captcha`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   请求参数说明：

| 参数名称     | 说明                                                                                        | 请求类型 | 必填  | 类型   |
|--------------|---------------------------------------------------------------------------------------------|----------|-------|--------|
| X-Lang       | 语言类别(1-简体，2-繁体，3-English)                                                         | header   | true  | string |
| X-Request-Id | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等                        | header   | true  | string |
| X-Channel    | 渠道                                                                                        | header   | true  | string |
| X-Time       | 时间戳                                                                                      | header   | true  | string |
| X-Sign       | 签名                                                                                        | header   | true  | string |
| areaCode     | 区域号86中国，852香港，853中国澳门，886中国台湾，65新加坡。当使用手机号登录时，区号为必填。 | body     | false | string |
| type         | 验证码类型 101注册 102重置密码 103更换手机号 104绑定手机号 105新设备登录校验 106短信登录    | body     | true  | string |
| phoneNumber  | 手机号/邮箱RSA加密（与X-Sign不同秘钥）                                                      | body     | true  | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例：

<div class="language-json extra-class">

``` language-json
{

    "areaCode": 86,

    "type": 102,

    "phoneNumber": "rsa"

}
```

</div>

-   出参说明：

| 参数名称        | 说明                                                 | 类型    |
|-----------------|------------------------------------------------------|---------|
| areaCode        | 区号                                                 | string  |
| avatar          | 头像地址                                             | string  |
| expiration      | 过期时间                                             | int64   |
| extendStatusBit | 用戶扩展状态                                         | int32   |
| firstLogin      | 是否为第一次登录                                     | boolean |
| invitationCode  | 邀请码，如果有，则显示。                             | string  |
| languageCn      | 1简体2繁体                                           | int32   |
| languageHk      | 1简体2繁体                                           | int32   |
| lineColorHk     | 1红涨绿跌2绿涨红跌                                   | int32   |
| nickname        | 昵称                                                 | string  |
| openedAccount   | 是否开户                                             | boolean |
| phoneNumber     | 手机号                                               | string  |
| thirdBindBit    | 绑定位 手机1&lt;&lt;0 微信 1&lt;&lt;1 微博1&lt;&lt;2 | int32   |
| token           | 登录鉴权的token                                      | string  |
| tradePassword   | 是否设置过交易密码                                   | boolean |
| unionId         | 微信公众平台的unionId，如果有则显示。                | string  |
| uuid            | 盈立用户注册的uuid，全局唯一                         | int64   |

-   返回示例：

<div class="language-json extra-class">

``` language-json
{

    "areaCode": 86,

    "avatar": "",

    "expiration": 0,

    "extendStatusBit": "1<<0 登录密码 1<<1 行情权限 1<<2 衍生品",

    "firstLogin": true,

    "invitationCode": 1234,

    "languageCn": 0,

    "languageHk": 0,

    "lineColorHk": 0,

    "nickname": "xxx",

    "openedAccount": true,

    "phoneNumber": "188xxxx9188",

    "thirdBindBit": 1,

    "token": "",

    "tradePassword": true,

    "unionId": "",

    "uuid": 0

}
```

</div>

-   响应状态

| 状态码 | 说明                                                     |
|--------|----------------------------------------------------------|
| 0      | 成功                                                     |
| 200    | OK                                                       |
| 300100 | 非法请求                                                 |
| 300102 | 账户被冻结，无法完成操作，如非本人操作，请联系客服       |
| 300103 | 用户被删除                                               |
| 300309 | 请输入正确的手机号码                                     |
| 300701 | 该手机号没有注册                                         |
| 300702 | 密码错误次数过多帐号已锁定，请%s分钟后重新登录或找回密码 |
| 300703 | 密码错误，请重新输入，您还可以尝试%s次                   |
| 300705 | 该帐户未设置登录密码，请使用短信验证码登录               |
| 300809 | 需要校验手机短信验证码                                   |

### 1.3渠道验证码登录

-   手机/邮箱+验证码+渠道登录：

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/loginCaptcha`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/loginCaptcha`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   请求参数说明：

| 参数名称     | 说明                                                                                        | 请求类型 | 必填  | 类型   |
|--------------|---------------------------------------------------------------------------------------------|----------|-------|--------|
| X-Lang       | 语言类别(1-简体，2-繁体，3-English)                                                         | header   | true  | string |
| X-Request-Id | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等                        | header   | true  | string |
| X-Channel    | 渠道                                                                                        | header   | true  | string |
| X-Time       | 时间戳                                                                                      | header   | true  | string |
| X-Sign       | 签名                                                                                        | header   | true  | string |
| areaCode     | 区域号86中国，852香港，853中国澳门，886中国台湾，65新加坡。当使用手机号登录时，区号为必填。 | body     | false | string |
| captcha      | 验证码                                                                                      | body     | true  | string |
| phoneNumber  | 手机号/邮箱RSA加密（与X-Sign不同秘钥）                                                      | body     | true  | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例：

<div class="language-json extra-class">

``` language-json
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

</div>

-   出参说明：

| 参数名称        | 说明                                                 | 类型    |
|-----------------|------------------------------------------------------|---------|
| areaCode        | 区号                                                 | string  |
| avatar          | 头像地址                                             | string  |
| expiration      | 过期时间                                             | int64   |
| extendStatusBit | 用戶扩展状态                                         | int32   |
| firstLogin      | 是否为第一次登录                                     | boolean |
| invitationCode  | 邀请码，如果有，则显示。                             | string  |
| languageCn      | 1简体2繁体                                           | int32   |
| languageHk      | 1简体2繁体                                           | int32   |
| lineColorHk     | 1红涨绿跌2绿涨红跌                                   | int32   |
| nickname        | 昵称                                                 | string  |
| openedAccount   | 是否开户                                             | boolean |
| phoneNumber     | 手机号                                               | string  |
| thirdBindBit    | 绑定位 手机1&lt;&lt;0 微信 1&lt;&lt;1 微博1&lt;&lt;2 | int32   |
| token           | 登录鉴权的token                                      | string  |
| tradePassword   | 是否设置过交易密码                                   | boolean |
| unionId         | 微信公众平台的unionId，如果有则显示。                | string  |
| uuid            | 盈立用户注册的uuid，全局唯一                         | int64   |

-   返回示例：

<div class="language-json extra-class">

``` language-json
{

    "areaCode": 86,

    "avatar": "",

    "expiration": 0,

    "extendStatusBit": "1<<0 登录密码 1<<1 行情权限 1<<2 衍生品",

    "firstLogin": true,

    "invitationCode": 1234,

    "languageCn": 0,

    "languageHk": 0,

    "lineColorHk": 0,

    "nickname": "xxx",

    "openedAccount": true,

    "phoneNumber": "188xxxx9188",

    "thirdBindBit": 1,

    "token": "",

    "tradePassword": true,

    "unionId": "",

    "uuid": 0

}
```

</div>

-   响应状态

| 状态码 | 说明                                                     |
|--------|----------------------------------------------------------|
| 0      | 成功                                                     |
| 200    | OK                                                       |
| 300100 | 非法请求                                                 |
| 300102 | 账户被冻结，无法完成操作，如非本人操作，请联系客服       |
| 300103 | 用户被删除                                               |
| 300309 | 请输入正确的手机号码                                     |
| 300701 | 该手机号没有注册                                         |
| 300702 | 密码错误次数过多帐号已锁定，请%s分钟后重新登录或找回密码 |
| 300703 | 密码错误，请重新输入，您还可以尝试%s次                   |
| 300705 | 该帐户未设置登录密码，请使用短信验证码登录               |
| 300809 | 需要校验手机短信验证码                                   |

### 1.4设置交易密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/set-trade-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/set-trade-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需带登录态token 用户需要完成开户，且未设置过交易密码，否则算非法请求

-   请求参数

| 参数名称      | 说明                                                                                       | 请求类型 | 必填  | 类型   |
|---------------|--------------------------------------------------------------------------------------------|----------|-------|--------|
| Authorization | 见概述Authorization说明                                                                    | header   | true  | string |
| X-Lang        | 语言1简体2繁体                                                                             | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等                       | header   | true  | string |
| X-Channel     | 渠道                                                                                       | header   | true  | string |
| X-Time        | 时间戳                                                                                     | header   | true  | string |
| X-Sign        | 签名                                                                                       | header   | true  | string |
| password      | 交易密码 设置、修改、重置交易密码必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥） | body     | true  | string |
| oldPassword   | 旧交易密码 修改交易密码必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥）           | body     | false | string |
| phoneCaptcha  | 手机验证码，根据验证码重置交易密码必填                                                     | body     | false | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "oldPassword": "",

  "password": "",

  "phoneCaptcha": ""

}
```

</div>

-   响应状态

| 状态码 | 说明                                               | schema             |
|--------|----------------------------------------------------|--------------------|
| 0      | 成功                                               |                    |
| 200    | OK                                                 | UserResponseEntity |
| 300100 | 非法请求                                           |                    |
| 300101 | 非法TOKEN                                          |                    |
| 301001 | 交易密码需为6位纯数字，请重新输入                  |                    |
| 301003 | 交易密码错误，请重新输入，您还可以尝试%s次         |                    |
| 301004 | 交易服務異常                                       |                    |
| 301005 | 账户被冻结，无法完成操作，如非本人操作，请联系客服 |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {},

  "msg": ""

}
```

</div>

### 1.5校验交易密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/check-trade-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/check-trade-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 权限：需要Token

-   请求参数

| 参数名称      | 说明                                                | 请求类型 | 必填  | 类型   |
|---------------|-----------------------------------------------------|----------|-------|--------|
| Authorization | 见概述Authorization说明                             | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                 | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息， 19位长度                  | header   | true  | string |
| X-Channel     | 渠道                                                | header   | true  | string |
| X-Time        | 时间戳                                              | header   | true  | string |
| X-Sign        | 签名                                                | header   | true  | string |
| password      | 交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥） | String   | false | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

/user-server/open-api/check-trade-password?password=123456 RES加密

-   响应状态

| 状态码 | 说明                                                     | schema             |
|--------|----------------------------------------------------------|--------------------|
| 0      | 成功                                                     |                    |
| 200    | OK                                                       | UserResponseEntity |
| 300100 | 非法请求                                                 |                    |
| 300101 | 非法TOKEN                                                |                    |
| 301001 | 交易密码需为6位纯数字，请重新输入                        |                    |
| 301002 | 错误次数过多交易密码已锁定，请%s小时后重新尝试或找回密码 |                    |
| 301004 | 交易服務異常                                             |                    |
| 310104 | 交易密码错误                                             |                    |
| 310106 | 未设置交易密码                                           |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {},

  "msg": ""

}
```

</div>

### 1.6重置登录密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/reset-login-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/reset-login-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 不需要token

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------------------|----------|-------|--------|
| Authorization | 见概述Authorization说明                                              | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true  | string |
| X-Channel     | 渠道                                                                 | header   | true  | string |
| X-Time        | 时间戳                                                               | header   | true  | string |
| X-Sign        | 签名                                                                 | header   | true  | string |
| areaCode      | 区域号86中国，852香港，853中国澳门，886中国台湾，65新加坡            | body     | false | string |
| password      | 新密码RSA加密（与X-Sign不同秘钥）                                    | body     | false | string |
| phoneCaptcha  | 手机验证码                                                           | body     | false | string |
| phoneNumber   | 手机号RSA加密（与X-Sign不同秘钥）                                    | body     | false | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "areaCode": "86",

    "password": "rsa",

    "phoneCaptcha": "1234",

    "phoneNumber": "188********"

}
```

</div>

-   响应状态

| 状态码 | 说明                                                             | schema             |
|--------|------------------------------------------------------------------|--------------------|
| 0      | 成功                                                             |                    |
| 200    | OK                                                               | UserResponseEntity |
| 300100 | 非法请求                                                         |                    |
| 300304 | 验证次数过多，请稍后重试                                         |                    |
| 300305 | 抱歉，验证码已过期，请重新获取                                   |                    |
| 300701 | 该手机号没有注册                                                 |                    |
| 300707 | 您当前已通过客户经理完成预注册，请通过短信验证码登录并激活账号。 |                    |
| 300800 | 短信验证码不正确，请重新输入                                     |                    |
| 300801 | 密码长度不能小于8位                                              |                    |
| 300802 | 密码长度不能大于24位                                             |                    |
| 300803 | 密码不能为纯数字/字母/符号                                       |                    |
| 300804 | 请设置正确密码，8\~24位数字/字母/符号组合                        |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "data": {},

    "msg": ""

}
```

</div>

### 1.7解锁交易

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/trade-login`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/trade-login`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要token

请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 见概述Authorization说明                                              | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Channel     | 渠道                                                                 | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Sign        | 签名                                                                 | header   | true | string |
| password      | 新密码RSA加密（与X-Sign不同秘钥）                                    | body     | true | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   响应状态

| 状态码 | 说明                                                             | schema             |
|--------|------------------------------------------------------------------|--------------------|
| 0      | 成功                                                             |                    |
| 200    | OK                                                               | UserResponseEntity |
| 300100 | 非法请求                                                         |                    |
| 300304 | 验证次数过多，请稍后重试                                         |                    |
| 300305 | 抱歉，验证码已过期，请重新获取                                   |                    |
| 300701 | 该手机号没有注册                                                 |                    |
| 300707 | 您当前已通过客户经理完成预注册，请通过短信验证码登录并激活账号。 |                    |
| 300800 | 短信验证码不正确，请重新输入                                     |                    |
| 300801 | 密码长度不能小于8位                                              |                    |
| 300802 | 密码长度不能大于24位                                             |                    |
| 300803 | 密码不能为纯数字/字母/符号                                       |                    |
| 300804 | 请设置正确密码，8\~24位数字/字母/符号组合                        |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": ,

  "msg": ""

}
```

</div>

### 1.8获取交易解锁状态

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/get-trade-status`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/get-trade-status`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要token

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 见概述Authorization说明                                              | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Channel     | 渠道                                                                 | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Sign        | 签名                                                                 | header   | true | string |
| password      | 新密码RSA加密（与X-Sign不同秘钥）                                    | body     | true | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   响应状态

| 状态码 | 说明                                                             | schema             |
|--------|------------------------------------------------------------------|--------------------|
| 0      | 成功                                                             |                    |
| 200    | OK                                                               | UserResponseEntity |
| 300100 | 非法请求                                                         |                    |
| 300304 | 验证次数过多，请稍后重试                                         |                    |
| 300305 | 抱歉，验证码已过期，请重新获取                                   |                    |
| 300701 | 该手机号没有注册                                                 |                    |
| 300707 | 您当前已通过客户经理完成预注册，请通过短信验证码登录并激活账号。 |                    |
| 300800 | 短信验证码不正确，请重新输入                                     |                    |
| 300801 | 密码长度不能小于8位                                              |                    |
| 300802 | 密码长度不能大于24位                                             |                    |
| 300803 | 密码不能为纯数字/字母/符号                                       |                    |
| 300804 | 请设置正确密码，8\~24位数字/字母/符号组合                        |                    |

-   响应参数

| 参数名称 | 说明                       | 类型   | schema |
|----------|----------------------------|--------|--------|
| code     | 响应码                     | int32  |        |
| data     | 响应体                     | object |        |
| status   | 订单状态，0未解密，1已解锁 | int32  |        |
| msg      | 响应内容                   | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
    "code": 0,
    "msg": "成功",
    "data": {
        "status": 0
    }
}
```

</div>

### 1.9修改交易密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/update-trade-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/update-trade-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需带登录态token 用户需要完成开户，且未设置过交易密码，否则算非法请求

-   请求参数

| 参数名称      | 说明                                                                             | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------------------------------|----------|-------|--------|
| Authorization | 见概述Authorization说明                                                          | header   | true  | string |
| X-Lang        | 语言1简体2繁体                                                                   | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等             | header   | true  | string |
| X-Channel     | 渠道                                                                             | header   | true  | string |
| X-Time        | 时间戳                                                                           | header   | true  | string |
| X-Sign        | 签名                                                                             | header   | true  | string |
| password      | 交易密码 必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥）               | body     | true  | string |
| oldPassword   | 旧交易密码 修改交易密码必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥） | body     | false | string |
| phoneCaptcha  | 手机验证码，根据验证码重置交易密码必填                                           | body     | false | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "oldPassword": "",

  "password": "",

  "phoneCaptcha": ""

}
```

</div>

-   响应状态

| 状态码 | 说明                                               | schema             |
|--------|----------------------------------------------------|--------------------|
| 0      | 成功                                               |                    |
| 200    | OK                                                 | UserResponseEntity |
| 300100 | 非法请求                                           |                    |
| 300101 | 非法TOKEN                                          |                    |
| 301001 | 交易密码需为6位纯数字，请重新输入                  |                    |
| 301003 | 交易密码错误，请重新输入，您还可以尝试%s次         |                    |
| 301004 | 交易服務異常                                       |                    |
| 301005 | 账户被冻结，无法完成操作，如非本人操作，请联系客服 |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {},

  "msg": ""

}
```

</div>

### 1.10重置交易密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/reset-trade-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/reset-trade-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需带登录态token 用户需要完成开户，且未设置过交易密码，否则算非法请求

-   请求参数

| 参数名称      | 说明                                                                   | 请求类型 | 必填  | 类型   |
|---------------|------------------------------------------------------------------------|----------|-------|--------|
| Authorization | 见概述Authorization说明                                                | header   | true  | string |
| X-Lang        | 语言1简体2繁体                                                         | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等   | header   | true  | string |
| X-Channel     | 渠道                                                                   | header   | true  | string |
| X-Time        | 时间戳                                                                 | header   | true  | string |
| X-Sign        | 签名                                                                   | header   | true  | string |
| password      | 交易密码 必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥）     | body     | true  | string |
| oldPassword   | 旧交易密码 非必填，交易密码必须是6位纯数字 RSA加密（与X-Sign不同秘钥） | body     | false | string |
| phoneCaptcha  | 手机验证码，根据验证码重置交易密码必填                                 | body     | false | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "oldPassword": "",

  "password": "",

  "phoneCaptcha": ""

}
```

</div>

-   响应状态

| 状态码 | 说明                                               | schema             |
|--------|----------------------------------------------------|--------------------|
| 0      | 成功                                               |                    |
| 200    | OK                                                 | UserResponseEntity |
| 300100 | 非法请求                                           |                    |
| 300101 | 非法TOKEN                                          |                    |
| 301001 | 交易密码需为6位纯数字，请重新输入                  |                    |
| 301003 | 交易密码错误，请重新输入，您还可以尝试%s次         |                    |
| 301004 | 交易服務異常                                       |                    |
| 301005 | 账户被冻结，无法完成操作，如非本人操作，请联系客服 |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {},

  "msg": ""

}
```

</div>

### 1.11修改登录密码

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/update-login-password`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/update-login-password`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需带登录态token 用户需要已设置登录密码，否则算非法请求

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 见概述Authorization说明                                              | header   | true | string |
| X-Lang        | 语言1简体2繁体                                                       | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Channel     | 渠道                                                                 | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Sign        | 签名                                                                 | header   | true | string |
| password      | 新登录密码 必填RSA加密（与X-Sign不同秘钥）                           | body     | true | string |
| oldPassword   | 旧登录密码 必填RSA加密（与X-Sign不同秘钥）                           | body     | true | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "oldPassword": "",

  "password": "",

}
```

</div>

-   响应状态

| 状态码 | 说明                                      | schema             |
|--------|-------------------------------------------|--------------------|
| 0      | 成功                                      |                    |
| 200    | OK                                        | UserResponseEntity |
| 300100 | 非法请求                                  |                    |
| 300101 | 非法TOKEN                                 |                    |
| 300704 | 原登录密码不正确                          |                    |
| 300804 | 请设置正确密码，8\~24位数字/字母/符号组合 |                    |
| 300810 | 新密码长度不能小于8位                     |                    |
| 300811 | 新密码长度不能大于24位                    |                    |
| 300812 | 新密码不能为纯数字/字母/符号              |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {},

  "msg": ""

}
```

</div>

### 1.12根据市场查询账户类型

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/get-user-info-with-market-for-stock/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/get-user-info-with-market-for-stock/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 根据市场获取用户信息

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型    |
|---------------|----------------------------------------------------------------------|----------|------|---------|
| Authorization | 见概述Authorization说明                                              | header   | true | string  |
| X-Lang        | 语言1简体2繁体                                                       | header   | true | string  |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string  |
| X-Channel     | 渠道                                                                 | header   | true | string  |
| X-Time        | 时间戳                                                               | header   | true | string  |
| X-Sign        | 签名                                                                 | header   | true | string  |
| marketType    | 市场类型（参考ExchangeType字典）                                     | body     | true | integer |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "marketType": 3

}
```

</div>

-   响应状态

| 状态码 | 说明      | schema             |
|--------|-----------|--------------------|
| 0      | 成功      |                    |
| 200    | OK        | UserResponseEntity |
| 300100 | 非法请求  |                    |
| 300101 | 非法TOKEN |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   出参说明：

| 参数名称  | 说明                                       | 类型   |
|-----------|--------------------------------------------|--------|
| assetProp | 账户类型,具体字典参考下面的AssetProp的值。 | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
    "code": 0,
    "msg": "成功",
    "data": {
        "assetProp": "M"
    }
}
```

</div>

### 1.13 根据资金账号查询融资利率

-   生产环境接口地址 `https://open-jy.yxzq.com/user-server/open-api/get-rate-info-by-fund-account/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/user-server/open-api/get-rate-info-by-fund-account/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 根据市场获取用户信息

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 见概述Authorization说明                                              | header   | true | string |
| X-Lang        | 语言1简体2繁体                                                       | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Channel     | 渠道                                                                 | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Sign        | 签名                                                                 | header   | true | string |
| fundAccount   | 用户的资金账号                                                       | body     | true | string |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
    "fundAccount": "80019641"
}
```

</div>

-   响应状态

| 状态码 | 说明      | schema             |
|--------|-----------|--------------------|
| 0      | 成功      |                    |
| 200    | OK        | UserResponseEntity |
| 300100 | 非法请求  |                    |
| 300101 | 非法TOKEN |                    |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 响应码   | int32  |        |
| data     | 响应体   | object |        |
| msg      | 响应内容 | string |        |

-   出参说明：

| 参数名称     | 说明                                        | 类型   |
|--------------|---------------------------------------------|--------|
| hkdRateValue | 港币利率，直接返回百分比；比如6.6，代表6.6% | number |
| usdRateValue | 美元利率，同上                              | number |
| cnyRateValue | 人民币利率，同上                            | number |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "data": {
    "hkdRateValue": 6.6,
    "usdRateValue": 4.6,
    "cnyRateValue": 6.6
  }
}
```

</div>

## **2** 交易及查询

### 2.1下单

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/entrust-order`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/entrust-order`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 下单

-   请求参数

| 参数名称         | 说明                                                                                                                                                                                                                | 请求类型 | 必填  | 类型    |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------|-------|---------|
| Authorization    | 头部信息的token信息                                                                                                                                                                                                 | header   | true  | string  |
| X-Lang           | 语言类别(1-简体，2-繁体，3-English)                                                                                                                                                                                 | header   | true  | string  |
| X-Channel        | 渠道ID，由盈立分配                                                                                                                                                                                                  | header   | true  | string  |
| X-Time           | 时间戳                                                                                                                                                                                                              | header   | true  | string  |
| X-Dt             | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac)                                                                                                                                                            | header   | true  | string  |
| X-Sign           | RSA签名                                                                                                                                                                                                             | header   | true  | string  |
| serialNo         | 流水号，最长19位，确保唯一推荐雪花算法生成                                                                                                                                                                          | body     | true  | int64   |
| entrustAmount    | 委托数量                                                                                                                                                                                                            | body     | true  | number  |
| entrustPrice     | 价格(竞价单价格传0)                                                                                                                                                                                                 | body     | true  | number  |
| entrustProp      | 委托属性('0'-美股限价单/暗盘委托limit order,'d'-竞价单,'e'-增强限价单,'g'-竞价限价单) 港股: ('0'-暗盘委托/限价单,'d'-竞价单,'e'-增强限价单,'g'-竞价限价单,'w'-市价单)美股: ('0'-限价单,'w'-市价单)A股: ('0'-限价单) | body     | true  | string  |
| entrustType      | 委托类别(0-买，1-卖)                                                                                                                                                                                                | body     | true  | int32   |
| exchangeType     | 交易类别(0-香港,5-美股,6-沪港通,7-深港通)                                                                                                                                                                           | body     | true  | int32   |
| stockCode        | 股票代码                                                                                                                                                                                                            | body     | true  | string  |
| password         | 交易密码（RSA公钥加密）                                                                                                                                                                                             | body     | false | string  |
| stockName        | 股票名称                                                                                                                                                                                                            | body     | false | string  |
| forceEntrustFlag | 是否强制委托标识，超过9倍24档下单时forceEntrustFlag=true可强制下单，但有可能是废单                                                                                                                                  | body     | false | boolean |
| sessionType      | 交易阶段标志（0/不传-正常订单交易（默认），1-盘前，2-盘后交易，3-暗盘交易，12-盘前盘后）                                                                                                                            | body     | false | int32   |
| orderType        | 订单类型：GTC/GTD/DAY(默认DAY当日有效，暂不支持)                                                                                                                                                                    | body     | false | string  |
| validDate        | 有效期（GTD传递订单,格式：yyyy-MM-dd，最多90天，暂不支持）                                                                                                                                                          | body     | false | string  |
| exchange         | 交易所 默认SMART（SMART,AMEX,ARCA,BATS,BEX,BYX,CBOE,CHX,DRCTEDGE,EDGEA,EDGX,IBKRTS,IEX,ISE,ISLAND,LTSE,MEMX,NYSE,NYSENAT,PEARL,PHLX,PSX)                                                                            | body     | false | string  |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "serialNo": "2000000000000000018",

  "entrustAmount": "1000",

  "entrustPrice": "11.0",

  "entrustProp": "e",

  "entrustType": "0",

  "exchangeType": "0",

  "stockCode": "00981",

  "stockName": "00981",

  "forceEntrustFlag": "false",

  "sessionType": "0",

  "password":"Fpocc_11vTS6mS9YKYby6-v2VNujUx_fnnMaGncHPerLh9mCP_vDIhbeE1GLNDU4arl1euay-hiTmqmlwZlwtCMbw3Law7mx9NgVuwGVX3pXPuwYjcqxhaGZIsATHDSywxd4uZZhTCsrRua-Ug8dgJaPDc5os7-A9sFYxbxhI6I="

}
```

</div>

-   响应状态

| 状态码 | 说明                                                                               | schema                           |
|--------|------------------------------------------------------------------------------------|----------------------------------|
| 0      | 成功                                                                               |                                  |
| 200    | OK                                                                                 | ResponseVO«EntrustOrderResponse» |
| 201    | Created                                                                            |                                  |
| 401    | Unauthorized                                                                       |                                  |
| 403    | Forbidden                                                                          |                                  |
| 404    | Not Found                                                                          |                                  |
| 406472 | 订单中不能包含小于1手数量的碎股，请交易1手的整数倍，或通过"碎股单"交易碎股         |                                  |
| 410200 | 抱歉，订单中不能包含小于1手数量的碎股，请交易1手的整数倍，如需交易碎股请联系客服。 |                                  |

-   响应参数

| 参数名称   | 说明                                    | 类型                 | schema               |
|------------|-----------------------------------------|----------------------|----------------------|
| code       | 状态码                                  | int32                |                      |
| data       | 返回体                                  | EntrustOrderResponse | EntrustOrderResponse |
| entrustId  | 订单id,可用于查询订单/修改订单/取消订单 | string               |                      |
| status     | 订单状态                                | int32                |                      |
| statusName | 订单状态名称                            | string               |                      |
| ·msg       | 状态信息                                | string               |                      |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
    "code": 0,
    "msg": "操作成功",
    "data": {
        "entrustId": "1181776863632019456",
        "status": 1,
        "statusName": "等待提交"
    }
}
```

</div>

### 2.2委托改单/撤单

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/modify-order`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/modify-order`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 委托改单/撤单

-   请求参数

| 参数名称         | 说明                                                                               | 请求类型 | 必填  | 类型    |
|------------------|------------------------------------------------------------------------------------|----------|-------|---------|
| Authorization    | 头部信息的token信息                                                                | header   | true  | string  |
| X-Lang           | 语言类别(1-简体，2-繁体，3-English)                                                | header   | true  | string  |
| X-Channel        | 渠道ID，由盈立分配                                                                 | header   | true  | string  |
| X-Time           | 时间戳                                                                             | header   | true  | string  |
| X-Request-Id     | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等               | header   | true  | string  |
| X-Sign           | RSA签名                                                                            | header   | true  | string  |
| actionType       | 操作类型(0-撤单，1-改单)                                                           | body     | true  | int32   |
| entrustAmount    | 委托数量，撤单时传0                                                                | body     | true  | number  |
| entrustId        | 委托Id                                                                             | body     | true  | int64   |
| entrustPrice     | 委托价格，撤单时传0                                                                | body     | true  | number  |
| password         | 交易密码（RSA公钥加密）                                                            | body     | false | string  |
| forceEntrustFlag | 是否强制委托标识，超过9倍24档下单时forceEntrustFlag=true可强制下单，但有可能是废单 | body     | false | boolean |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "actionType": 1,

    "entrustAmount": 500,

    "entrustId": 1181776863632019456,

    "entrustPrice": 322.0,

    "forceEntrustFlag": true

}
```

</div>

-   响应状态

| 状态码 | 说明                                                                               | schema |
|--------|------------------------------------------------------------------------------------|--------|
| 0      | 成功                                                                               |        |
| 200    | OK                                                                                 | Object |
| 201    | Created                                                                            |        |
| 401    | Unauthorized                                                                       |        |
| 403    | Forbidden                                                                          |        |
| 404    | Not Found                                                                          |        |
| 406472 | 订单中不能包含小于1手数量的碎股，请交易1手的整数倍，或通过"碎股单"交易碎股         |        |
| 410200 | 抱歉，订单中不能包含小于1手数量的碎股，请交易1手的整数倍，如需交易碎股请联系客服。 |        |

-   响应参数

| 参数名称   | 说明     | 类型   | schema |
|------------|----------|--------|--------|
| code       | 状态码   | int32  |        |
| data       | 返回体   | Object |        |
| entrustId  | 申请编号 | string |        |
| status     | 状态     | int32  |        |
| statusName | 状态名   | string |        |
| msg        | 状态信息 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "entrustId": "1181776863632019456",

        "status": 5,

        "statusName": "等待改单"

    }

}
```

</div>

### 2.3改单范围

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/modified-range`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/modified-range`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 改单展示范围

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填 | 类型   |
|---------------|-------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                 | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true | string |
| X-Time        | 时间戳                              | header   | true | string |
| X-Sign        | RSA签名                             | header   | true | string |
| entrustId     | 委托Id                              | body     | true | int64  |
| newPrice      | 最新价-竞价单也需要传最新价         | body     | true | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

<div class="language-json extra-class">

``` language-json
{

    "entrustId": 1181776863632019456,

    "newPrice": 323

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                               |
|--------|--------------|--------------------------------------|
| 0      | 成功         | ResponseVO                           |
| 200    | OK           | ResponseVO«QueryEntrustInfoResponse» |
| 201    | Created      |                                      |
| 401    | Unauthorized |                                      |
| 403    | Forbidden    |                                      |
| 404    | Not Found    |                                      |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>QueryEntrustInfoResponse</td><td>QueryEntrustInfoResponse</td></tr><tr class="odd"><td>businessAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="even"><td>entrustAmount</td><td>原订单数量</td><td>number</td><td></td></tr><tr class="odd"><td>modifiedUpperAmount</td><td>可修改范围的修改上限</td><td>number</td><td></td></tr><tr class="even"><td>modifiedlowerAmount</td><td>可修改范围的修改下限</td><td>number</td><td></td></tr><tr class="odd"><td>cashEnableAmount</td><td>现金最大可买</td><td>number</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
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
```

</div>

### 2.4碎股下单

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/odd-entrust`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/odd-entrust`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 碎股交易

-   请求示例

<div class="language-json extra-class">

``` language-json
{

  "entrustAmount": 1,

  "entrustPrice": 82.1,

  "entrustType": 1,

  "exchangeType": 0,

  "stockCode": "00002"

}
```

</div>

-   请求参数

| 参数名称      | 说明                                                     | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                      | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true | string |
| X-Time        | 时间戳                                                   | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true | string |
| X-Sign        | RSA签名                                                  | header   | true | string |
| entrustAmount | 委托数量                                                 | body     | true | number |
| entrustPrice  | 价格                                                     | body     | true | number |
| entrustType   | 委托类别(1-卖)                                           | body     | true | int32  |
| exchangeType  | 交易类别(0-香港,5-美股)                                  | body     | true | int32  |
| stockCode     | 股票代码                                                 | body     | true | string |

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

| 参数名称   | 说明           | 类型   |
|------------|----------------|--------|
| code       | 状态码         | int32  |
| data       | 返回体         |        |
| oddId      | 碎股请求记录id | string |
| status     | 订单状态       | int32  |
| statusName | 订单状态名称   | string |
| msg        | 状态信息       | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
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

</div>

### 2.5碎股撤单

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/odd-modify`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/odd-modify`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 碎股交易

请求示例

<div class="language-json extra-class">

``` language-json
{

  "actionType": 0,

  "oddId": 1207553433704988672

}
```

</div>

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                                  | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                                   | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Sign        | RSA签名                                                              | header   | true | string |
| actionType    | 操作类型(0-撤单)                                                     | body     | true | int32  |
| oddId         | 碎股委托Id                                                           | body     | true | int64  |

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数

| 参数名称   | 说明           | 类型   |
|------------|----------------|--------|
| code       | 状态码         | int32  |
| oddId      | 碎股请求记录id | string |
| status     | 订单状态       | int32  |
| statusName | 订单状态名称   | string |
| msg        | 状态信息       | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
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

</div>

### 2.6最大可买、可卖数量

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/trade-quantity`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/trade-quantity`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 获取最大可用数量

-   请求参数

| 参数名称      | 说明                                                                           | 请求类型 | 必填  | 类型   |
|---------------|--------------------------------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                                            | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                            | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                                             | header   | true  | string |
| X-Time        | 时间戳                                                                         | header   | true  | string |
| X-Sign        | RSA签名                                                                        | header   | true  | string |
| entrustPrice  | 委托价格(不能为0,竞价单可不填)                                                 | body     | false | number |
| entrustProp   | 委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单，'u'-碎股单) | body     | true  | string |
| exchangeType  | 交易类别(0-香港,5-美股,6-沪港通,7-深港通)                                      | body     | true  | int32  |
| stockCode     | 证券代码                                                                       | body     | true  | string |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "entrustPrice": 234,

    "entrustProp": "e",

    "exchangeType": 0,

    "stockCode": "700"

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                 |
|--------|--------------|----------------------------------------|
| 0      | 成功         | ResponseVO                             |
| 200    | OK           | ResponseVO«SaleAndBuyQuantityResponse» |
| 201    | Created      |                                        |
| 401    | Unauthorized |                                        |
| 403    | Forbidden    |                                        |
| 404    | Not Found    |                                        |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>SaleAndBuyQuantityResponse</td><td>SaleAndBuyQuantityResponse</td></tr><tr class="odd"><td>buyEnableAmount</td><td>最大可买数量（融资可买）</td><td>number</td><td></td></tr><tr class="even"><td>oddEnableAmount</td><td>最大可卖碎股数量</td><td>number</td><td></td></tr><tr class="odd"><td>saleEnableAmount</td><td>最大可卖数量（现金）</td><td>number</td><td></td></tr><tr class="even"><td>saleEnableIntAmount</td><td>最大可卖整股数量</td><td>number</td><td></td></tr><tr class="odd"><td>handAmount</td><td>每手股数</td><td>number</td><td></td></tr><tr class="even"><td>cashEnableAmount</td><td>现金可买数量-包含碎股：查可买返回</td><td>number</td><td></td></tr><tr class="odd"><td>cashEnableIntAmount</td><td>现金可买整手数量：查可买返回</td><td>number</td><td></td></tr><tr class="even"><td>cashPurchasingPower</td><td>现金购买力，查可买返回</td><td>number</td><td></td></tr><tr class="odd"><td>maxPurchasingPower</td><td>融资购买力，margin账户&amp;&amp;查可买返回</td><td>number</td><td></td></tr><tr class="even"><td>fundAccoutType</td><td>资金账号类型(0-现金账号，M-融资账号)</td><td>string</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
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

</div>

### 2.7今日订单-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/today-entrust`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/today-entrust`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要资金账号

-   请求参数

| 参数名称      | 说明                                                  | 请求类型 | 必填  | 类型   |
|---------------|-------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                   | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                   | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                    | header   | true  | string |
| X-Time        | 时间戳                                                | header   | true  | string |
| X-Sign        | RSA签名                                               | header   | true  | string |
| exchangeType  | 交易类别(0-香港,5-美股, 67-A股，100-查询所有交易类别) | body     | true  | int32  |
| pageNum       | 当前页 1开始，默认值1                                 | body     | false | int32  |
| pageSize      | 每页结果数，默认值10                                  | body     | false | int32  |
| stockCode     | 证券代码                                              | body     | false | string |
| stockName     | 证券名称                                              | body     | false | string |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "exchangeType": 0,

    "pageNum": 1,

    "pageSize": 10,

    "stockCode": "",

    "stockName": ""

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                            |
|--------|--------------|---------------------------------------------------|
| 0      | 成功         | ResponseVO                                        |
| 200    | OK           | ResponseVO«PageInfoVO«TodayEntrustByAppResponse»» |
| 201    | Created      |                                                   |
| 401    | Unauthorized |                                                   |
| 403    | Forbidden    |                                                   |
| 404    | Not Found    |                                                   |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«TodayEntrustByAppResponse»</td><td>PageInfoVO«TodayEntrustByAppResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>TodayEntrustByAppResponse</td></tr><tr class="even"><td>businessAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>businessAveragePrice</td><td>成交均价</td><td>number</td><td></td></tr><tr class="even"><td>serialNo</td><td>流水号</td><td>int64</td><td></td></tr><tr class="odd"><td>createTime</td><td>委托时间</td><td>string</td><td></td></tr><tr class="even"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="odd"><td>entrustId</td><td>委托id</td><td>string</td><td></td></tr><tr class="even"><td>entrustNo</td><td>委托编号</td><td>string</td><td></td></tr><tr class="odd"><td>entrustPrice</td><td>委托价格</td><td>number</td><td></td></tr><tr class="even"><td>entrustProp</td><td>委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单,'h'-港股限价单,'j'-特殊限价单)</td><td>string</td><td></td></tr><tr class="odd"><td>entrustType</td><td>买卖方向,委托类型(0-买，1-卖)</td><td>int32</td><td></td></tr><tr class="even"><td>exchangeType</td><td>交易类别，0港股，5美股</td><td>int32</td><td></td></tr><tr class="odd"><td>flag</td><td>订单类型-普通单0-条件单1-碎股单2-月供股单</td><td>string</td><td></td></tr><tr class="even"><td>moneyType</td><td>币种类别</td><td>int32</td><td></td></tr><tr class="odd"><td>sessionType</td><td>交易阶段标志（0/不传-正常订单交易（默认），1-盘前，2-盘后交易，3-暗盘交易）</td><td>int32</td><td></td></tr><tr class="even"><td>status</td><td>委托状态</td><td>int32</td><td></td></tr><tr class="odd"><td>statusName</td><td>委托状态名</td><td>string</td><td></td></tr><tr class="even"><td>stockCode</td><td>股票代码</td><td>string</td><td></td></tr><tr class="odd"><td>stockName</td><td>股票简体名称</td><td>string</td><td></td></tr><tr class="even"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="odd"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="even"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "pageNum": 1,

        "pageSize": 0,

        "total": 1,

        "list": [{

            "entrustId": "1181776863632019456",

            "entrustNo": "191",

            "status": 5,

            "statusName": "等待改单",

            "exchangeType": 0,

            "entrustType": 0,

            "entrustProp": "e",

            "entrustAmount": 700,

            "businessAmount": 0,

            "entrustPrice": 210,

            "businessAveragePrice": 0,

            "stockCode": "00700",

            "stockName": "腾讯控股",

            "moneyType": 2,

            "createTime": "11:42:15",

            "flag": "0",

            "serialNo": 1233123554314,

            "sessionType": 0

        }]

    }

}
```

</div>

### 2.8全部订单-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/his-entrust`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/his-entrust`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要资金账号

-   请求参数

| 参数名称         | 说明                                                                                         | 请求类型 | 必填  | 类型   |
|------------------|----------------------------------------------------------------------------------------------|----------|-------|--------|
| Authorization    | 头部信息的token信息                                                                          | header   | true  | string |
| X-Lang           | 语言类别(1-简体，2-繁体，3-English)                                                          | header   | true  | string |
| X-Channel        | 渠道ID，由盈立分配                                                                           | header   | true  | string |
| X-Time           | 时间戳                                                                                       | header   | true  | string |
| X-Sign           | RSA签名                                                                                      | header   | true  | string |
| dateFlag         | 1:一周订单，2：一个月订单，3: 三个月订单，4：近一年订单，5：今年订单，6：自选时间,7.查询全部 | body     | true  | string |
| exchangeType     | 交易类别(0-香港,5-美股, 67-A股，100-查询所有交易类别)                                        | body     | true  | int32  |
| entrustBeginDate | 开始时间，如果不传时间默认从最新前一天倒序,规则yyyy-MM-dd                                    | body     | false | string |
| entrustEndDate   | 结束时间，如果不传时间默认从最新前一天倒序,规则yyyy-MM-dd                                    | body     | false | string |
| pageNum          | 当前页 1开始，默认值1                                                                        | body     | false | int32  |
| pageSize         | 每页结果数，默认值10                                                                         | body     | false | int32  |
| stockCode        | 证券代码                                                                                     | body     | false | string |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "dateFlag": "1",

    "entrustBeginDate": "",

    "entrustEndDate": "",

    "exchangeType": 0,

    "pageNum": 1,

    "pageSize": 10,

    "stockCode": ""

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                          |
|--------|--------------|-------------------------------------------------|
| 0      | 成功         | ResponseVO                                      |
| 200    | OK           | ResponseVO«PageInfoVO«HisEntrustByAppResponse»» |
| 201    | Created      |                                                 |
| 401    | Unauthorized |                                                 |
| 403    | Forbidden    |                                                 |
| 404    | Not Found    |                                                 |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«HisEntrustByAppResponse»</td><td>PageInfoVO«HisEntrustByAppResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>HisEntrustByAppResponse</td></tr><tr class="even"><td>businessAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>businessAveragePrice</td><td>成交均价</td><td>number</td><td></td></tr><tr class="even"><td>serialNo</td><td>流水号</td><td>int64</td><td></td></tr><tr class="odd"><td>createDate</td><td>委托日期</td><td>string</td><td></td></tr><tr class="even"><td>createTime</td><td>委托时间</td><td>string</td><td></td></tr><tr class="odd"><td>dayEnd</td><td>是否隔天,0未隔天，1已经隔天</td><td>int32</td><td></td></tr><tr class="even"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="odd"><td>entrustId</td><td>委托ID</td><td>string</td><td></td></tr><tr class="even"><td>entrustNo</td><td>委托编号</td><td>string</td><td></td></tr><tr class="odd"><td>entrustPrice</td><td>委托价格</td><td>number</td><td></td></tr><tr class="even"><td>entrustProp</td><td>委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单,'h'-港股限价单,'j'-特殊限价单)</td><td>string</td><td></td></tr><tr class="odd"><td>entrustType</td><td>买卖方向,委托类型(0-买，1-卖)</td><td>int32</td><td></td></tr><tr class="even"><td>exchangeType</td><td>交易类别，0港股，5美股</td><td>int32</td><td></td></tr><tr class="odd"><td>flag</td><td>订单类型-普通单1-条件单2-碎股单3-月供股单4</td><td>string</td><td></td></tr><tr class="even"><td>moneyType</td><td>币种类别</td><td>int32</td><td></td></tr><tr class="odd"><td>sessionType</td><td>交易阶段标志（0/不传-正常订单交易（默认），1-盘前，2-盘后交易，3-暗盘交易）</td><td>int32</td><td></td></tr><tr class="even"><td>status</td><td>委托状态</td><td>int32</td><td></td></tr><tr class="odd"><td>statusName</td><td>委托状态名</td><td>string</td><td></td></tr><tr class="even"><td>stockCode</td><td>股票代码</td><td>string</td><td></td></tr><tr class="odd"><td>stockName</td><td>股票简体名称</td><td>string</td><td></td></tr><tr class="even"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="odd"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="even"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
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

                "status": 5,

                "statusName": "等待改单",

                "exchangeType": 0,

                "entrustType": 0,

                "entrustProp": "e",

                "entrustAmount": 700,

                "businessAmount": 0,

                "entrustPrice": 210,

                "businessAveragePrice": 0,

                "stockCode": "00700",

                "stockName": "腾讯控股",

                "moneyType": 2,

                "createTime": "11:42:15",

                "createDate": "20191009",

                "flag": "0",

                "serialNo": 1233123554314,

                "sessionType": 0

            }

        ],

        "nowDate": "20191009"

    }

}
```

</div>

### 2.9查询订单明细

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/order-detail`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/order-detail`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 查询订单明细

-   请求参数

| 参数名称                      | 说明                                   | 请求类型 | 必填 | 类型                          |
|-------------------------------|----------------------------------------|----------|------|-------------------------------|
| Authorization                 | 头部信息的token信息                    | header   | true | string                        |
| X-Lang                        | 语言类别(1-简体，2-繁体，3-English)    | header   | true | string                        |
| X-Channel                     | 渠道ID，由盈立分配                     | header   | true | string                        |
| X-Time                        | 时间戳                                 | header   | true | string                        |
| X-Sign                        | RSA签名                                | header   | true | string                        |
| appEntrustRecordDetailRequest | appEntrustRecordDetailRequest          | body     | true | AppEntrustRecordDetailRequest |
| serialNo                      | 流水号（委托ID、流水号一个至少传一个） | body     | true | int64                         |
| entrustId                     | 委托id（委托ID、流水号一个至少传一个） | body     | true | int64                         |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

<div class="language-json extra-class">

``` language-json
{

    "serialNo": 0,

    "entrustId": 0

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                     |
|--------|--------------|--------------------------------------------|
| 0      | 成功         | ResponseVO                                 |
| 200    | OK           | ResponseVO«AppEntrustRecordDetailResponse» |
| 201    | Created      |                                            |
| 401    | Unauthorized |                                            |
| 403    | Forbidden    |                                            |
| 404    | Not Found    |                                            |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>AppEntrustRecordDetailResponse</td><td>AppEntrustRecordDetailResponse</td></tr><tr class="odd"><td>appEntrustRecordDetailInfoList</td><td>list信息</td><td>array</td><td>AppEntrustRecordDetailInfo</td></tr><tr class="even"><td>businessAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>businessAveragePrice</td><td>成交均价</td><td>number</td><td></td></tr><tr class="even"><td>businessBalance</td><td>成交金额</td><td>number</td><td></td></tr><tr class="odd"><td>commissionFee</td><td>港美,佣金</td><td>string</td><td></td></tr><tr class="even"><td>createTime</td><td>时间</td><td>string</td><td></td></tr><tr class="odd"><td>depositStockDay</td><td>股份到账时间</td><td>string</td><td></td></tr><tr class="even"><td>entrustId</td><td>委托记录号</td><td>int64</td><td></td></tr><tr class="odd"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="even"><td>entrustBalance</td><td>委托金额</td><td>number</td><td></td></tr><tr class="odd"><td>entrustFee</td><td>总费用</td><td>string</td><td></td></tr><tr class="even"><td>entrustPrice</td><td>委托价格</td><td>number</td><td></td></tr><tr class="odd"><td>entrustProp</td><td>委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单,'h'-港股限价单,'j'-特殊限价单)</td><td>string</td><td></td></tr><tr class="even"><td>entrustPropName</td><td>委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单,'h'-港股限价单,'j'-特殊限价单)</td><td>string</td><td></td></tr><tr class="odd"><td>moneyType</td><td>币种类别</td><td>int32</td><td></td></tr><tr class="even"><td>orderStatus</td><td>状态</td><td>int32</td><td></td></tr><tr class="odd"><td>orderStatusName</td><td>状态名</td><td>string</td><td></td></tr><tr class="even"><td>payFee</td><td>港美，交收费</td><td>string</td><td></td></tr><tr class="odd"><td>platformUseFee</td><td>港美,平台使用费</td><td>string</td><td></td></tr><tr class="even"><td>stampDutyFee</td><td>港，印花税</td><td>string</td><td></td></tr><tr class="odd"><td>tradingSystemUsage</td><td>港，交易系统使用费</td><td>string</td><td></td></tr><tr class="even"><td>transactionFee</td><td>港：交易费，美：证监会规费</td><td>string</td><td></td></tr><tr class="odd"><td>transactionLevyFee</td><td>港，交易征费，美：交易活动费</td><td>string</td><td></td></tr><tr class="even"><td>frcTransactionLevyFee</td><td>港，财汇局交易征费 （2022.1.1起征）</td><td>string</td><td></td></tr><tr class="odd"><td>document</td><td>文案信息</td><td>string</td><td></td></tr><tr class="even"><td>entrustType</td><td>买入卖出</td><td>int32</td><td></td></tr><tr class="odd"><td>exchangeType</td><td>市场类型</td><td>int32</td><td></td></tr><tr class="even"><td>sessionType</td><td>交易阶段标志（0/不传-正常订单交易（默认），1-盘前，2-盘后交易，3-暗盘交易）</td><td>int32</td><td></td></tr><tr class="odd"><td>status</td><td>委托状态</td><td>int32</td><td></td></tr><tr class="even"><td>statusName</td><td>委托状态名</td><td>string</td><td></td></tr><tr class="odd"><td>stockCode</td><td>股票代码</td><td>string</td><td></td></tr><tr class="even"><td>stockName</td><td>股票名称</td><td>string</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{

​   "code": 0,

​   "msg": "操作成功",

​   "data": {

​       "statusName": "全部成交",

​       "status": 0,

​       "stockCode": "00700",

​       "stockName": "腾讯控股",

​       "document": "由于和交易所清算交收，部分数据可能在交易完成的第2天（工作日）展示",

​       "appEntrustRecordDetailInfoList": [{

​               "entrustProp": "e",

​               "entrustPropName": "增强限价单",

​               "entrustAmount": 700,

​               "businessAmount": 700,

​               "entrustPrice": 210,

​               "entrustBalance": 147000,

​               "businessAveragePrice": 322,

​               "businessBalance": 225400,

​               "moneyType": 2,

​               "createTime": "2019-10-09 11:42:15",

​               "depositStockDay": null,

​               "commissionFee": null,

​               "platformUseFee": null,

​               "stampDutyFee": null,

​               "payFee": null,

​               "transactionFee": null,

​               "transactionLevyFee": null,

​               "tradingSystemUsage": null,

​               "entrustFee": null,

​               "orderStatus": 11,

​               "orderStatusName": "委托下单"

​           },

​           {

​               "entrustProp": "e",

​               "entrustPropName": "增强限价单",

​               "entrustAmount": 700,

​               "businessAmount": 700,

​               "entrustPrice": 322,

​               "entrustBalance": 225400,

​               "businessAveragePrice": 322,

​               "businessBalance": 225400,

​               "moneyType": 2,

​               "createTime": "2019-10-09 14:58:03",

​               "depositStockDay": null,

​               "commissionFee": null,

​               "platformUseFee": null,

​               "stampDutyFee": null,

​               "payFee": null,

​               "transactionFee": null,

​               "transactionLevyFee": null,

​               "tradingSystemUsage": null,

​               "entrustFee": null,

​               "orderStatus": 21,

​               "orderStatusName": "改单（最新订单）"

​           },

​           {

​               "entrustProp": "e",

​               "entrustPropName": "增强限价单",

​               "entrustAmount": 700,

​               "businessAmount": 700,

​               "entrustPrice": 322,

​               "entrustBalance": 225400,

​               "businessAveragePrice": 322,

​               "businessBalance": 225400,

​               "moneyType": 2,

​               "createTime": "2019-10-09 15:00:30",

​               "depositStockDay": null,

​               "commissionFee": null,

​               "platformUseFee": null,

​               "stampDutyFee": null,

​               "payFee": null,

​               "transactionFee": null,

​               "transactionLevyFee": null,

​               "tradingSystemUsage": null,

​               "entrustFee": null,

​               "orderStatus": 0,

​               "orderStatusName": "全部成交（订单结束）"

​           }

​       ],

​       "entrustType": 0,

​       "exchangeType": 0,

​       "finalStateFlag": "1",

​       "sessionType": 0,

"entrustId": 1181776863632019500

​   }

}
```

</div>

### 2.10查询成交流水-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/stock-record`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/stock-record`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要资金账号

-   请求参数

| 参数名称      | 说明                                                  | 请求类型 | 必填  | 类型   |
|---------------|-------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                   | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                   | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                    | header   | true  | string |
| X-Time        | 时间戳                                                | header   | true  | string |
| X-Sign        | RSA签名                                               | header   | true  | string |
| exchangeType  | 交易类别(0-香港,5-美股, 67-A股，100-查询所有交易类别) | body     | true  | int32  |
| stockCode     | 股票代码                                              | body     | false | string |
| entrustId     | 委托ID                                                | body     | false | int64  |
| beginTime     | 成交开始时间，规则yyyy-MM-dd                          | body     | false | string |
| endTime       | 成交结束时间，规则yyyy-MM-dd                          | body     | false | string |
| pageNum       | 当前页 1开始，默认值1                                 | body     | false | int32  |
| pageSize      | 每页结果数，默认值10                                  | body     | false | int32  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

<div class="language-json extra-class">

``` language-json
{

​   "beginTime": "2019-10-01",

​   "endTime": "2019-10-10",

​   "entrustId": 0,

​   "exchangeType": 0,

​   "pageNum": 1,

​   "pageSize": 10,

​   "stockCode": "700"

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                      |
|--------|--------------|---------------------------------------------|
| 0      | 成功         | ResponseVO                                  |
| 200    | OK           | ResponseVO«PageInfoVO«StockRecordResponse»» |
| 201    | Created      |                                             |
| 401    | Unauthorized |                                             |
| 403    | Forbidden    |                                             |
| 404    | Not Found    |                                             |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«StockRecordResponse»</td><td>PageInfoVO«StockRecordResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>StockRecordResponse</td></tr><tr class="even"><td>businessAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>businessBalance</td><td>成交金额</td><td>number</td><td></td></tr><tr class="even"><td>businessPrice</td><td>成交价格</td><td>number</td><td></td></tr><tr class="odd"><td>businessStatus</td><td>成交状态（1成交成功，2成交取消）</td><td>int32</td><td></td></tr><tr class="even"><td>businessTime</td><td>成交时间</td><td>date-time</td><td></td></tr><tr class="odd"><td>createTime</td><td>记录创建时间</td><td>date-time</td><td></td></tr><tr class="even"><td>entrustId</td><td>委托记录号</td><td>int64</td><td></td></tr><tr class="odd"><td>entrustType</td><td>委托类型(''0''-买，1-卖，''2''-查询，''3'-撤单，''4'-补单，''5''-改单，6转入，7转出,8成交取消类型)</td><td>int32</td><td></td></tr><tr class="even"><td>exchangeType</td><td>交易类别('0'-香港，'1'-上海A，'2'-上海B，'3'-深圳A，'4'-深证B，'5'-美股，'6'-沪股通，'7'-深港通)</td><td>int32</td><td></td></tr><tr class="odd"><td>id</td><td></td><td>int64</td><td></td></tr><tr class="even"><td>moneyType</td><td>币种类型(0-人民币，1-美元，2-港币)</td><td>int32</td><td></td></tr><tr class="odd"><td>recordId</td><td>成交流水编号</td><td>int64</td><td></td></tr><tr class="even"><td>remark</td><td>备注</td><td>string</td><td></td></tr><tr class="odd"><td>stockCode</td><td>股票代码</td><td>string</td><td></td></tr><tr class="even"><td>stockName</td><td>股票名称</td><td>string</td><td></td></tr><tr class="odd"><td>updateTime</td><td>记录最后更新时间</td><td>date-time</td><td></td></tr><tr class="even"><td>userId</td><td>用户id</td><td>int64</td><td></td></tr><tr class="odd"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="even"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="odd"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{

​   "code": 0,

​   "msg": "操作成功",

​   "data": {

​       "pageNum": 1,

​       "pageSize": 10,

​       "total": 133,

​       "list": [{

​           "id": 18405,

​           "recordId": 1139100093871222800,

​           "entrustId": 1139096696801153000,

​           "userId": 336547695646785540,

​           "moneyType": 2,

​           "exchangeType": 0,

​           "stockCode": "700",

​           "stockName": "腾讯控股",

​           "businessStatus": 1,

​           "businessPrice": 334.2,

​           "businessAmount": 10,

​           "businessTime": "2019-06-14T09:12:49.000+0000",

​           "createTime": "2019-06-13T09:20:00.000+0000",

​           "updateTime": "2019-06-13T09:20:00.000+0000",

​           "remark": null,

​           "entrustType": 0,

​           "businessBalance": 3342

​       }]

​   }

}
```

</div>

### 2.11查询资产

-   生产环境接口地址 `https://open-jy.yxzq.com/asset-center-server/open-api/open-assetQuery/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/asset-center-server/open-api/open-assetQuery/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 查询资产

-   请求参数

| 参数名称      | 说明                                      | 请求类型 | 必填  | 类型           |
|---------------|-------------------------------------------|----------|-------|----------------|
| Authorization | 头部信息的token信息                       | header   | true  | string         |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)       | header   | true  | string         |
| X-Channel     | 渠道                                      | header   | true  | string         |
| X-Time        | 时间戳                                    | header   | true  | string         |
| X-Sign        | RSA签名                                   | header   | true  | string         |
| moneyType     | 金额的币种类型 (0:人民币; 1:美元; 2:港币) | body     | false | integer(int32) |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

  "moneyType": 0

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                              |
|--------|--------------|-------------------------------------|
| 0      | 成功         | ResponseVO                          |
| 200    | OK           | ResponseVO«MultiAssetAllInfoRespVO» |
| 201    | Created      |                                     |
| 401    | Unauthorized | \+                                  |
| 403    | Forbidden    |                                     |
| 404    | Not Found    |                                     |

-   响应参数

| 参数名称                  | 参数说明                                                                                                                                                                                                                                                              | 类型                      | schema                     |
|---------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------|----------------------------|
| code                      | 状态码                                                                                                                                                                                                                                                                | integer(int32)            | integer(int32)             |
| data                      | 返回体                                                                                                                                                                                                                                                                | MultiAssetAllInfoRespVO   | MultiAssetAllInfoRespVO    |
| assetSingleInfoRespVOS    | 业务对象明细                                                                                                                                                                                                                                                          | array                     | MultiAssetSingleInfoRespVO |
| asset                     | 总资产                                                                                                                                                                                                                                                                | number                    |                            |
| availableBalance          | 可用金额·                                                                                                                                                                                                                                                             | number                    |                            |
| borrowAmount              | 融资金额,日内融业务使用                                                                                                                                                                                                                                               | number                    |                            |
| cashBalance               | 现金资产,基金为0                                                                                                                                                                                                                                                      | number                    |                            |
| cashFundAsset             | 现金+资产,基金业务使用                                                                                                                                                                                                                                                | number                    |                            |
| costBalance               | 持仓成本                                                                                                                                                                                                                                                              | number                    |                            |
| dueInterest               | 应收利息（债券用）                                                                                                                                                                                                                                                    | number                    |                            |
| frozenBalance             | 冻结金额                                                                                                                                                                                                                                                              | number                    |                            |
| fundAccount               | 业务账户                                                                                                                                                                                                                                                              | string                    |                            |
| fundAccountStatus         | 当前业务是否开通的状态 1已开通，2未开通                                                                                                                                                                                                                               | integer(int32)            |                            |
| fundAccountType           | 账户类型-正股类型的账户只返回现金、融资 (0:普通账户; 2:margin账户; 4:跟投账户; 6:碎股账户; 10:DA账户; 11:MA公共账户; 12:MA费用账户; 20:日内融账户; 30:期权账户; 31:期权沽空账户; 40:沽空账户; 50:统一理财账户; 51:基金账户; 52:Cash+账户; 60:债券账户; 61:债券账户V2) | integer(int32)            |                            |
| fundAsset                 | 基金资产,基金业务使用                                                                                                                                                                                                                                                 | number                    |                            |
| holdInfos                 | 持仓信息                                                                                                                                                                                                                                                              | array                     | HomePageHoldInfoAppRespVO  |
| businessType              | 业务类型，暂定股票做空(SS)、期权（O）、期权沽空(OS)使用                                                                                                                                                                                                               | string                    |                            |
| code                      | 代码                                                                                                                                                                                                                                                                  | string                    |                            |
| costBalance               | 持仓成本总金额                                                                                                                                                                                                                                                        | number                    |                            |
| costPrice                 | 成本价                                                                                                                                                                                                                                                                | number                    |                            |
| curHoldNum                | 持仓数量                                                                                                                                                                                                                                                              | number                    |                            |
| dueInterest               | 应收利息                                                                                                                                                                                                                                                              | number                    |                            |
| exchangeType              | 交易类型                                                                                                                                                                                                                                                              | integer(int32)            |                            |
| fundAccountType           | 资金账号类型                                                                                                                                                                                                                                                          | integer(int32)            |                            |
| holdProfit                | 持仓盈亏                                                                                                                                                                                                                                                              | number                    |                            |
| holdProfitPercent         | 持仓盈亏率                                                                                                                                                                                                                                                            | number                    |                            |
| holdProfitVar             | 持仓盈亏变量 0 或者 1，默认情况是 0                                                                                                                                                                                                                                   | integer(int32)            |                            |
| id                        | ID                                                                                                                                                                                                                                                                    | integer(int64)            |                            |
| isinOrCusip               | 债券isin或cusip                                                                                                                                                                                                                                                       | string                    |                            |
| marketValue               | 市值                                                                                                                                                                                                                                                                  | number                    |                            |
| moneyType                 | 券的交易币种                                                                                                                                                                                                                                                          | integer(int32)            |                            |
| multiplier                | 乘数，期权使用。                                                                                                                                                                                                                                                      | number                    |                            |
| name                      | 名称                                                                                                                                                                                                                                                                  | string                    |                            |
| newHoldProfitVar          | 新持仓盈亏变量 0 或者 1，默认情况是 0                                                                                                                                                                                                                                 | integer(int32)            |                            |
| newTodayProfitDB          | 新今日盈亏金额                                                                                                                                                                                                                                                        | number                    |                            |
| newTodayProfitVar         | 新今日盈亏变量 0 或者 1，默认情况是 1                                                                                                                                                                                                                                 | integer(int32)            |                            |
| nextInterestDate          | 付息日                                                                                                                                                                                                                                                                | string(date-time)         |                            |
| preClose                  | 昨收价                                                                                                                                                                                                                                                                | number                    |                            |
| preMarketValue            | 昨日市值                                                                                                                                                                                                                                                              | number                    |                            |
| preTodayProfit            | T-1 今日盈亏 只有在夜盘交易才有值                                                                                                                                                                                                                                     | number                    |                            |
| sessionType               | 市场状态: 0-正常 1-盘前 2-盘后。期权没有盘前盘后                                                                                                                                                                                                                      | integer(int32)            |                            |
| shortMarginValue          | 空头保证金                                                                                                                                                                                                                                                            | number                    |                            |
| todayDelta                | 今日变动值                                                                                                                                                                                                                                                            | number                    |                            |
| todayProfitDB             | 今日盈亏金额                                                                                                                                                                                                                                                          | number                    |                            |
| todayProfitVar            | 今日盈亏变量 0 或者 1，默认情况是 1                                                                                                                                                                                                                                   | integer(int32)            |                            |
| holdingProfit             | 持仓盈亏金额，基金为近7日收益                                                                                                                                                                                                                                         | number                    |                            |
| holdingProfitPercent      | 持仓盈亏率                                                                                                                                                                                                                                                            | number                    |                            |
| marketValue               | 证券市值                                                                                                                                                                                                                                                              | number                    |                            |
| moneyType                 | 币种类型 (0:人民币; 1:美元; 2:港币)                                                                                                                                                                                                                                   | integer(int32)            |                            |
| multiAssetBusinessType    | 资产业务类型 (11:港股; 12:港股日内融; 21:美股; 22:美股日内融; 23:美股沽空; 24:美股碎股; 31:A股; 41:美股期权; 42:美股期权沽空; 50:基金; 52:港币基金; 53:美元基金; 60:债券; 61:港币债券; 62:美元债券; 70:资管账户; 80:统一财富; 81:统一财富-港元; 82:统一财富-美元)     | integer(int32)            |                            |
| mvLevelDesc               | 风险等级描述                                                                                                                                                                                                                                                          | string                    |                            |
| mvRate                    | 风险比率Sum(MM)/ELV                                                                                                                                                                                                                                                   | number                    |                            |
| newTodayProfit            | 今日盈亏金额                                                                                                                                                                                                                                                          | number                    |                            |
| num                       | 持仓数量                                                                                                                                                                                                                                                              | integer(int32)            |                            |
| processBalance            |                                                                                                                                                                                                                                                                       | number                    |                            |
| purchasePower             | 购买力                                                                                                                                                                                                                                                                | number                    |                            |
| realFundAccountType       | 账户类型 (0:普通账户; 2:margin账户; 4:跟投账户; 6:碎股账户; 10:DA账户; 11:MA公共账户; 12:MA费用账户; 20:日内融账户; 30:期权账户; 31:期权沽空账户; 40:沽空账户; 50:统一理财账户; 51:基金账户; 52:Cash+账户; 60:债券账户; 61:债券账户V2)                                | integer(int32)            |                            |
| riskStatusCode            | 风控状态CODE                                                                                                                                                                                                                                                          | integer(int32)            |                            |
| todayProfit               | 今日盈亏金额                                                                                                                                                                                                                                                          | number                    |                            |
| followAssetHomePageRespVO | 跟投账户资产                                                                                                                                                                                                                                                          | FollowAssetHomePageRespVO | FollowAssetHomePageRespVO  |
| asset                     | 总资产                                                                                                                                                                                                                                                                | number                    |                            |
| cashBalance               | 现金资产                                                                                                                                                                                                                                                              | number                    |                            |
| fundAccountStatus         | 账户状态,1已开通，2未开通                                                                                                                                                                                                                                             | integer(int32)            |                            |
| marketValue               | 跟投账户市值                                                                                                                                                                                                                                                          | number                    |                            |
| moneyType                 | 币种                                                                                                                                                                                                                                                                  | integer(int32)            |                            |
| totalAssetValue           | 净资产                                                                                                                                                                                                                                                                | number                    |                            |
| totalCashBalance          | 账户现金余额                                                                                                                                                                                                                                                          | number                    |                            |
| totalMarketValue          | 证券市值                                                                                                                                                                                                                                                              | number                    |                            |
| userId                    | 用户uuid                                                                                                                                                                                                                                                              | integer(int64)            |                            |
| userIdShort               | 用户短id                                                                                                                                                                                                                                                              | integer(int64)            |                            |
| error                     | 错误详情                                                                                                                                                                                                                                                              | string                    |                            |
| msg                       | 状态信息                                                                                                                                                                                                                                                              | string                    |                            |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  
  "msg": "成功",
  
  "data": {
    "assetSingleInfoRespVOS": [
      {
        "asset": "135692954.88",
        "availableBalance": "19823466.67",
        "borrowAmount": "0.00",
        "cashBalance": "19925810.88",
        "cashFundAsset": "0.0000",
        "costBalance": "0.00",
        "dueInterest": "0.00",
        "frozenBalance": "102344.2100",
        "fundAccount": "80019614",
        "fundAccountStatus": 1,
        "fundAccountType": 2,
        "fundAsset": "0.0000",
        "holdInfos": [
          {
            "businessType": "",
            "code": "12345",
            "costBalance": "0.000",
            "costPrice": "5.000",
            "curHoldNum": "1000.0000",
            "exchangeType": 0,
            "fundAccountType": 2,
            "holdProfit": "-5000.00",
            "holdProfitPercent": "-1.0000",
            "holdProfitVar": 0,
            "id": "1460715989705072640",
            "isinOrCusip": "",
            "marketValue": "0.00",
            "name": "MBVANKE@EC2207A",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "0.000",
            "preMarketValue": "0.000",
            "sessionType": 0,
            "shortMarginValue": "0.00",
            "todayDelta": "5000.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 1
          },
          {
            "businessType": "",
            "code": "00981",
            "costBalance": "0.000",
            "costPrice": "44.200",
            "curHoldNum": "500.0000",
            "exchangeType": 0,
            "fundAccountType": 2,
            "holdProfit": "3475.00",
            "holdProfitPercent": "0.1572",
            "holdProfitVar": 0,
            "id": "1459679191809671168",
            "isinOrCusip": "",
            "marketValue": "25575.00",
            "name": "中芯国际",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "48.700",
            "preMarketValue": "0.000",
            "sessionType": 0,
            "shortMarginValue": "0.00",
            "todayDelta": "22100.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 1
          },
          {
            "businessType": "",
            "code": "03690",
            "costBalance": "0.000",
            "costPrice": "250.000",
            "curHoldNum": "300.0000",
            "exchangeType": 0,
            "fundAccountType": 2,
            "holdProfit": "-39150.00",
            "holdProfitPercent": "-0.5220",
            "holdProfitVar": 0,
            "id": "1443018584197681152",
            "isinOrCusip": "",
            "marketValue": "35850.00",
            "name": "美团-W",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "119.200",
            "preMarketValue": "0.000",
            "sessionType": 0,
            "shortMarginValue": "0.00",
            "todayDelta": "75000.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 1
          },
          {
            "businessType": "",
            "code": "00700",
            "costBalance": "0.000",
            "costPrice": "499.024",
            "curHoldNum": "206802.0000",
            "exchangeType": 0,
            "fundAccountType": 2,
            "holdProfit": "12506557.75",
            "holdProfitPercent": "0.1212",
            "holdProfitVar": 0,
            "id": "1373427112588980224",
            "isinOrCusip": "",
            "marketValue": "115705719.00",
            "name": "腾讯控股",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "561.000",
            "preMarketValue": "0.000",
            "sessionType": 0,
            "shortMarginValue": "0.00",
            "todayDelta": "103199422.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 1
          }
        ],
        "holdingProfit": "12465882.75",
        "marketValue": "115767144.00",
        "moneyType": 2,
        "multiAssetBusinessType": 11,
        "mvLevelDesc": "安全",
        "mvRate": "0.0001",
        "newTodayProfit": "12465622.00",
        "num": 4,
        "processBalance": "0.00",
        "purchasePower": "915794381.56",
        "riskStatusCode": 1,
        "todayProfit": "12465622.00"
      },
      {
        "asset": "230122099.88",
        "availableBalance": "113581566.23",
        "borrowAmount": "0.00",
        "cashBalance": "113600146.66",
        "cashFundAsset": "0.0000",
        "costBalance": "0.00",
        "dueInterest": "0.00",
        "frozenBalance": "5684.8000",
        "fundAccount": "80019614",
        "fundAccountStatus": 1,
        "fundAccountType": 2,
        "fundAsset": "0.0000",
        "holdInfos": [
          {
            "businessType": "",
            "code": "JD",
            "costBalance": "0.000",
            "costPrice": "1.100",
            "curHoldNum": "10000.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "361700.00",
            "holdProfitPercent": "32.8818",
            "holdProfitVar": 0,
            "id": "1458325385658253312",
            "isinOrCusip": "",
            "marketValue": "372700.00",
            "name": "JD",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "37.270",
            "preMarketValue": "372700.000",
            "preTodayProfit": "361700.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "361700.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "BABA",
            "costBalance": "0.000",
            "costPrice": "80.000",
            "curHoldNum": "3.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "116.73",
            "holdProfitPercent": "0.4864",
            "holdProfitVar": 0,
            "id": "1313020606410870784",
            "isinOrCusip": "",
            "marketValue": "356.73",
            "name": "阿里巴巴",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "114.750",
            "preMarketValue": "344.910",
            "preTodayProfit": "0.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "PHUN",
            "costBalance": "0.000",
            "costPrice": "0.050",
            "curHoldNum": "5.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "21.65",
            "holdProfitPercent": "86.6000",
            "holdProfitVar": 0,
            "id": "1252174505539964928",
            "isinOrCusip": "",
            "marketValue": "21.90",
            "name": "Phunware, Inc.",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "4.380",
            "preMarketValue": "21.900",
            "preTodayProfit": "0.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "AAPL",
            "costBalance": "0.000",
            "costPrice": "4.075",
            "curHoldNum": "164442.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "36618766.77",
            "holdProfitPercent": "54.6466",
            "holdProfitVar": 0,
            "id": "1252141968369291264",
            "isinOrCusip": "",
            "marketValue": "37288867.92",
            "name": "APPLE INC",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "229.090",
            "preMarketValue": "37357933.560",
            "preTodayProfit": "4670152.800",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "4670152.800",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "PBTS",
            "costBalance": "0.000",
            "costPrice": "0.000",
            "curHoldNum": "10000000.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "0.00",
            "holdProfitPercent": "0.0000",
            "holdProfitVar": 0,
            "id": "1003044837984915456",
            "isinOrCusip": "",
            "marketValue": "0.00",
            "name": "",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "0.000",
            "preMarketValue": "0.000",
            "preTodayProfit": "0.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "IMTE",
            "costBalance": "0.000",
            "costPrice": "0.000",
            "curHoldNum": "10000000.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "12200000.00",
            "holdProfitPercent": "1.0000",
            "holdProfitVar": 0,
            "id": "1003044820297535488",
            "isinOrCusip": "",
            "marketValue": "12200000.00",
            "name": "Integrated Media Technology Ltd.",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "1.220",
            "preMarketValue": "12200000.000",
            "preTodayProfit": "0.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "",
            "code": "AMD",
            "costBalance": "0.000",
            "costPrice": "0.000",
            "curHoldNum": "10000001.0000",
            "exchangeType": 5,
            "fundAccountType": 2,
            "holdProfit": "66660006.67",
            "holdProfitPercent": "1.0000",
            "holdProfitVar": 0,
            "id": "932459313663533056",
            "isinOrCusip": "",
            "marketValue": "66660006.67",
            "name": "美国超威",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "6.666",
            "preMarketValue": "66660006.666",
            "preTodayProfit": "0.000",
            "sessionType": 20,
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          }
        ],
        "holdingProfit": "115840611.82",
        "marketValue": "116521953.22",
        "moneyType": 1,
        "multiAssetBusinessType": 21,
        "mvLevelDesc": "安全",
        "mvRate": "0.0001",
        "newTodayProfit": "-69053.82",
        "num": 7,
        "processBalance": "0.00",
        "purchasePower": "117366016.14",
        "riskStatusCode": 1,
        "todayProfit": "5031852.80"
      },
      {
        "asset": "72276.00",
        "availableBalance": "0.00",
        "borrowAmount": "0.00",
        "cashBalance": "0.00",
        "cashFundAsset": "0.0000",
        "costBalance": "0.00",
        "dueInterest": "0.00",
        "frozenBalance": "0.0000",
        "fundAccount": "77000287",
        "fundAccountStatus": 1,
        "fundAccountType": 30,
        "fundAsset": "0.0000",
        "holdInfos": [
          {
            "businessType": "0",
            "code": "AAPL250815C90000",
            "costBalance": "0.000",
            "costPrice": "3.527",
            "curHoldNum": "3.0000",
            "exchangeType": 51,
            "fundAccountType": 30,
            "holdProfitVar": 1,
            "id": "1472396064037044224",
            "isinOrCusip": "",
            "marketValue": "41286.00",
            "multiplier": "100.00",
            "name": "AAPL 250815 90.0 C",
            "newHoldProfitVar": 1,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 0,
            "preClose": "3.527",
            "preMarketValue": "0.000",
            "shortMarginValue": "0.00",
            "todayDelta": "1058.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "0",
            "code": "NVDA250815P220000",
            "costBalance": "0.000",
            "costPrice": "4.560",
            "curHoldNum": "2.0000",
            "exchangeType": 51,
            "fundAccountType": 30,
            "holdProfitVar": 1,
            "id": "1472390112235782144",
            "isinOrCusip": "",
            "marketValue": "20430.00",
            "multiplier": "100.00",
            "name": "NVDA 250815 220.0 P",
            "newHoldProfitVar": 1,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 0,
            "preClose": "4.560",
            "preMarketValue": "0.000",
            "shortMarginValue": "0.00",
            "todayDelta": "912.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          },
          {
            "businessType": "0",
            "code": "QQQ260116C520000",
            "costBalance": "0.000",
            "costPrice": "11.000",
            "curHoldNum": "11.0000",
            "exchangeType": 51,
            "fundAccountType": 30,
            "holdProfitVar": 0,
            "id": "1470143648579194880",
            "isinOrCusip": "",
            "marketValue": "19800.00",
            "multiplier": "100.00",
            "name": "QQQ 260116 520.0 C",
            "newHoldProfitVar": 0,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 1,
            "preClose": "18.750",
            "preMarketValue": "19800.000",
            "shortMarginValue": "0.00",
            "todayDelta": "0.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 1
          },
          {
            "businessType": "OS",
            "code": "AA250919P60000",
            "costBalance": "0.000",
            "costPrice": "20.648",
            "curHoldNum": "-4.0000",
            "exchangeType": 51,
            "fundAccountType": 31,
            "holdProfitVar": 1,
            "id": "1472397925452382208",
            "isinOrCusip": "",
            "marketValue": "-9240.00",
            "multiplier": "100.00",
            "name": "AA 250919 60.0 P",
            "newHoldProfitVar": 1,
            "newTodayProfitDB": "0.000",
            "newTodayProfitVar": 0,
            "preClose": "20.648",
            "preMarketValue": "0.000",
            "shortMarginValue": "0.00",
            "todayDelta": "-8259.000",
            "todayProfitDB": "0.000",
            "todayProfitVar": 0
          }
        ],
        "holdingProfit": "67446.00",
        "holdingProfitPercent": "4.7936",
        "marketValue": "72276.00",
        "moneyType": 1,
        "multiAssetBusinessType": 41,
        "mvLevelDesc": "",
        "newTodayProfit": "59746.00",
        "num": 4,
        "processBalance": "0.00",
        "purchasePower": "117366016.14",
        "todayProfit": "59746.00"
      },
      {
        "asset": "0.00",
        "availableBalance": "0.00",
        "borrowAmount": "0.00",
        "cashBalance": "0.00",
        "cashFundAsset": "0.0000",
        "costBalance": "0.00",
        "dueInterest": "0.00",
        "frozenBalance": "0.0000",
        "fundAccount": "80019614",
        "fundAccountStatus": 1,
        "fundAccountType": 2,
        "fundAsset": "0.0000",
        "holdInfos": [

        ],
        "holdingProfit": "0.00",
        "marketValue": "0.00",
        "moneyType": 0,
        "multiAssetBusinessType": 31,
        "mvLevelDesc": "安全",
        "mvRate": "0.0001",
        "newTodayProfit": "0.00",
        "num": 0,
        "processBalance": "0.00",
        "purchasePower": "833822185.35",
        "riskStatusCode": 1,
        "todayProfit": "0.00"
      }
    ],
    "moneyType": 1,
    "totalAssetValue": "248386394.00",
    "totalCashBalance": "117134233.07",
    "totalMarketValue": "131252160.94",
    "userId": "390501763164413952",
    "userIdShort": "2994"
  }
}
```

</div>

### 2.12获取融资股数

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/trade-margin-quantity`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/trade-margin-quantity`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 获取融资股数

-   请求示例

<div class="language-json extra-class">

``` language-json
{

  "entrustAmount": 1,

  "entrustId": 1,

  "entrustPrice": 1,

  "entrustProp": "",

  "entrustType": 1,

  "exchangeType": 1,

  "stockCode": ""

}
```

</div>

-   请求参数

| 参数名称      | 参数说明                                                                       | 请求类型 | 是否必须 | 数据类型 |
|---------------|--------------------------------------------------------------------------------|----------|----------|----------|
| Authorization | 头部信息的token信息                                                            | header   | true     | string   |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                            | header   | true     | string   |
| X-Channel     | 渠道ID，由盈立分配                                                             | header   | true     | string   |
| X-Time        | 时间戳                                                                         | header   | true     | string   |
| X-Sign        | RSA签名                                                                        | header   | true     | string   |
| entrustAmount | 委托数量                                                                       | body     | true     | number   |
| entrustProp   | 委托属性('0'-美股限价单,'d'-竞价单,'e' -增强限价单,'g'-竞价限价单，'u'-碎股单) | body     | true     | string   |
| exchangeType  | 交易类别(0-香港,5-美股,6-沪港通,7-深港通)                                      | body     | true     | int32    |
| stockCode     | 证券代码                                                                       | body     | true     | string   |
| entrustId     | 委托Id-如果entrystType是改单的话，必填                                         | body     | false    | int64    |
| entrustPrice  | 委托价格(不能为0,竞价单可不填)                                                 | body     | false    | number   |
| entrustType   | 查询委托类别(0-买，5-改单)                                                     | body     | false    | int32    |

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 0      | 成功         |
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数：

| 参数名称            | 参数说明                 | 类型           |
|---------------------|--------------------------|----------------|
| code                | 状态码                   | integer(int32) |
| data                | 返回体                   |                |
| cashEnableAmount    | 此订单使用的现金可买数量 | number         |
| cashEnableBalance   | 此订单使用的可买现金     | number         |
| cashMaxEnableAmount | 最大使用的现金可买数量   | number         |
| marginAmount        | 融资股数                 | number         |
| marginBalance       | 融资金额                 | number         |
| msg                 | 状态信息                 | string         |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

 "code": 0,

 "msg": "操作成功",

 "data": {

   "saleEnableAmount": 0.00,

   "saleEnableIntAmount": 0.0000,

   "oddEnableAmount": 0.0000,

   "buyEnableAmount": 6000.00,

   "handAmount": 100.0000,

   "cashEnableAmount": 2931,

   "cashEnableIntAmount": 2900.0000,

   "cashPurchasingPower": 983164.00,

   "maxPurchasingPower": 2026893.26,

   "fundAccoutType": "M"

 }

}
```

</div>

### 2.13客户融资账户详情

-   生产环境接口地址 `https://open-jy.yxzq.com/asset-center-server/open-api/open-margin-detail/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/asset-center-server/open-api/open-margin-detail/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 需要资金账号

-   请求示例

<div class="language-json extra-class">

``` language-json
{

  "exchangeType": 0

}
```

</div>

-   请求参数

| 参数名称      | 参数说明                            | 请求类型 | 是否必须 | 数据类型 |
|---------------|-------------------------------------|----------|----------|----------|
| Authorization | 头部信息的token信息                 | header   | true     | string   |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true     | string   |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true     | string   |
| X-Request-Id  | 头部信息的requestId信息             | header   | true     | string   |
| X-Sign        | RSA签名                             | header   | true     | string   |
| X-Type        | APP类别(1-大陆版，2-港版)           | header   | true     | string   |
| exchangeType  | 交易类别，0港股，5美股              | body     | true     | int32    |

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 0      | 成功         |
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数

| 参数名称                   | 参数说明                             | 类型                         | schema                       |
|----------------------------|--------------------------------------|------------------------------|------------------------------|
| code                       | 状态码                               | integer(int32)               | integer(int32)               |
| data                       | 返回体                               | AccountMarginDetailAppRespVO | AccountMarginDetailAppRespVO |
| anticipatedInterest        | 预计利息                             | number                       |                              |
| asset                      | 净资产                               | number                       |                              |
| availableBalance           | 可用金额                             | number                       |                              |
| callMarginCall             | 追缴保证金                           | number                       |                              |
| cashBalance                | 现金余额                             | number                       |                              |
| cashPurchasePower          | 现金购买力                           | number                       |                              |
| cnhAccount                 | A股市场账户                          | string                       |                              |
| creditAmount               | 信用额度                             | number                       |                              |
| creditRatio                | 信用比率                             | number                       |                              |
| crossDebitBalance          | 总负债金额SGD                        | number                       |                              |
| crossMarginValue           | 总抵押市值                           | number                       |                              |
| crossMarketValue           | 跨市场总市值                         | number                       |                              |
| debitBalance               | 负债金额                             | number                       |                              |
| debitHairCut               | 总负债hairCut                        | number                       |                              |
| frozenBalance              | 冻结金额                             | number                       |                              |
| hkdAccount                 | 港股市场账户                         | string                       |                              |
| holdMarketValueHairCut     | 股票市值Haircut（多头）              | number                       |                              |
| longStockMarketValue       | 美股证券市值（多头）                 | number                       |                              |
| marginRatioYear            | 融资利率年                           | string                       |                              |
| marketValue                | 股票市值                             | number                       |                              |
| mv                         | mv%                                  | number                       |                              |
| onWayBalance               | 在途资金                             | number                       |                              |
| penaltyCouponBalance       | 融券利息                             | number                       |                              |
| purchasePower              | 最大购买力                           | number                       |                              |
| riskStatusCode             | 风控水平CODE                         | integer(int32)               |                              |
| riskStatusName             | 风控水平名称                         | string                       |                              |
| shortMarketValue           | 股票做空市值                         | number                       |                              |
| shortMarketValueHaircut    | 融券市值(Haircut)                    | number                       |                              |
| shortOptionKeepMarginValue | 期权沽空维持保证金                   | number                       |                              |
| shortOptionMarginValue     | 期权沽空保证金                       | number                       |                              |
| shortStockMarginValue      | 美股空头保证金                       | number                       |                              |
| shortStockMarketValue      | 美股证券市值（空头）                 | number                       |                              |
| stockDebit                 | 融券金额 融券市值=卖空股票市值绝对值 | number                       |                              |
| totalTradeAmount           | 总交易额度                           | number                       |                              |
| usdAccount                 | 美股市场账户                         | string                       |                              |
| usePvhc                    | 使用pvhc风控                         | boolean                      |                              |
| withdrawBalance            | 可取现金                             | number                       |                              |
| error                      | 错误详情                             | string                       |                              |
| msg                        | 状态信息                             | string                       |                              |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  
  "msg": "成功",
  
  "data": {
    
    "anticipatedInterest": "0.00",
    
    "asset": "135692924.88",
    
    "availableBalance": "19823466.67",
    
    "callMarginCall": "0.00",
    
    "cashBalance": "19925810.88",
    
    "cashPurchasePower": "905759683.26",
    
    "cnhAccount": "80019614",
    
    "creditAmount": "10000000.00",
    
    "creditRatio": "1.0000",
    
    "crossDebitBalance": "72072.00",
    
    "crossMarginValue": "181876274.11",
    
    "crossMarketValue": "1024317594.99",
    
    "debitBalance": "0.00",
    
    "debitHairCut": "83974.25",
    
    "frozenBalance": "102344.21",
    
    "hkdAccount": "80019614",
    
    "holdMarketValueHairCut": "229803759.74",
    
    "longStockMarketValue": "115767114.00",
    
    "marginRatioYear": "6.50%",
    
    "marketValue": "115767114.00",
    
    "mv": "0.0001",
    
    "onWayBalance": "0.00",
    
    "penaltyCouponBalance": "0.00",
    
    "purchasePower": "915794381.56",
    
    "riskStatusCode": 1,
    
    "riskStatusName": "安全",
    
    "shortMarketValue": "0.00",
    
    "shortMarketValueHaircut": "0.00",
    
    "shortOptionKeepMarginValue": "83974.25",
    
    "shortOptionMarginValue": "101173.80",
    
    "shortStockMarginValue": "0.00",
    
    "shortStockMarketValue": "0.00",
    
    "totalTradAmount": "0.00",
    
    "usdAccount": "80019614",
    
    
    "usePvhc": true,
    
    "withdrawBalance": "19823466.67",
    
  }
}
```

</div>

## **3** IPO认购

### 3.1获取IPO列表-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/ipo-list`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/ipo-list`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 获取IPO列表（不需要登录）

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填  | 类型   |
|---------------|-------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                 | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true  | string |
| X-Channel     | 渠道                                | header   | true  | string |
| X-Time        | 时间戳                              | header   | true  | string |
| X-Sign        | RSA签名                             | header   | true  | string |
| status        | Tab页类别(0-认购中，1-待上市)       | body     | true  | int32  |
| pageNum       | 当前页 1开始, 默认值1               | body     | false | int32  |
| pageSize      | 每页结果数, 默认值10                | body     | false | int32  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "pageNum": 1,

    "pageSize": 10,

    "status": 1

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                        |
|--------|--------------|-----------------------------------------------|
| 200    | OK           | ResponseVO«PageInfoVO«AppGetIpoListResponse»» |
| 201    | Created      |                                               |
| 401    | Unauthorized |                                               |
| 403    | Forbidden    |                                               |
| 404    | Not Found    |                                               |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«OpenApiGetIpoListResponse»</td><td>PageInfoVO«OpenApiGetIpoListResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>OpenApiGetIpoListResponse</td></tr><tr class="even"><td>bookingRatio</td><td>认购倍数</td><td>number</td><td></td></tr><tr class="odd"><td>endTime</td><td>现金认购结束时间yyyy-MM-dd HH:mm:ss</td><td>string</td><td></td></tr><tr class="even"><td>englishName</td><td>新股英文名</td><td>string</td><td></td></tr><tr class="odd"><td>exchangeType</td><td>市场类型(0-港股)</td><td>int32</td><td></td></tr><tr class="even"><td>financingEndTime</td><td>融资认购结束时间</td><td>string</td><td></td></tr><tr class="odd"><td>financingMultiple</td><td>融资倍数</td><td>int32</td><td></td></tr><tr class="even"><td>ipoId</td><td>IPO id</td><td>string</td><td></td></tr><tr class="odd"><td>labelStatus</td><td>标签状态(0-已认购,1-已中签,2-未中签)</td><td>int32</td><td></td></tr><tr class="even"><td>latestEndtime</td><td>最晚认购截止时间(国际认购、融资认购和现金认购截止时间最晚的时间)</td><td>string</td><td></td></tr><tr class="odd"><td>leastAmount</td><td>起购金额</td><td>number</td><td></td></tr><tr class="even"><td>listingPrice</td><td>最终上市价格</td><td>number</td><td></td></tr><tr class="odd"><td>listingTime</td><td>上市交易时间</td><td>string</td><td></td></tr><tr class="even"><td>moneyType</td><td>币种类型(0-人民币，1-美元，2-港币)</td><td>int32</td><td></td></tr><tr class="odd"><td>priceMax</td><td>最高招股价</td><td>number</td><td></td></tr><tr class="even"><td>priceMin</td><td>最低招股价</td><td>number</td><td></td></tr><tr class="odd"><td>publishTime</td><td>公布中签日期</td><td>string</td><td></td></tr><tr class="even"><td>remainingTime</td><td>认购剩余时间（秒）</td><td>int64</td><td></td></tr><tr class="odd"><td>serverTime</td><td>服务器时间</td><td>string</td><td></td></tr><tr class="even"><td>status</td><td>新股状态(0-待认购，1-认购中，2-待扣款，3-已扣款待确认，4-已确认待公布，5-已公布待上市，6-已上市，7-取消上市，8-暂缓上市，9-延迟上市)</td><td>int32</td><td></td></tr><tr class="odd"><td>statusName</td><td>状态中文名</td><td>string</td><td></td></tr><tr class="even"><td>stockCode</td><td>新股代码</td><td>string</td><td></td></tr><tr class="odd"><td>stockName</td><td>新股名称</td><td>string</td><td></td></tr><tr class="even"><td>subscribeWay</td><td>认购方式，多种认购用,隔开，比如0,1 支持现金和融资(1-公开现金认购，2-公开融资认购，3-国际配售)-这个字段可以判断是否支持融资认购</td><td>string</td><td></td></tr><tr class="odd"><td>successRate</td><td>中签率</td><td>number</td><td></td></tr><tr class="even"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="odd"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="even"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td></td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
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

                "status": 1,

                "statusName": "认购中",

                "stockName": "中国黄金国际",

                "englishName": "CHINAGOLDINTL",

                "leastAmount": null,

                "priceMin": 7,

                "priceMax": 11,

                "listingPrice": 10,

                "endTime": "2019-06-27",

                "financingEndTime": null,

                "latestEndtime": "2019-06-27",

                "remainingTime": -1,

                "labelStatus": null,

                "successRate": null,

                "bookingRatio": null,

                "publishTime": "2019-07-01",

                "listingTime": "2019-07-02",

                "moneyType": 2,

                "serverTime": "2019-10-09 21:08:21",

                "subscribeWay": "1",

                "financingMultiple": 3

            },

            {

                "ipoId": "1133576191818039296",

                "stockCode": "00994",

                "exchangeType": 0,

                "status": 1,

                "statusName": "认购中",

                "stockName": "中天宏信",

                "englishName": "CT VISION",

                "leastAmount": null,

                "priceMin": 7,

                "priceMax": 10,

                "listingPrice": 9,

                "endTime": "2019-07-29",

                "financingEndTime": null,

                "latestEndtime": "2019-07-29",

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
```

</div>

### 3.2获取新股详细信息

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/ipo-info`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/ipo-info`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 获取新股详细信息

-   请求参数

| 参数名称      | 说明                                                                                                             | 请求类型 | 必填  | 类型   |
|---------------|------------------------------------------------------------------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                                                                              | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                                                              | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                                                                               | header   | true  | string |
| X-Time        | 时间戳                                                                                                           | header   | true  | string |
| X-Sign        | RSA签名                                                                                                          | header   | true  | string |
| exchangeType  | 市场类型(0-HK,5-US),如果ipoId不传，该字段必传                                                                    | body     | false | int32  |
| ipoId         | 新股id \[与(stockCode&exchangeType不能同时为空)\],当ipoId有值，优先取ipoId查询，stockCode&exchangeType条件不生效 | body     | false | int64  |
| stockCode     | 股票代码,如果ipoId不传，该字段必传                                                                               | body     | false | string |

-   响应状态

| 状态码 | 说明         | schema                         |
|--------|--------------|--------------------------------|
| 200    | OK           | ResponseVO«appIpoInfoResponse» |
| 201    | Created      |                                |
| 401    | Unauthorized |                                |
| 403    | Forbidden    |                                |
| 404    | Not Found    |                                |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "ipoId": 1133576191528632320

}
```

</div>

-   响应参数

| 参数名称                 | 说明                                                                                                                                                                                                                    | 类型               | schema             |
|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------|--------------------|
| code                     | 状态码                                                                                                                                                                                                                  | int32              |                    |
| data                     | 返回体                                                                                                                                                                                                                  | appIpoInfoResponse | appIpoInfoResponse |
| applied                  | 用户是否已认购                                                                                                                                                                                                          | boolean            |                    |
| beginTime                | 现金认购开始时间                                                                                                                                                                                                        | string             |                    |
| bookingFee               | 现金认购手续费                                                                                                                                                                                                          | number             |                    |
| bookingRatio             | 认购倍数                                                                                                                                                                                                                | number             |                    |
| compFinancingSurplus     | 公司融资额度净余                                                                                                                                                                                                        | number             |                    |
| depositRate              | 融资比例                                                                                                                                                                                                                | number             |                    |
| ecmEndTime               | 国际认购截止时间                                                                                                                                                                                                        | date-time          |                    |
| ecmStatus                | ecm新股状态(0-待认购,1-认购中，2-待扣款，3-待扣款\[未全部扣款成功\]，4-待提交，5-待分配，6-待返款，7-待返款\[未全部返款成功\]，8-待返券，9-待返券\[未全部返券成功\]，10-待CCASS确认，11-待上市，12-已上市，13-暂停认购) | int32              |                    |
| endTime                  | 现金认购结束时间                                                                                                                                                                                                        | string             |                    |
| englishName              | 新股英文名                                                                                                                                                                                                              | string             |                    |
| exchangeType             | 交易类别(0-HK,5-US)                                                                                                                                                                                                     | int32              |                    |
| exchangeTypeName         | 交易类别名称                                                                                                                                                                                                            | string             |                    |
| financingEndTime         | 融资认购截止时间                                                                                                                                                                                                        | date-time          |                    |
| financingFee             | 融资手续费                                                                                                                                                                                                              | number             |                    |
| financingMultiple        | 融资倍数                                                                                                                                                                                                                | int32              |                    |
| financingTips            | 融资认购温馨提示                                                                                                                                                                                                        | string             |                    |
| greyFlag                 | 是否支持暗盘（0-不支持，1-支持）                                                                                                                                                                                        | int32              |                    |
| greyTimeBegin            | 暗盘交易时间段开始，格式 HH:mm:ss                                                                                                                                                                                       | string             |                    |
| greyTimeEnd              | 暗盘交易时间段结束，格式 HH:mm:ss                                                                                                                                                                                       | string             |                    |
| greyTradeDate            | 暗盘交易日，格式 yyyy-MM-dd                                                                                                                                                                                             | string             |                    |
| handAmount               | 每手股数                                                                                                                                                                                                                | number             |                    |
| interestBeginDate        | 融资认购/计息开始时间                                                                                                                                                                                                   | date-time          |                    |
| interestDay              | 计息天数                                                                                                                                                                                                                | int32              |                    |
| interestEndDate          | 融资计息结束时间                                                                                                                                                                                                        | date-time          |                    |
| interestRate             | 默认融资利率                                                                                                                                                                                                            | number             |                    |
| ipoFinancingRatios       | 融资阶梯利率(json数组:\[{"financing\_amount\_begin":初始认购金额,"financing\_amount\_end":结束认购金额,"interest\_rate":利率,"exchange\_type":市场类型,"stock\_code":"新股代码"}\])                                     | array              | IpoFinancingRatio  |
| exchange\_type           | 市场类型                                                                                                                                                                                                                | int32              |                    |
| financing\_amount\_begin | 初始认购金额                                                                                                                                                                                                            | number             |                    |
| financing\_amount\_end   | 结束认购金额                                                                                                                                                                                                            | number             |                    |
| interest\_rate           | 利率                                                                                                                                                                                                                    | number             |                    |
| stock\_code              | 新股代码                                                                                                                                                                                                                | string             |                    |
| ipoId                    | IPO id                                                                                                                                                                                                                  | string             |                    |
| latestEndtime            | 最晚认购截止时间(国际认购、融资认购和现金认购截止时间最晚的时间)                                                                                                                                                        | string             |                    |
| leastAmount              | 起购金额(一手认购金额)                                                                                                                                                                                                  | number             |                    |
| listingPrice             | 最终上市价格                                                                                                                                                                                                            | number             |                    |
| listingTime              | 上市交易时间                                                                                                                                                                                                            | string             |                    |
| marketValueMax           | 市值最大值                                                                                                                                                                                                              | number             |                    |
| marketValueMin           | 市值最小值                                                                                                                                                                                                              | number             |                    |
| moneyType                | 币种类型(0-人民币，1-美元，2-港币)                                                                                                                                                                                      | int32              |                    |
| officialBegin            | 官方招股开始时间                                                                                                                                                                                                        | string             |                    |
| officialEnd              | 官方招股结束时间                                                                                                                                                                                                        | string             |                    |
| priceMax                 | 最高招股价                                                                                                                                                                                                              | number             |                    |
| priceMin                 | 最低招股价                                                                                                                                                                                                              | number             |                    |
| prospectusLink           | 招股书链接                                                                                                                                                                                                              | string             |                    |
| publishQuantity          | 发行股本                                                                                                                                                                                                                | number             |                    |
| publishTime              | 公布中签日期                                                                                                                                                                                                            | string             |                    |
| qtyAndCharges            | 档位信息(json数组:\[{"allotted\_amount":中签金额,"applied\_amount":申购金额,"exchange\_type":市场类型,"shared\_applied":申购数量,"stock\_code":"新股代码"," leastCash ":档位对应的最少使用现金}\])                      | array              | IpoQtyAndCharges   |
| allotted\_amount         | 中签金额                                                                                                                                                                                                                | number             |                    |
| applied\_amount          | 申购金额                                                                                                                                                                                                                | number             |                    |
| exchange\_type           | 市场类型                                                                                                                                                                                                                | int32              |                    |
| leastCash                | 档位对应的最少使用现金                                                                                                                                                                                                  | int32              |                    |
| shared\_applied          | 申购数量                                                                                                                                                                                                                | number             |                    |
| stock\_code              | 新股代码                                                                                                                                                                                                                | string             |                    |
| remainingTime            | 认购剩余时间（秒）                                                                                                                                                                                                      | int64              |                    |
| serverTime               | 服务器时间                                                                                                                                                                                                              | string             |                    |
| sponsor                  | 保荐人                                                                                                                                                                                                                  | string             |                    |
| status                   | 新股状态(0-待认购，1-认购中，2-待扣款，3-已扣款待确认，4-已确认待公布，5-已公布待上市，6-已上市，7-取消上市，8-暂缓上市，9-延迟上市)                                                                                    | int32              |                    |
| statusName               | 状态中文名                                                                                                                                                                                                              | string             |                    |
| stockCode                | 新股代码                                                                                                                                                                                                                | string             |                    |
| stockIntroduction        | 股票介绍                                                                                                                                                                                                                | string             |                    |
| stockName                | 新股名称                                                                                                                                                                                                                | string             |                    |
| subscribeWay             | 认购方式，多种认购用,隔开，比如1,2 支持现金和融资(1-公开现金认购，2-公开融资认购，3-国际配售)-这个字段可以判断是否支持融资认购                                                                                          | string             |                    |
| successRate              | 中签率                                                                                                                                                                                                                  | number             |                    |
| tips                     | 现金认购温馨提示                                                                                                                                                                                                        | string             |                    |
| totalQuantity            | 总股本                                                                                                                                                                                                                  | number             |                    |
| updateTime               | 更新时间                                                                                                                                                                                                                | string             |                    |
| msg                      | 状态信息                                                                                                                                                                                                                | string             |                    |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "ipoId": "1143834475048767488",

        "stockCode": "02099",

        "stockName": "中国黄金国际",

        "status": 1,

        "exchangeType": 0,

        "moneyType": 2,

        "handAmount": null,

        "bookingFee": 10,

        "beginTime": "2019-06-25 09:00:00",

        "endTime": "2019-06-27 12:00:00",

        "publishTime": "2019-07-01 00:00:00",

        "listingTime": "2019-07-02 00:00:00",

        "listingPrice": null,

        "priceMin": null,

        "priceMax": 11,

        "financingEndTime": null,

        "interestBeginDate": null,

        "interestEndDate": null,

        "officialBegin": "2019-06-25 09:00:00",

        "officialEnd": "2019-06-28 12:00:00",

        "leastAmount": null,

        "successRate": null,

        "bookingRatio": null,

        "sponsor": "",

        "publishQuantity": null,

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

                "stock_code": "2099",

                "exchange_type": 0,

                "financing_amount_begin": 10001,

                "financing_amount_end": 20000,

                "interest_rate": 0.7

            }

        ],

        "financingMultiple": 3,

        "depositRate": 0.7,

        "financingFee": null,

        "interestDay": 0,

        "interestRate": null,

        "compFinancingSurplus": null,

        "subscribeWay": "1"

    }

}
```

</div>

### 3.3ipo新股认购

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/apply-ipo`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/apply-ipo`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 ipo新股认购

-   请求参数

| 参数名称      | 说明                                                     | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                      | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true  | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true  | string |
| X-Channel     | 渠道                                                     | header   | true  | string |
| X-Time        | 时间戳                                                   | header   | true  | string |
| X-Sign        | RSA签名                                                  | header   | true  | string |
| applyQuantity | 认购数量                                                 | body     | true  | number |
| applyType     | 认购类型(1-现金，2-融资)                                 | body     | true  | int32  |
| ipoId         | ipo交易系统唯一编号                                      | body     | true  | int64  |
| serialNo      | 流水号，最长19位，确保唯一推荐雪花算法生成               | body     | true  | int64  |
| cash          | 认购现金(融资认购时必填)                                 | body     | false | number |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1Qi LCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密’; 
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "applyQuantity": 100,

    "applyType": 1,

    "cash": 0,

    "ipoId": 1133576191818039296,

    "serialNo": 1182189250463484234

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                       |
|--------|--------------|------------------------------|
| 200    | OK           | ResponseVO«IpoApplyResponse» |
| 201    | Created      |                              |
| 401    | Unauthorized |                              |
| 403    | Forbidden    |                              |
| 404    | Not Found    |                              |

-   响应参数

| 参数名称 | 说明                                                                                                                         | 类型             | schema           |
|----------|------------------------------------------------------------------------------------------------------------------------------|------------------|------------------|
| code     | 状态码                                                                                                                       | int32            |                  |
| data     | 返回体                                                                                                                       | IpoApplyResponse | IpoApplyResponse |
| applyId  | 申购id                                                                                                                       | string           |                  |
| status   | 申购状态(0-已提交,1-已认购,2-等待改单, 3-等待撤销,4-已撤销,5-已扣款,6-待公布中签,7-全部中签,8-部分中签,9-未中签,10-认购失败) | int32            |                  |
| msg      | 状态信息                                                                                                                     | string           |                  |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "applyId": "1182192040986583040",

        "status": 1

    }

}
```

</div>

### 3.4ipo改单/撤单

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/modify-ipo`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/modify-ipo`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 ipo改单/撤单

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                                  | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true  | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true  | string |
| X-Channel     | 渠道                                                                 | header   | true  | string |
| X-Time        | 时间戳                                                               | header   | true  | string |
| X-Sign        | RSA签名                                                              | header   | true  | string |
| actionType    | 操作类型 0-改单,1-撤单                                               | body     | true  | int32  |
| applyId       | 认购记录Id                                                           | body     | true  | int64  |
| applyQuantity | 认购数量                                                             | body     | true  | number |
| cash          | 认购现金(改融资认购单，必填)                                         | body     | false | number |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "actionType": 1,

    "applyId": 1182192040986583040,

    "applyQuantity": 0,

    "cash": 0

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                       |
|--------|--------------|------------------------------|
| 200    | OK           | ResponseVO«IpoApplyResponse» |
| 201    | Created      |                              |
| 401    | Unauthorized |                              |
| 403    | Forbidden    |                              |
| 404    | Not Found    |                              |

-   响应参数

| 参数名称 | 说明                                                                                                                         | 类型             | schema           |
|----------|------------------------------------------------------------------------------------------------------------------------------|------------------|------------------|
| code     | 状态码                                                                                                                       | int32            |                  |
| data     | 返回体                                                                                                                       | IpoApplyResponse | IpoApplyResponse |
| applyId  | 申购id                                                                                                                       | string           |                  |
| status   | 申购状态(0-已提交,1-已认购,2-等待改单, 3-等待撤销,4-已撤销,5-已扣款,6-待公布中签,7-全部中签,8-部分中签,9-未中签,10-认购失败) | int32            |                  |
| msg      | 状态信息                                                                                                                     | string           |                  |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "applyId": "1182192040986583040",

        "status": 4

    }

}
```

</div>

### 3.5获取客户ipo申购列表-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/ipo-record-list`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/ipo-record-list`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 获取客户ipo申购列表

-   请求参数

| 参数名称      | 说明                                   | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                    | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)    | header   | true  | string |
| X-Channel     | 渠道                                   | header   | true  | string |
| X-Time        | 时间戳                                 | header   | true  | string |
| X-Sign        | RSA签名                                | header   | true  | string |
| applyTimeMin  | 认购开始时间，格式:yyyy-MM-dd HH:mm:ss | body     | false | string |
| applyTimeMax  | 认购结束时间，格式:yyyy-MM-dd HH:mm:ss | body     | false | string |
| pageNum       | 当前页 1开始，默认值1                  | body     | false | int32  |
| pageSize      | 每页结果数，默认值10                   | body     | false | int32  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

<div class="language-json extra-class">

``` language-json
{

    "pageNum": 1,

    "pageSize": 10,

    "applyTimeMin": "2019-10-12 00:00:00",

    "applyTimeMax": "2020-01-30 00:00:00"

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                        |
|--------|--------------|-----------------------------------------------|
| 200    | OK           | ResponseVO«PageInfoVO«IpoRecordListResponse»» |
| 201    | Created      |                                               |
| 401    | Unauthorized |                                               |
| 403    | Forbidden    |                                               |
| 404    | Not Found    |                                               |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«IpoRecordListResponse»</td><td>PageInfoVO«IpoRecordListResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>IpoRecordListResponse</td></tr><tr class="even"><td>allottedQuantity</td><td>中签股数</td><td>number</td><td></td></tr><tr class="odd"><td>applyAmount</td><td>认购总金额(包含手续费，不包含利息)</td><td>number</td><td></td></tr><tr class="even"><td>applyId</td><td>申请编号</td><td>string</td><td></td></tr><tr class="odd"><td>applyQuantity</td><td>认购股数</td><td>number</td><td></td></tr><tr class="even"><td>applyType</td><td>认购类型(1-现金，2-融资)</td><td>int32</td><td></td></tr><tr class="odd"><td>applyTypeName</td><td>认购类型(1-现金认购，2-融资认购)</td><td>string</td><td></td></tr><tr class="even"><td>priceMax</td><td>最高招股价</td><td>number</td><td></td></tr><tr class="odd"><td>priceMin</td><td>最低招股价</td><td>number</td><td></td></tr><tr class="even"><td>listingPrice</td><td>最终上市价格</td><td>number</td><td></td></tr><tr class="odd"><td>cash</td><td>认购现金</td><td>number</td><td></td></tr><tr class="even"><td>exchangeType</td><td>市场类型(0-HK,5-US)</td><td>int32</td><td></td></tr><tr class="odd"><td>financingAmount</td><td>融资利息</td><td>number</td><td></td></tr><tr class="even"><td>financingBalance</td><td>融资金额</td><td>number</td><td></td></tr><tr class="odd"><td>interestRate</td><td>融资利率</td><td>number</td><td></td></tr><tr class="even"><td>labelCode</td><td>状态标签码(0-待系统确认,1-已认购,4-已撤销,6-待公布中签,7-已中签,9-未中签,10-认购失败)</td><td>int32</td><td></td></tr><tr class="odd"><td>moneyType</td><td>币种类型(0-人民币，1-美元，2-港币)</td><td>int32</td><td></td></tr><tr class="even"><td>publishTime</td><td>公布中签日期</td><td>string</td><td></td></tr><tr class="odd"><td>listingTime</td><td>上市交易时间(YYYY-MM-DD)</td><td></td><td></td></tr><tr class="even"><td>serverTime</td><td>服务器时间</td><td>string</td><td></td></tr><tr class="odd"><td>status</td><td>认购状态(0-已提交,1-已认购,2-等待改单, 3-等待撤销,4-已撤销,5-已扣款,6-待公布中签,7-全部中签,8-部分中签,9-未中签,10-认购失败)</td><td>int32</td><td></td></tr><tr class="even"><td>statusName</td><td>认购状态名称</td><td>string</td><td></td></tr><tr class="odd"><td>stockCode</td><td>股票代码</td><td>string</td><td></td></tr><tr class="even"><td>stockName</td><td>股票名称</td><td>string</td><td></td></tr><tr class="odd"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="even"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="odd"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{

    "code": 0,

    "msg": "操作成功",

    "data": {

        "pageNum": 1,

        "pageSize": 0,

        "total": 34,

        "list": [{

                "applyId": "1147036407112679424",

                "applyType": 2,

                "applyTypeName": "融资认购",

                "stockName": "香港中華煤氣",

                "stockCode": "00003",

                "exchangeType": 0,

                "status": 10,

                "statusName": "认购失败",

                "applyQuantity": 200,

                "applyAmount": 4140.31,

                "cash": null,

                "financingBalance": null,

                "interestRate": null,

                "priceMin": 10,

                "priceMax": 20,

                "listingPrice": 13,

                "financingAmount": 1.75,

                "allottedQuantity": 0,

                "publishTime": "2019-07-05 00:00:00",

                "serverTime": null,

                "moneyType": 2,

                "labelCode": 10

            },

            {

                "applyId": "1147018860570537984",

                "applyType": 2,

                "applyTypeName": "融资认购",

                "stockName": "香港中華煤氣",

                "stockCode": "00003",

                "exchangeType": 0,

                "status": 4,

                "statusName": "已撤销",

                "applyQuantity": 200,

                "applyAmount": 4140.31,

                "cash": null,

                "financingBalance": null,

                "interestRate": null,

                "priceMin": 10,

                "priceMax": 20,

                "listingPrice": 13,

                "financingAmount": 1.75,

                "allottedQuantity": null,

                "publishTime": "2019-07-05 00:00:00",

                "serverTime": null,

                "moneyType": 2,

                "labelCode": 4

            }

        ]
    }

}
```

</div>

### 3.6获取客户ipo申购明细

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/ipo-record`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/ipo-record`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 获取客户ipo申购明细

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填  | 类型   |
|---------------|-------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                 | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true  | string |
| X-Time        | 时间戳                              | header   | true  | string |
| X-Sign        | RSA签名                             | header   | true  | string |
| X-Channel     | 渠道                                | header   | true  | string |
| applyId       | 申购编号(传其中一个即可)            | body     | false | int64  |
| serialNo      | 流水号(传其中一个即可)              | body     | false | int64  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求示例

<div class="language-json extra-class">

``` language-json
{

"applyId": 1147036407112679424,

"serialNo": 1233123554314

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                        |
|--------|--------------|-------------------------------|
| 200    | OK           | ResponseVO«IpoRecordResponse» |
| 201    | Created      |                               |
| 401    | Unauthorized |                               |
| 403    | Forbidden    |                               |
| 404    | Not Found    |                               |

-   响应参数

| 参数名称             | 说明                                                                                                                                      | 类型              | schema            |
|----------------------|-------------------------------------------------------------------------------------------------------------------------------------------|-------------------|-------------------|
| code                 | 状态码                                                                                                                                    | int32             |                   |
| data                 | 返回体                                                                                                                                    | IpoRecordResponse | IpoRecordResponse |
| allottedQuantity     | 中签股数                                                                                                                                  | number            |                   |
| applyAmount          | 认购总金额(包含手续费，不包含利息)                                                                                                        | number            |                   |
| applyId              | 申请编号                                                                                                                                  | string            |                   |
| applyQuantity        | 认购股数                                                                                                                                  | number            |                   |
| applyType            | 认购类型(1-现金，2-融资)                                                                                                                  | int32             |                   |
| applyTypeName        | 认购类型(1-现金认购，2-融资认购)                                                                                                          | string            |                   |
| cash                 | 认购现金                                                                                                                                  | number            |                   |
| channel              | 渠道类型(1-APP提交，2-中台提交，99-其它)                                                                                                  | int32             |                   |
| createTime           | 认购提交时间                                                                                                                              | string            |                   |
| deductStatus         | 扣款状态(0-已冻结，1-已扣款，2-已解冻)                                                                                                    | int32             |                   |
| deductStatusName     | 扣款状态名                                                                                                                                | string            |                   |
| endTime              | 当前认购方式截止时间                                                                                                                      | string            |                   |
| exchangeType         | 市场类型(0-HK,5-US)                                                                                                                       | int32             |                   |
| failReason           | 认购失败原因                                                                                                                              | string            |                   |
| financingAmount      | 融资利息                                                                                                                                  | number            |                   |
| financingBalance     | 融资金额                                                                                                                                  | number            |                   |
| handlingFee          | 手续费                                                                                                                                    | number            |                   |
| interestDay          | 计息天数                                                                                                                                  | int32             |                   |
| interestRate         | 融资利率                                                                                                                                  | number            |                   |
| ipoId                | ipo编号                                                                                                                                   | string            |                   |
| ipoStatus            | 新股状态(0-待认购，1-认购中，2-待扣款，3-已扣款待确认，4-已确认待公布，5-已公布待上市，6-已上市，7-取消上市，8-暂缓上市，9-延迟上市)      | int32             |                   |
| labelCode            | 状态标签码(0-待系统确认,1-已认购,4-已撤销,6-待公布中签,7-已中签,9-未中签,10-认购失败)                                                     | int32             |                   |
| moneyType            | 币种类型(0-人民币，1-美元，2-港币)                                                                                                        | int32             |                   |
| publishTime          | 公布中签日期 yyyy-MM-dd HH:mm:ss                                                                                                          | string            |                   |
| refundAmount         | 退款金额                                                                                                                                  | number            |                   |
| refundFlag           | 退款状态(0-无退款，1-待退款，2-已退款)                                                                                                    | int32             |                   |
| serverTime           | 服务器时间                                                                                                                                | string            |                   |
| status               | 认购状态(0-已提交,1-已认购,2-等待改单, 3-等待撤销,4-已撤销,5-已扣款,6-待公布中签,7-全部中签,8-部分中签,9-未中签,10-认购失败,20额度申请中) | int32             |                   |
| statusName           | 认购状态名称                                                                                                                              | string            |                   |
| stockCode            | 股票代码                                                                                                                                  | string            |                   |
| stockName            | 股票名称                                                                                                                                  | string            |                   |
| listingTime          | 上市时间yyyy-MM-dd                                                                                                                        | string            |                   |
| accountCanCancel     | 该账户在APP是否允许撤销 true-允许，false-不允许                                                                                           | boolean           |                   |
| cancelDeductInterest | 融资撤销是否扣除利息(0-撤单无需收取利息，1-撤单需要收取利息，2-撤单利息收取中，3-撤单已收取利息)                                          | int32             |                   |
| msg                  | 状态信息                                                                                                                                  | string            |                   |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "msg": "操作成功",

  "data": {

    "applyId": "1178190341147189248",

    "applyType": 1,

    "applyTypeName": "现金认购",

    "stockName": "新城市建设发展",

    "stockCode": "00456",

    "exchangeType": 0,

    "status": 4,

    "statusName": "已撤销",

    "applyQuantity": 1900.00,

    "applyAmount": 34544.6300,

    "cash": null,

    "financingBalance": null,

    "interestRate": null,

    "financingAmount": 0.0000,

    "allottedQuantity": null,

    "publishTime": "2019-10-03 00:00:00",

    "serverTime": "2019-11-01 20:33:55",

    "moneyType": 2,

    "labelCode": 4,

    "createTime": "2019-09-29 14:10:42",

    "deductStatus": 2,

    "deductStatusName": "已解冻",

    "refundFlag": 0,

    "refundAmount": null,

    "handlingFee": 0.0000,

    "failReason": null,

    "endTime": "2019-09-30 11:18:00",

    "ipoId": "1178148950262435840",

    "interestDay": 0,

    "channel": 1,

    "listingTime": "2019-10-04",

    "ipoStatus": 6

  }

}
```

</div>

### 3.7额度不足时确认现金认购数量

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/ipo-comfirm-qyt/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/ipo-comfirm-qyt/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 额度不足时确认现金认购数量

-   请求参数

| 参数名称            | 说明                                        | 请求类型 | 必填  | 类型    |
|---------------------|---------------------------------------------|----------|-------|---------|
| Authorization       | 头部信息的token信息                         | header   | true  | string  |
| X-Lang              | 语言类别(1-简体，2-繁体，3-English)         | header   | true  | string  |
| X-Time              | 时间戳                                      | header   | true  | string  |
| X-Sign              | RSA签名                                     | header   | true  | string  |
| X-Channel           | 渠道                                        | header   | true  | string  |
| applyId             | 申购编号                                    | query    | true  | integer |
| noQuotaCashFlag     | 是否需要现金认购(0-否，1-是)                | query    | true  | integer |
| confirmBy           | 确认来源，1-ipo认购,2-ipo修改,3-ipo详情修改 | query    | true  | integer |
| noQuotaCashQuantity | 申购股数，noQuotaCashFlag=1时必填           | query    | false | number  |

-   请求示例

<div class="language-json extra-class">

``` language-json
{

  "applyId": "1249718975670743040",

  "noQuotaCashFlag":0

} 
```

</div>

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数

| 参数名称 | 参数说明 | 类型           | schema         |
|----------|----------|----------------|----------------|
| code     | 状态码   | integer(int32) | integer(int32) |
| msg      |          |                |                |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "msg": "操作成功",

} 
```

</div>

## **4** 资金记录

### 4.1查询汇率

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-capital-server/open-api/currency-exchange-info`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-capital-server/open-api/currency-exchange-info`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填 | 类型   |
|---------------|-------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                 | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true | string |
| X-Time        | 时间戳                              | header   | true | string |
| X-Sign        | RSA签名                             | header   | true | string |
| X-Channel     | 渠道                                | header   | true | string |

-   响应状态

| 状态码 | 说明         | schema                                   |
|--------|--------------|------------------------------------------|
| 200    | OK           | CapitalResponseVO«FetchExchangeRateResp» |
| 201    | Created      |                                          |
| 401    | Unauthorized |                                          |
| 403    | Forbidden    |                                          |
| 404    | Not Found    |                                          |

-   响应参数

| 参数名称       | 说明                               | 类型   |
|----------------|------------------------------------|--------|
| code           | 状态码                             | int32  |
| data           | 返回体                             | array  |
| baseMoneyType  | 基准币种，0:人民币 1：美元 2：港币 | int32  |
| sourceCurrency | 源币种，0:人民币 1：美元 2：港币   | int32  |
| targetCurrency | 目标币，0:人民币 1：美元 2：港币   | int32  |
| yxBuyRate      | 盈立买入汇率                       | number |
| yxSellRate     | 盈立卖出汇率                       | number |
| bocSellRate    | 中银卖出汇率                       | number |
| bocBuyRate     | 中银买入汇率                       | number |
| msg            | 状态信息                           | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

 "code": 0,

 "msg": "操作成功",

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
```

</div>

### 4.2获取历史记录

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-capital-server/open-api/business-flow`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-capital-server/open-api/business-flow`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述

-   请求示例

<div class="language-json extra-class">

``` language-json
{

    "dateType": 9,

    "pageNum": 1,

    "pageSize": 10,

    "startTime": "2020-05-09 00:00:00",

    "endTime": "2020-12-24 23:59:59",

    "type": -1

}
```

</div>

-   请求参数

| 参数名称      | 说明                                               | 请求类型 | 必填  | 类型      |
|---------------|----------------------------------------------------|----------|-------|-----------|
| Authorization | 头部信息的token信息                                | header   | true  | string    |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                | header   | true  | string    |
| X-Channel     | 渠道ID，由盈立分配                                 | header   | true  | string    |
| X-Time        | 时间戳                                             | header   | true  | string    |
| X-Sign        | RSA签名                                            | header   | true  | string    |
| dateType      | -1,全部0,近一个月1,近三个月2,近一年3,今年9 ,自定义 | body     | false | int32     |
| startTime     | 开始时间，data-9时传                               | body     | false | date-time |
| endTime       | 结束时间，data-9时传                               | body     | false | date-time |
| pageNum       | 当前页 1开始                                       | body     | true  | int32     |
| pageSize      | 每页结果数                                         | body     | true  | int32     |
| type          | 0-入金，1-出金，2-货币兑换，不传查询所有           | body     | false | int32     |

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数

| 参数名称       | 说明                                                                                                                                                                                                                                                                                                                                                     | 类型   |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------|
| code           | 状态码                                                                                                                                                                                                                                                                                                                                                   | int32  |
| list           | 结果集合                                                                                                                                                                                                                                                                                                                                                 | array  |
| applyTime      | 发生时间                                                                                                                                                                                                                                                                                                                                                 | string |
| businessId     | 业务ID                                                                                                                                                                                                                                                                                                                                                   | string |
| businessStatus | 业务实际状态值 入金：入金状态 0无效 ，10客户入金申请，20待初审匹配，23初审匹配失败，25终审驳回给财务，30待客服确认，40待终审，51驳回给客户，52审核不通过，无退款（终态）， 60待入金，62入金处理中，超过十分钟定时任务补查结果，63入金失败,需要人工干预，64入金成功（终态），70待退款，73退款失败,需要人工干预，74退款成功（终态）。状态&gt;=40的不能撤销 | int32  |
| occurBalance   | 入金的通知金额、出金的提取金额、换汇的兑换金额                                                                                                                                                                                                                                                                                                           | string |
| postBalance    | 入金的实际到账金额、换汇的兑换结果                                                                                                                                                                                                                                                                                                                       | string |
| reason         | 驳回原因                                                                                                                                                                                                                                                                                                                                                 | string |
| statusDesc     | 状态描述1换汇成功,2换汇失败,3处理中,10待处理,11处理中,12已汇出,13出金失败,14已撤销,15已驳回,20处理中,21已到账,22入金失败,30已驳回,40待退款,41已退款,42 "退款失败                                                                                                                                                                                         | string |
| statusValue    | 状态值                                                                                                                                                                                                                                                                                                                                                   | int32  |
| title          | 标题，如转入港币、港币兑美元                                                                                                                                                                                                                                                                                                                             | string |
| type           | 类型                                                                                                                                                                                                                                                                                                                                                     | string |
| pageNum        | 当前页                                                                                                                                                                                                                                                                                                                                                   | int32  |
| pageSize       | 每页条数                                                                                                                                                                                                                                                                                                                                                 | int32  |
| systemDate     | 系统当前时间 yyyy-MM-dd                                                                                                                                                                                                                                                                                                                                  | string |
| total          | 总数                                                                                                                                                                                                                                                                                                                                                     | int32  |
| error          | 错误详情                                                                                                                                                                                                                                                                                                                                                 | string |
| msg            | 状态信息                                                                                                                                                                                                                                                                                                                                                 | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": {

    "list": [

      {

        "applyTime": "2020-05-09 16:15:38",

        "businessId": "776607442319044608",

        "businessStatus": null,

        "occurBalance": "1000.00港币",

        "postBalance": "",

        "reason": "",

        "statusDesc": "待处理",

        "statusValue": 10,

        "title": "提取 港币",

        "type": "1"

      },

      {

        "applyTime": "2020-04-16 15:59:15",

        "businessId": "768268401176485888",

        "businessStatus": 23,

        "occurBalance": "20000.00港币",

        "postBalance": "",

        "reason": "",

        "statusDesc": "处理中",

        "statusValue": 20,

        "title": "转入 港币",

        "type": "0"

      }

    ],

    "pageNum": 1,

    "pageSize": 10,

    "systemDate": "2020-05-09",

    "total": 2

  },

  "msg": "成功"

}
```

</div>

### 4.2客户出金撤销

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-capital-server/open-api/app-cashOut-revoke`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-capital-server/open-api/app-cashOut-revoke`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述

-   请求示例

<div class="language-json extra-class">

``` language-json
{

  "id": 768268401176485888

}
```

</div>

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填 | 类型   |
|---------------|-------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                 | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true | string |
| X-Time        | 时间戳                              | header   | true | string |
| X-Sign        | RSA签名                             | header   | true | string |
| id            | id                                  | body     | true | int64  |

-   响应状态

| 状态码 | 说明         |
|--------|--------------|
| 200    | OK           |
| 201    | Created      |
| 401    | Unauthorized |
| 403    | Forbidden    |
| 404    | Not Found    |

-   响应参数

| 参数名称 | 说明     | 类型   |
|----------|----------|--------|
| code     | 状态码   | int32  |
| data     | 返回体   |        |
| error    | 错误详情 | string |
| msg      | 状态信息 | string |

-   响应示例

<div class="language-json extra-class">

``` language-json
{

  "code": 0,

  "data": null,

  "msg": "成功"

}
```

</div>

## **5** 数据字典

### 5.1订单状态（Status）

| 编码 | 名称     |
|------|----------|
| -1   | 失败     |
| 0    | 全部成交 |
| 1    | 等待提交 |
| 2    | 待成交   |
| 3    | 部分成交 |
| 4    | 等待撤单 |
| 5    | 等待改单 |
| 6    | 已撤单   |
| 7    | 部成撤单 |
| 8    | 废单     |
| 11   | 等待提交 |
| 61   | 收市撤单 |

### 5.2市场类型（ExchangeType）

| 编码 | 名称                 |
|------|----------------------|
| 0    | 港股                 |
| 1    | 上海A                |
| 2    | 上海B                |
| 3    | 深圳A                |
| 4    | 深圳B                |
| 5    | 美股                 |
| 6    | 沪港通               |
| 7    | 深港通               |
| 67   | A股（用于查询）      |
| 100  | 所有市场（用于查询） |

### 5.3IPO新股状态（Status）

| 编码 | 名称         |
|------|--------------|
| 0    | 待认购       |
| 1    | 认购中       |
| 2    | 待扣款       |
| 3    | 已扣款待确认 |
| 4    | 已确认待公布 |
| 5    | 已公布待上市 |
| 6    | 已上市       |
| 7    | 取消上市     |
| 8    | 暂缓上市     |
| 9    | 延迟上市     |
| 11   | 已删除       |

### 5.4IPO认购状态（Status）

| 编码 | 名称       |
|------|------------|
| 0    | 已提交     |
| 1    | 已认购     |
| 2    | 等待改单   |
| 3    | 等待撤销   |
| 4    | 已撤销     |
| 5    | 已扣款     |
| 6    | 待公布中签 |
| 7    | 全部中签   |
| 8    | 部分中签   |
| 9    | 未中签     |
| 10   | 认购失败   |
| 11   | 已中签     |
| 12   | 待系统确认 |
| 20   | 申请额度中 |

### 5.5币种（moneyType）

| 编码 | 名称   |
|------|--------|
| 0    | 人民币 |
| 1    | 美元   |
| 2    | 港币   |

### 5.6设备类别（X-Dt）

| 编码 | 名称    |
|------|---------|
| t1   | 安卓    |
| t2   | Ios     |
| t3   | 其它    |
| t4   | Windows |
| t5   | Mac     |

### 5.7账户类型（AssetProp）

| 编码 | 名称     |
|------|----------|
| 0    | 现金账户 |
| M    | 融资账户 |

## **6** 孖展

### 6.1获取股票抵押比率列表

-   生产环境接口地址 `https://open-jy.yxzq.com/stock-order-server/open-api/mortgage-list`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/stock-order-server/open-api/mortgage-list`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["*/*"\]

-   接口描述 获取股票抵押比率列表（不需要登录）

-   请求参数

| 参数名称      | 说明                                   | 请求类型 | 必填  | 类型    |
|---------------|----------------------------------------|----------|-------|---------|
| Authorization | 头部信息的token信息                    | header   | true  | string  |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)    | header   | true  | string  |
| X-Channel     | 渠道                                   | header   | true  | string  |
| X-Time        | 时间戳                                 | header   | true  | string  |
| X-Sign        | RSA签名                                | header   | true  | string  |
| exchangeType  | 市场：0-港股，5-美股，67-A股，100-全部 | body     | false | int32   |
| stockCode     | 证券代码                               | body     | false | string  |
| status        | 状态:1-生效中 0-已下架,默认1           | body     | false | int32   |
| pageSizeZero  | 是否不分页,默认false                   | body     | false | boolean |
| pageNum       | 当前页 1开始, 默认值1                  | body     | false | int32   |
| pageSize      | 每页结果数, 默认值10,最大20            | body     | false | int32   |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{

    "exchangeType": 0,

    "pageNum": 1,

    "pageSize": 10,

    "stockCode": "",

  "pageSizeZero":true,

  "status":1

}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                                  |
|--------|--------------|---------------------------------------------------------|
| 200    | OK           | ResponseVO&lt;PageInfoVO&lt;MortgageOpenApiResp&gt;&gt; |
| 201    | Created      |                                                         |
| 401    | Unauthorized |                                                         |
| 403    | Forbidden    |                                                         |
| 404    | Not Found    |                                                         |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>ResponseVO&lt;PageInfoVO&lt;MortgageOpenApiResp&gt;&gt;</td><td>ResponseVO&lt;PageInfoVO&lt;MortgageOpenApiResp&gt;&gt;</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>MortgageOpenApiResp</td></tr><tr class="even"><td>beginTime</td><td>生效日</td><td>string(date-time)</td><td></td></tr><tr class="odd"><td>effectiveTime</td><td>有效截止时间yyyy-MM-dd HH:mm:ss</td><td>string(date-time)</td><td></td></tr><tr class="even"><td>exchangeType</td><td>市场(0-港股 5-美股 6-沪港通 7-深港通)</td><td>int32</td><td></td></tr><tr class="odd"><td>exchangeTypeName</td><td>市场名称</td><td>string</td><td></td></tr><tr class="even"><td>mortgageRatio</td><td>融资抵押比率</td><td>string</td><td></td></tr><tr class="odd"><td>status</td><td>记录状态 1-生效中 0-已下架</td><td>int32</td><td></td></tr><tr class="even"><td>statusName</td><td>记录状态名称</td><td>string</td><td></td></tr><tr class="odd"><td>stockCode</td><td>证券代码</td><td>string</td><td></td></tr><tr class="even"><td>stockName</td><td>证券名称</td><td>string</td><td></td></tr><tr class="odd"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="even"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="odd"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td></td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{

 "code": 0,

 "msg": "操作成功",

 "data": {

  "pageNum": 1,

  "pageSize": 10,

  "total": 2,

  "list": [

   {

    "exchangeType": 6,

    "exchangeTypeName": "沪港通",

    "stockName": "贵州茅台",

    "stockCode": "600519",

    "mortgageRatio": "60.00%",

    "beginTime": "2020-10-27",

    "effectiveTime": "2099-12-31",

    "status": 1,

    "statusName": "生效中"

   },

   {

    "exchangeType": 6,

    "exchangeTypeName": "沪港通",

    "stockName": "上海临港",

    "stockCode": "600848",

    "mortgageRatio": "10.00%",

    "beginTime": "2020-10-27",

    "effectiveTime": "2099-12-31",

    "status": 1,

    "statusName": "生效中"

   }

  ]

 }

}
```

</div>

## **7** MA账户交易及查询

### 7.1下单

-   生产环境接口地址 `https://open-jy.yxzq.com/ams-center/open-api/ma-order-submit/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/ams-center/open-api/ma-order-submit/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 下单

-   请求参数

| 参数名称         | 说明                                                                                    | 请求类型 | 必填 | 类型   |
|------------------|-----------------------------------------------------------------------------------------|----------|------|--------|
| Authorization    | 头部信息的token信息                                                                     | header   | true | string |
| X-Lang           | 语言类别(1-简体，2-繁体，3-English)                                                     | header   | true | string |
| X-Channel        | 渠道ID，由盈立分配                                                                      | header   | true | string |
| X-Time           | 时间戳                                                                                  | header   | true | string |
| X-Dt             | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac)                                | header   | true | string |
| X-Sign           | RSA签名                                                                                 | header   | true | string |
| serialNo         | 流水号，最长19位，确保唯一推荐雪花算法生成                                              | body     | true | int64  |
| strategyId       | 策略id                                                                                  | body     | true | number |
| stockId          | 股票代码                                                                                | body     | true | string |
| tradeType        | 交易类型 1.买 2.卖                                                                      | body     | true | int32  |
| opType           | 委托类型 0.买 1.卖                                                                      | body     | true | int32  |
| orderType        | 订单类型 订单类型 1.限价单 2.增强限价单 3.市价单 4.竞价单 5.竞价现价单 6.条件单（限价） | body     | true | int32  |
| sellQuota        | 委托数量                                                                                | body     | true | number |
| sellPrice        | 委托价格 （每股价格 \*10000)                                                            | body     | true | number |
| openClosePreFlag | 是否允许盘前盘后交易 1.不允许 2.允许                                                    | body     | true | int32  |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "strategyId": 10626,
  "stockId": "hk02202",
  "tradeType": 1,
  "orderType": 2,
  "opType": 0,
  "sellQuota": 100,
  "sellPrice": 1000,
  "openClosePreFlag": 1,
  "serialNo":"4234345345345"
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                |
|--------|--------------|---------------------------------------|
| 0      | 成功         |                                       |
| 200    | OK           | ResponseVO«OpenApiMaOrderCancelReqVO» |
| 201    | Created      |                                       |
| 401    | Unauthorized |                                       |
| 403    | Forbidden    |                                       |
| 404    | Not Found    |                                       |

-   响应参数

| 参数名称 | 说明                           | 类型                      | schema                    |
|----------|--------------------------------|---------------------------|---------------------------|
| code     | 状态码                         | int32                     |                           |
| data     | 返回体                         | OpenApiMaOrderCancelReqVO | OpenApiMaOrderCancelReqVO |
| orderId  | 订单id,可用于查询订单/取消订单 | string                    |                           |
| msg      | 状态信息                       | string                    |                           |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": {
    "orderId": "1449856553723613186"
  },
  "msg": "Success"
}
```

</div>

### 7.2撤单

-   生产环境接口地址 `https://open-jy.yxzq.com/ams-center/open-api/ma-order-cancel/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/ams-center/open-api/ma-order-cancel/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 撤单

-   请求参数

| 参数名称      | 说明                                                                 | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                                  | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                                  | header   | true | string |
| X-Request-Id  | 头部信息的requestId信息,长度30位，确保唯一，防止重复提交实现接口幂等 | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                                   | header   | true | string |
| X-Time        | 时间戳                                                               | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac)             | header   | true | string |
| X-Sign        | RSA签名                                                              | header   | true | string |
| maOrderId     | ma订单id                                                             | body     | true | String |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1

X-Request-Id: 928239187123721231232

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "maOrderId": "1447739372567232512"
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 状态码   | int32  |        |
| data     | 返回体   |        |        |
| msg      | 状态信息 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": null,
  "msg": "Success"
}
```

</div>

### 7.3订单列表-分页查询

-   生产环境接口地址 `https://open-jy.yxzq.com/ams-center/open-api/ma-order-list/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/ams-center/open-api/ma-order-list/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 订单列表-分页查询

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填  | 类型   |
|---------------|-------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                 | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true  | string |
| X-Time        | 时间戳                              | header   | true  | string |
| X-Sign        | RSA签名                             | header   | true  | string |
| pageNum       | 当前页 1开始，默认值1               | body     | false | int32  |
| pageSize      | 每页结果数，默认值20                | body     | false | int32  |
| strategyId    | 策略id                              | body     | true  | number |
| today         | 是否今日订单，1 是，0 历史          | body     | true  | int32  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "strategyId": 10626,
  "pageNum": 1,
  "pageSize": 20,
  "today": 0
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>PageInfoVO«MaOrderListResponse»</td><td>PageInfoVO«MaOrderListResponse»</td></tr><tr class="odd"><td>list</td><td>结果集合</td><td>array</td><td>MaOrderListResponse</td></tr><tr class="even"><td>serialNo</td><td>流水号</td><td>int64</td><td></td></tr><tr class="odd"><td>createTime</td><td>委托时间</td><td>string</td><td></td></tr><tr class="even"><td>orderStatus</td><td>订单状态(1-等待提交，5-待报单，10-报单中，11-待成交，12-等待撤单，13-等待改单，20-部分成交，27-成交处理中，28-部成撤单，29-全部成交，30-已撤单，31-下单失败，32-废单，33-收市撤单 40-分配中 41-分配成功 42-分配失败 50补单中 51补单成功 52补单失败)</td><td>int32</td><td></td></tr><tr class="odd"><td>cancelable</td><td>是否可取消 1 是，0 否</td><td>integer</td><td></td></tr><tr class="even"><td>dealAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>dealMoney</td><td>成交金额</td><td>number</td><td></td></tr><tr class="even"><td>dealPrice</td><td>成交价格</td><td>number</td><td></td></tr><tr class="odd"><td>dealTime</td><td>成交时间</td><td>string</td><td></td></tr><tr class="even"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="odd"><td>entrustPrice</td><td>委托价格</td><td>float</td><td></td></tr><tr class="even"><td>entrustProp</td><td>委托属性 LMT-限价单,ELMT-增强限价单,MKT-市价单,AM-竟价市价单,AL-竟价限价单</td><td>string</td><td></td></tr><tr class="odd"><td>entrustTime</td><td>委托时间</td><td>date-time</td><td></td></tr><tr class="even"><td>jyTradeId</td><td>上手下单后返回的序号</td><td>string</td><td></td></tr><tr class="odd"><td>maOrderId</td><td>MA订单ID</td><td>number</td><td></td></tr><tr class="even"><td>opType</td><td>委托方向 (0 买 1 卖)</td><td>integer</td><td></td></tr><tr class="odd"><td>tradeType</td><td>交易类型 1.买 2.卖</td><td>integer</td><td></td></tr><tr class="even"><td>stockId</td><td>股票代码</td><td>string</td><td></td></tr><tr class="odd"><td>stockMarket</td><td>股票市场 （1 HK 2 US 4 A股 8 SG）</td><td>integer</td><td></td></tr><tr class="even"><td>stockName</td><td>股票名称</td><td>string</td><td></td></tr><tr class="odd"><td>pageNum</td><td>当前页</td><td>int32</td><td></td></tr><tr class="even"><td>pageSize</td><td>每页条数</td><td>int32</td><td></td></tr><tr class="odd"><td>total</td><td>总数</td><td>int64</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": {
    "list": [
      {
        "cancelable": 0,
        "dealAmount": 0.000000,
        "dealMoney": null,
        "dealPrice": null,
        "dealTime": "",
        "entrustAmount": 100.000000,
        "entrustMoney": 0,
        "entrustPrice": 0.100000,
        "entrustProp": "ELMT",
        "entrustTime": "2025-06-10 11:47:14",
        "jyTradeId": "1932283389052784640",
        "maOrderId": "1449856553723613186",
        "opType": 0,
        "orderStatus": 33,
        "remarks": "",
        "serialNo": "4234345345345",
        "stockId": "02202",
        "stockMarket": 1,
        "stockName": "万科企业",
        "tradeType": 1
      }
    ],
    "total": 6
  },
  "msg": "Success"
}
```

</div>

### 7.4订单详情

-   生产环境接口地址 `https://open-jy.yxzq.com/ams-center/open-api/ma-order-detail/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/ams-center/open-api/ma-order-detail/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 订单详情

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填 | 类型   |
|---------------|-------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                 | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true | string |
| X-Time        | 时间戳                              | header   | true | string |
| X-Sign        | RSA签名                             | header   | true | string |
| maOrderId     | ma订单id                            | body     | true | String |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "maOrderId": 1449856553723613186
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>OpenapiMaOrderDetailVO</td><td>OpenapiMaOrderDetailVO</td></tr><tr class="odd"><td>serialNo</td><td>流水号</td><td>int64</td><td></td></tr><tr class="even"><td>updateTime</td><td>更新时间</td><td>string</td><td></td></tr><tr class="odd"><td>orderStatus</td><td>订单状态(1-等待提交，5-待报单，10-报单中，11-待成交，12-等待撤单，13-等待改单，20-部分成交，27-成交处理中，28-部成撤单，29-全部成交，30-已撤单，31-下单失败，32-废单，33-收市撤单 40-分配中 41-分配成功 42-分配失败 50补单中 51补单成功 52补单失败)</td><td>int32</td><td></td></tr><tr class="even"><td>dealAmount</td><td>成交数量</td><td>number</td><td></td></tr><tr class="odd"><td>dealMoney</td><td>成交金额</td><td>number</td><td></td></tr><tr class="even"><td>dealPrice</td><td>成交价格</td><td>number</td><td></td></tr><tr class="odd"><td>dealTime</td><td>成交时间</td><td>string</td><td></td></tr><tr class="even"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="odd"><td>entrustPrice</td><td>委托价格</td><td>float</td><td></td></tr><tr class="even"><td>orderType</td><td>委托属性 LMT-限价单,ELMT-增强限价单,MKT-市价单,AM-竟价市价单,AL-竟价限价单</td><td>string</td><td></td></tr><tr class="odd"><td>entrustTime</td><td>委托时间</td><td>string</td><td></td></tr><tr class="even"><td>jyEntrustId</td><td>上手下单后返回的序号</td><td>string</td><td></td></tr><tr class="odd"><td>maOrderId</td><td>MA订单ID</td><td>number</td><td></td></tr><tr class="even"><td>opType</td><td>委托方向 (0 买 1 卖)</td><td>integer</td><td></td></tr><tr class="odd"><td>tradeType</td><td>交易类型 1.买 2.卖</td><td>integer</td><td></td></tr><tr class="even"><td>stockId</td><td>股票代码</td><td>string</td><td></td></tr><tr class="odd"><td>stockMarket</td><td>股票市场 （1 HK 2 US 4 A股 8 SG）</td><td>integer</td><td></td></tr><tr class="even"><td>stockName</td><td>股票名称</td><td>string</td><td></td></tr><tr class="odd"><td>remarks</td><td>备注</td><td>string</td><td></td></tr><tr class="even"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": {
    "dealAmount": 0.000000,
    "dealMoney": 0.000000,
    "dealPrice": 0.000000,
    "dealTime": "",
    "entrustAmount": 100.000000,
    "entrustPrice": 0.100000,
    "entrustTime": "2025-06-10 11:47:14",
    "jyEntrustId": "1932283389052784640",
    "maOrderId": "1449856553723613186",
    "opType": 0,
    "orderStatus": 33,
    "orderType": "ELMT",
    "remarks": "",
    "serialNo": "4234345345345",
    "stockId": "02202",
    "stockMarket": 1,
    "stockName": "万科企业",
    "tradeType": 1,
    "updateTime": "2025-06-10 16:12:01"
  },
  "msg": "Success"
}
```

</div>

### 7.5获取策略购买力

-   生产环境接口地址 `https://open-jy.yxzq.com/ams-center/open-api/get-ma-trade-account-info/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/ams-center/open-api/get-ma-trade-account-info/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 获取策略购买力

-   请求参数

| 参数名称      | 说明                                | 请求类型 | 必填 | 类型    |
|---------------|-------------------------------------|----------|------|---------|
| Authorization | 头部信息的token信息                 | header   | true | string  |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English) | header   | true | string  |
| X-Channel     | 渠道ID，由盈立分配                  | header   | true | string  |
| X-Time        | 时间戳                              | header   | true | string  |
| X-Sign        | RSA签名                             | header   | true | string  |
| strategyId    | 策略id                              | body     | true | number  |
| stockId       | 股票代码                            | body     | true | string  |
| opType        | 委托方向 0-买 1-卖                  | body     | true | integer |
| price         | 每股价格 \*10000                    | body     | true | number  |
| amount        | 股票数量                            | body     | true | number  |

-   请求header示例

<div class="language-json extra-class">

``` language-json
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Lang: 1

X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "strategyId": 10626,
  "stockId": "hk01810",
  "opType": 0,
  "price": 533000,
  "amount": 200
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

<table><colgroup><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /><col style="width: 25%" /></colgroup><thead><tr class="header"><th>参数名称</th><th><div class="table_width">说明</div></th><th>类型</th><th>schema</th></tr></thead><tbody><tr class="odd"><td>code</td><td>状态码</td><td>int32</td><td></td></tr><tr class="even"><td>data</td><td>返回体</td><td>GetMaTradeAccountInfoRespVO</td><td>GetMaTradeAccountInfoRespVO</td></tr><tr class="odd"><td>cash</td><td>可用现金余额</td><td>string</td><td></td></tr><tr class="even"><td>availableBuyPosition</td><td>可买入股票数量占总资产的比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="odd"><td>availableBuyAmount</td><td>可以买入的最大股票数量（以股为单位）</td><td>string</td><td></td></tr><tr class="even"><td>availableSellAmount</td><td>实际可卖数量</td><td>number</td><td></td></tr><tr class="odd"><td>availableSellPosition</td><td>可卖出股票数量占总资产的比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="even"><td>entrustPosition</td><td>委托买卖股票数量占总资产的比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="odd"><td>entrustAmount</td><td>委托数量</td><td>number</td><td></td></tr><tr class="even"><td>endPosition</td><td>交易完成后预期的持仓比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="odd"><td>startPosition</td><td>交易前已有的持仓比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="even"><td>realAvailableBuyPosition</td><td>实际可购买的股票比例（以万分之一为单位）</td><td>number</td><td></td></tr><tr class="odd"><td>msg</td><td>状态信息</td><td>string</td><td></td></tr></tbody></table>

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": {
    "availableBuyAmount": 2,
    "availableBuyPosition": 51,
    "availableSellAmount": null,
    "availableSellPosition": null,
    "cash": "1525048",
    "endPosition": 3974,
    "entrustAmount": 2,
    "entrustPosition": 51,
    "realAvailableBuyPosition": 3974,
    "startPosition": 3922
  },
  "msg": "Success"
}
```

</div>

## **8** 期权交易和查询接口

### 8.1 期权-下单

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/option-trade/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/option-trade/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-下单

-   请求参数

-   Request Parameters

| 参数名称       | 说明                                                     | 请求类型 | 必填  | 类型   |
|----------------|----------------------------------------------------------|----------|-------|--------|
| Authorization  | 头部信息的token信息                                      | header   | true  | string |
| X-Lang         | 语言类别(1-简体，2-繁体，3-English)                      | header   | true  | string |
| X-Channel      | 渠道ID，由盈立分配                                       | header   | true  | string |
| X-Time         | 时间戳                                                   | header   | true  | string |
| X-Dt           | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true  | string |
| X-Sign         | RSA签名                                                  | header   | true  | string |
| `requestId`    | 请求流水号 (最小10，最大36位字符串)                      | body     | true  | string |
| `side`         | 买卖方向 1-买，2-卖                                      | body     | true  | number |
| `qty`          | 数量, 小数位最多两位，大于0                              | body     | true  | number |
| `price`        | 价格, 小数位最多两位，大于0, 非市价单必须传              | body     | true  | int32  |
| `symbol`       | 期权代码                                                 | body     | true  | string |
| `orderType`    | 订单类别 1-市价单 2-限价单                               | body     | true  | number |
| `businessType` | 业务类型：O-期权（缺省值），OS-期权沽空                  | body     | true  | string |
| `entrustType`  | 委托方式,默认 2- INTERNET, 1-电话委托                    | body     | false | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "businessType": "O",
  "orderType": 2,
  "price": 2.93,
  "qty": 1,
  "requestId": "11171635208375627921",
  "side": 1,
  "symbol": "TSLA250808C50000"
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                  |
|--------|--------------|-----------------------------------------|
| 0      | 成功         |                                         |
| 200    | OK           | ResponseVO«OpenApiEntrustOrderResponse» |
| 201    | Created      |                                         |
| 401    | Unauthorized |                                         |
| 403    | Forbidden    |                                         |
| 404    | Not Found    |                                         |

-   响应参数

| 参数名称 | 说明                              | 类型                        | schema                      |
|----------|-----------------------------------|-----------------------------|-----------------------------|
| code     | 状态码                            | int32                       |                             |
| data     | 返回体                            | OpenApiEntrustOrderResponse | OpenApiEntrustOrderResponse |
| orderId  | 订单id,可用于查询、改单、取消订单 | string                      |                             |
| msg      | 状态信息                          | string                      |                             |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "data": {
    "orderId": "1449856553723613186"
  },
  "msg": "Success"
}
```

</div>

### 8.2 期权-改单

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/option-replace-order/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/option-replace-order/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-改单

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                      | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true | string |
| X-Time        | 时间戳                                                   | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true | string |
| X-Sign        | RSA签名                                                  | header   | true | string |
| `requestId`   | 请求流水号 (最小10，最大36位字符串)                      | body     | true | string |
| `orderId`     | 订单ID                                                   | body     | true | number |
| `qty`         | 数量, 小数位最多两位，大于0                              | body     | true | number |
| `price`       | 价格, 小数位最多两位，大于0, 非市价单必须传              | body     | true | int32  |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "price": 2.93,
  "qty": 1,
  "requestId": "11171635208375627921",
  "orderId": 1449856553723613186
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                |
|--------|--------------|---------------------------------------|
| 0      | 成功         |                                       |
| 200    | OK           | ResponseVO«OpenApiMaOrderCancelReqVO» |
| 201    | Created      |                                       |
| 401    | Unauthorized |                                       |
| 403    | Forbidden    |                                       |
| 404    | Not Found    |                                       |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 状态码   | int32  |        |
| msg      | 状态信息 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "Success"
}
```

</div>

### 8.3 期权-撤单

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/option-cancel-order/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/option-cancel-order/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-撤单

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                      | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true | string |
| X-Time        | 时间戳                                                   | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true | string |
| X-Sign        | RSA签名                                                  | header   | true | string |
| `requestId`   | 请求流水号 (最小10，最大36位字符串)                      | body     | true | string |
| `orderId`     | 订单ID                                                   | body     | true | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "requestId": "11171635208375627921",
  "orderId": 1449856553723613186
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                |
|--------|--------------|---------------------------------------|
| 0      | 成功         |                                       |
| 200    | OK           | ResponseVO«OpenApiMaOrderCancelReqVO» |
| 201    | Created      |                                       |
| 401    | Unauthorized |                                       |
| 403    | Forbidden    |                                       |
| 404    | Not Found    |                                       |

-   响应参数

| 参数名称 | 说明     | 类型   | schema |
|----------|----------|--------|--------|
| code     | 状态码   | int32  |        |
| msg      | 状态信息 | string |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "Success"
}
```

</div>

### 8.4 期权-获取下单购买力

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/option-customer-range/v2`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/option-customer-range/v2`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-获取下单购买力

-   请求参数

-   Request Parameters

| 参数名称       | 说明                                                     | 请求类型 | 必填  | 类型   |
|----------------|----------------------------------------------------------|----------|-------|--------|
| Authorization  | 头部信息的token信息                                      | header   | true  | string |
| X-Lang         | 语言类别(1-简体，2-繁体，3-English)                      | header   | true  | string |
| X-Channel      | 渠道ID，由盈立分配                                       | header   | true  | string |
| X-Time         | 时间戳                                                   | header   | true  | string |
| X-Dt           | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true  | string |
| X-Sign         | RSA签名                                                  | header   | true  | string |
| `symbol`       | 期权代码                                                 | body     | true  | string |
| `businessType` | 业务类型：O-期权（缺省值），OS-期权沽空                  | body     | true  | string |
| `entrustQty`   | 数量, 小数位最多两位，大于0                              | body     | false | number |
| `price`        | 价格, 买入时必传                                         | body     | false | number |
| `side`         | 买卖方向 1-买，2-卖                                      | body     | true  | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "price": 10.6,
  "symbol": "AMZN250815C1600000",
  "businessType": "O",
  "side": 1,
  "entrustQty": 1
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                    |
|--------|--------------|---------------------------|
| 0      | 成功         |                           |
| 200    | OK           | ResponseVO«OptionRangeVO» |
| 201    | Created      |                           |
| 401    | Unauthorized |                           |
| 403    | Forbidden    |                           |
| 404    | Not Found    |                           |

-   响应参数

| 参数名称     | 说明         | 类型          | schema        |
|--------------|--------------|---------------|---------------|
| code         | 状态码       | int32         |               |
| data         | 返回体       | OptionRangeVO | OptionRangeVO |
| buyMax       | 最大可买数量 | nubmer        |               |
| sellMax      | 最大可卖数量 | nubmer        |               |
| expectMargin | 预计保证金   | nubmer        |               |
| msg          | 状态信息     | string        |               |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "error": null,
  "data": {
    "buyMax": 4175,
    "sellMax": 0,
    "expectMargin": null
  }
}
```

</div>

### 8.5 期权-获取改单购买力

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/option-customer-replace-range/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/option-customer-replace-range/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-获取改单购买力

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                      | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true  | string |
| X-Time        | 时间戳                                                   | header   | true  | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true  | string |
| X-Sign        | RSA签名                                                  | header   | true  | string |
| `orderId`     | 订单id                                                   | body     | true  | number |
| `entrustQty`  | 数量, 小数位最多两位，大于0                              | body     | false | number |
| `price`       | 价格, 必传                                               | body     | true  | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "price": 10.6,
  "orderId": 122342341323445345345,
  "entrustQty": 1
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                   |
|--------|--------------|------------------------------------------|
| 0      | 成功         |                                          |
| 200    | OK           | ResponseVO«OpenApiReplaceOptionMaxMinVO» |
| 201    | Created      |                                          |
| 401    | Unauthorized |                                          |
| 403    | Forbidden    |                                          |
| 404    | Not Found    |                                          |

-   响应参数

| 参数名称 | 说明         | 类型                         | schema                       |
|----------|--------------|------------------------------|------------------------------|
| code     | 状态码       | int32                        |                              |
| data     | 返回体       | OpenApiReplaceOptionMaxMinVO | OpenApiReplaceOptionMaxMinVO |
| max      | 最大修改数量 | nubmer                       |                              |
| min      | 最小修改数量 | nubmer                       |                              |
| msg      | 状态信息     | string                       |                              |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "error": null,
  "data": {
    "max": 4175,
    "min": 0
  }
}
```

</div>

### 8.6 期权-改单状态查询

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/query-option-order-replace-status/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/query-option-order-replace-status/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-改单状态查询

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                      | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true | string |
| X-Time        | 时间戳                                                   | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true | string |
| X-Sign        | RSA签名                                                  | header   | true | string |
| `orderId`     | 订单id                                                   | body     | true | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "orderId": 122342341323445345345,
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema                                 |
|--------|--------------|----------------------------------------|
| 0      | 成功         |                                        |
| 200    | OK           | ResponseVO«OrderReplaceStatusResponse» |
| 201    | Created      |                                        |
| 401    | Unauthorized |                                        |
| 403    | Forbidden    |                                        |
| 404    | Not Found    |                                        |

-   响应参数

| 参数名称           | 说明                                                        | 类型                       | schema                     |
|--------------------|-------------------------------------------------------------|----------------------------|----------------------------|
| code               | 状态码                                                      | int32                      |                            |
| data               | 返回体                                                      | OrderReplaceStatusResponse | OrderReplaceStatusResponse |
| orderReplaceStatus | 改单状态 1-提交待处理 2-fix消息待处理 3-改单成功 4-改单失败 | int32                      |                            |
| msg                | 状态信息                                                    | string                     |                            |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "error": null,
  "data": {
    "orderReplaceStatus": 3
  }
}
```

</div>

### 8.7 期权-今日订单列表接口

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/user-option-order-list/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/user-option-order-list/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-今日订单列表接口

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填  | 类型   |
|---------------|----------------------------------------------------------|----------|-------|--------|
| Authorization | 头部信息的token信息                                      | header   | true  | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true  | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true  | string |
| X-Time        | 时间戳                                                   | header   | true  | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true  | string |
| X-Sign        | RSA签名                                                  | header   | true  | string |
| `market`      | 市场，51：美股期权                                       | body     | true  | int32  |
| `symbol`      | 期权代码                                                 | body     | false | String |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "market": 51
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

| 参数名称      | 说明         | 类型    | schema                          |
|---------------|--------------|---------|---------------------------------|
| code          | 状态码       | int32   |                                 |
| msg           | 状态信息     | string  |                                 |
| error         | 错误信息     | string  |                                 |
| data          | 返回体       | object  | PageResponse«UserOptionOrderVO» |
| data.pageNum  | 当前页码     | int32   |                                 |
| data.pageSize | 每页数量     | int32   |                                 |
| data.total    | 总记录数     | string  |                                 |
| data.pages    | 总页数       | int32   |                                 |
| data.nowDate  | 当前日期     | string  |                                 |
| data.list     | 结果集合     | array   | UserOptionOrderVO               |
| success       | 是否成功     | boolean |                                 |
| shortError    | 简短错误信息 | string  |                                 |
| shortMsg      | 简短状态信息 | string  |                                 |

-   UserOptionOrderVO 参数

| 参数名称             | 说明                                                                                                                                                                                    | 类型       | schema |
|----------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------|--------|
| id                   | id                                                                                                                                                                                      | number     |        |
| entrustId            | 委托id                                                                                                                                                                                  | number     |        |
| orderId              | 订单id                                                                                                                                                                                  | number     |        |
| entrustNo            | 委托编号                                                                                                                                                                                | string     |        |
| status               | 委托状态代码（20-提交中，21-等待报单，30-下单失败，40-废单，50-待成交，60-部分成交，70-全部成交，80-待撤单，90-已撤单，100-部成已撤，110-日末撤单，120-待改单，130-改单，140-委托下单） | int16      |        |
| statusName           | 委托状态名                                                                                                                                                                              | string     |        |
| exchangeType         | 交易类别(0港股，5美股)                                                                                                                                                                  | int16      |        |
| entrustType          | 买卖方向(0-买，1-卖)                                                                                                                                                                    | int16      |        |
| entrustProp          | 委托属性                                                                                                                                                                                | string     |        |
| entrustAmount        | 委托数量                                                                                                                                                                                | BigDecimal |        |
| businessAmount       | 成交数量                                                                                                                                                                                | BigDecimal |        |
| entrustPrice         | 委托价格                                                                                                                                                                                | BigDecimal |        |
| businessAveragePrice | 成交均价                                                                                                                                                                                | BigDecimal |        |
| stockCode            | 期权代码                                                                                                                                                                                | string     |        |
| stockName            | 期权名称                                                                                                                                                                                | string     |        |
| moneyType            | 币种类别                                                                                                                                                                                | int16      |        |
| createTime           | 委托时间                                                                                                                                                                                | string     |        |
| finalStateFlag       | 是否终态标识(0非终态，1是终态)                                                                                                                                                          | string     |        |
| quickFlag            | 快捷栏标识                                                                                                                                                                              | string     |        |
| flag                 | 订单类型(0-普通单,1-条件单,2-碎股单,3-月供股单)                                                                                                                                         | string     |        |
| sessionType          | 交易阶段标志(0-正常订单,1-盘前,2-盘后,3-暗盘)                                                                                                                                           | int16      |        |
| failReason           | 失败原因                                                                                                                                                                                | string     |        |
| validTime            | 有效期                                                                                                                                                                                  | string     |        |
| additionalFlag       | 附加单标识(1普通单,2附加单)                                                                                                                                                             | int32      |        |
| entrustSide          | 委托方向                                                                                                                                                                                | int32      |        |
| optionBusinessType   | 业务类型(Long Call,Long Put,Short Call,Short Put)                                                                                                                                       | string     |        |
| businessType         | 业务类型(O-期权,OS-期权沽空)                                                                                                                                                            | string     |        |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "error": null,
  "data": {
    "pageNum": 1,
    "pageSize": 300,
    "total": "1",
    "pages": 1,
    "nowDate": "20250825",
    "list": [
      {
        "id": "1010193322633265152",
        "entrustId": "1010193322721345536",
        "orderId": "1010193322633265152",
        "entrustNo": "1010193322721345536",
        "status": 40,
        "statusName": "废单",
        "exchangeType": 51,
        "entrustType": 0,
        "entrustProp": "0",
        "entrustAmount": "1",
        "businessAmount": "0",
        "entrustPrice": "193.67",
        "businessAveragePrice": null,
        "stockCode": "TSLA250822C140000",
        "stockName": "TSLA 250822 140.0 C",
        "moneyType": 1,
        "createTime": "2025-08-19 14:27:37",
        "finalStateFlag": "1",
        "quickFlag": "1",
        "flag": "0",
        "conId": null,
        "sessionType": 0,
        "dayEnd": null,
        "failReason": "订单被交易所拒绝",
        "validTime": null,
        "additionalFlag": 1,
        "entrustSide": 1,
        "additionalTodayEntrustList": null,
        "optionBusinessType": "Long Call",
        "businessType": "O"
      }
    ]
  },
  "success": true,
  "shortError": "成功",
  "shortMsg": "成功"
}
```

</div>

### 8.8 期权-订单详情接口

-   生产环境接口地址 `https://open-jy.yxzq.com/option-order-server/open-api/user-option-order-detail/v1`

-   测试环境接口地址 `http://open-jy-uat.yxzq.com/option-order-server/open-api/user-option-order-detail/v1`

-   请求方式 POST

-   consumes \["application/json"\]

-   produces \["application/json"\]

-   接口描述 期权-订单详情接口

-   请求参数

-   Request Parameters

| 参数名称      | 说明                                                     | 请求类型 | 必填 | 类型   |
|---------------|----------------------------------------------------------|----------|------|--------|
| Authorization | 头部信息的token信息                                      | header   | true | string |
| X-Lang        | 语言类别(1-简体，2-繁体，3-English)                      | header   | true | string |
| X-Channel     | 渠道ID，由盈立分配                                       | header   | true | string |
| X-Time        | 时间戳                                                   | header   | true | string |
| X-Dt          | 设备类型(t1-android，t2-ios，t3-其他，t4-Windows,t5-Mac) | header   | true | string |
| X-Sign        | RSA签名                                                  | header   | true | string |
| `orderId`     | 订单ID                                                   | body     | true | number |

-   请求header示例

<div class="language-java extra-class">

``` language-java
Authorization:eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXNzaW9uIjoiMzIyMzM1ZTc1NTZiNDQzMzkyZWNmZWJmYTYzYjZmMzEiLCJzb3VyY2UiOiJhcHAiLCJ1dWlkIjozNDA1MDIxMzExOTM0ODczNjB9.cvuoahb0h_s1rx57iJBwQn7FNcNfFJ6llCTUlqDTFlD

Content-Type: application/json;charset=UTF-8

X-Dt: 1

X-Lang: 1


X-Type: 1

X-Channel：100082

X-Sign：body 使用RSA私钥加密
```

</div>

-   请求body示例

<div class="language-json extra-class">

``` language-json
{
  "orderId": 123423423345345345345345
}
```

</div>

-   响应状态

| 状态码 | 说明         | schema |
|--------|--------------|--------|
| 0      | 成功         |        |
| 200    | OK           |        |
| 201    | Created      |        |
| 401    | Unauthorized |        |
| 403    | Forbidden    |        |
| 404    | Not Found    |        |

-   响应参数

| 参数名称                        | 说明                                                                                                                                                                                    | 类型    |
|---------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| **基础字段**                    |                                                                                                                                                                                         |         |
| code                            | 状态码（0表示成功）                                                                                                                                                                     | int32   |
| msg                             | 状态信息                                                                                                                                                                                | string  |
| error                           | 错误信息                                                                                                                                                                                | string  |
| success                         | 是否成功                                                                                                                                                                                | boolean |
| shortError                      | 简短错误信息                                                                                                                                                                            | string  |
| shortMsg                        | 简短状态信息                                                                                                                                                                            | string  |
| **data**                        | 返回主体数据                                                                                                                                                                            | object  |
| data.statusName                 | 委托状态名                                                                                                                                                                              | string  |
| data.status                     | 委托状态代码（20-提交中，21-等待报单，30-下单失败，40-废单，50-待成交，60-部分成交，70-全部成交，80-待撤单，90-已撤单，100-部成已撤，110-日末撤单，120-待改单，130-改单，140-委托下单） | int16   |
| data.stockCode                  | 股票代码（如"TSLA250822C140000"）                                                                                                                                                       | string  |
| data.stockName                  | 股票名称（如"TSLA 250822 140.0 C"）                                                                                                                                                     | string  |
| data.document                   | 文案信息（如"由于清算交收..."）                                                                                                                                                         | string  |
| data.entrustType                | 买卖方向（0-买，1-卖）                                                                                                                                                                  | int16   |
| data.exchangeType               | 市场类型代码                                                                                                                                                                            | int16   |
| data.finalStateFlag             | 是否终态标识（0-非终态，1-终态）                                                                                                                                                        | string  |
| data.sessionType                | 交易阶段标志（0-正常订单，1-盘前，2-盘后，3-暗盘）                                                                                                                                      | int16   |
| data.orderType                  | 订单类型（0-普通单，1-条件单，2-碎股单，3-月供股单，4-内部碎股单，5-策略单，6-送股订单）                                                                                                | int16   |
| data.timeInForce                | 订单有效期类型（DAY-当日有效，GTC-撤销前有效，GTD-指定日期前有效）                                                                                                                      | string  |
| data.validTime                  | 到期时间（格式：yyyy-MM-dd HH:mm:ss）                                                                                                                                                   | string  |
| data.additionalFlag             | 附加单标识（1-普通单，2-附加单）                                                                                                                                                        | int32   |
| data.optionBusinessType         | 期权业务类型（1.Long Call，2.Long Put，3.Short Call，4.Short Put）                                                                                                                      | string  |
| data.businessType               | 业务类型（O-期权，OS-期权沽空）                                                                                                                                                         | string  |
| **detailList**                  | 订单明细列表                                                                                                                                                                            | array   |
| detailList.entrustProp          | 委托属性代码（0-美股限价单，d-竞价单，e-增强限价单，g-竞价限价单，h-港股限价单，j-特殊限价单）                                                                                          | string  |
| detailList.entrustPropName      | 委托属性名称（如"限价单"）                                                                                                                                                              | string  |
| detailList.entrustAmount        | 委托数量（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.businessAmount       | 成交数量（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.entrustPrice         | 委托价格（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.entrustBalance       | 委托金额（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.businessAveragePrice | 成交均价（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.businessBalance      | 成交金额（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.moneyType            | 币种类别代码                                                                                                                                                                            | int16   |
| detailList.moneyTypeName        | 币种类别名（如"美元"）                                                                                                                                                                  | string  |
| detailList.createTime           | 创建时间（格式：yyyy-MM-dd HH:mm:ss）                                                                                                                                                   | string  |
| detailList.depositStockDay      | 股份到账时间（格式：yyyy-MM-dd）                                                                                                                                                        | string  |
| detailList.commissionFee        | 佣金费用（字符串形式的数字）                                                                                                                                                            | string  |
| detailList.platformUseFee       | 平台使用费（字符串形式的数字）                                                                                                                                                          | string  |
| detailList.stampDutyFee         | 印花税（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.payFee               | 交收费（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.transactionFee       | 交易费/规费（字符串形式的数字）                                                                                                                                                         | string  |
| detailList.transactionLevyFee   | 交易征费/活动费（字符串形式的数字）                                                                                                                                                     | string  |
| detailList.tradingSystemUsage   | 交易系统使用费（字符串形式的数字）                                                                                                                                                      | string  |
| detailList.handleFee            | 经手费（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.superviseFee         | 证管费（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.transferFee          | 过户费（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.registerTransferFee  | 登记过户费（字符串形式的数字）                                                                                                                                                          | string  |
| detailList.entrustFee           | 总费用（字符串形式的数字）                                                                                                                                                              | string  |
| detailList.orderStatus          | 订单状态代码（40-废单，140-委托下单等）                                                                                                                                                 | int16   |
| detailList.orderStatusName      | 订单状态名称（如"委托下单"）                                                                                                                                                            | string  |
| detailList.retractMark          | 展示标志（0-不可收起，1-可收起）                                                                                                                                                        | int16   |
| detailList.failReason           | 失败原因（如"订单被交易所拒绝"）                                                                                                                                                        | string  |
| detailList.partFillList         | GTD部分成交信息列表（当orderStatus为13时返回）                                                                                                                                          | array   |

-   响应示例

<div class="language-json extra-class">

``` language-json
{
  "code": 0,
  "msg": "成功",
  "error": null,
  "data": {
    "statusName": "废单",
    "status": 40,
    "stockCode": "TSLA250822C140000",
    "stockName": "TSLA 250822 140.0 C",
    "document": "由于清算交收，部分数据可能在交易完成的第2天（工作日）展示",
    "detailList": [
      {
        "entrustProp": "0",
        "entrustPropName": "限价单",
        "entrustAmount": "1",
        "businessAmount": "0",
        "entrustPrice": "193.67",
        "entrustBalance": "19367",
        "businessAveragePrice": null,
        "businessBalance": "0",
        "moneyType": 1,
        "moneyTypeName": "美元",
        "createTime": "2025-08-19 14:27:37",
        "depositStockDay": null,
        "commissionFee": null,
        "platformUseFee": null,
        "stampDutyFee": null,
        "payFee": null,
        "transactionFee": null,
        "transactionLevyFee": null,
        "tradingSystemUsage": null,
        "handleFee": null,
        "superviseFee": null,
        "transferFee": null,
        "registerTransferFee": null,
        "entrustFee": null,
        "orderStatus": 140,
        "orderStatusName": "委托下单",
        "retractMark": 0,
        "failReason": "订单被交易所拒绝",
        "partFillList": null
      }
    ],
    "entrustType": 0,
    "exchangeType": 51,
    "finalStateFlag": "1",
    "sessionType": 0,
    "orderType": 0,
    "timeInForce": "DAY",
    "validTime": null,
    "additionalFlag": 1,
    "additionalTodayEntrustList": null,
    "optionBusinessType": "Long Call",
    "businessType": "O"
  },
  "success": true,
  "shortError": "成功",
  "shortMsg": "成功"
}
```

</div>

</div>
