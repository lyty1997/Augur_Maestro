# uSmart 行情推送接入协议

> Source URL: https://api-doc.usmart8.com/zh-cn/quote-push.html
>
> Fetched: 2026-05-21
>
> Truth source: uSmart official web documentation. Do not replace facts in this file with deleted PDF/MinerU output unless a newer official source is provided.

<div class="theme-default-content content__default">

# <a href="#行情推送接入协议" class="header-anchor">#</a> 行情推送接入协议

## <a href="#版本说明" class="header-anchor">#</a> 版本说明

| 修改时间   | 版本   | 修改描述           |
|:-----------|:-------|:-------------------|
| 2019.12.30 | v1.0.0 | 初始化文档         |
| 2020.01.19 | v1.0.0 | 新增买卖盘推送说明 |
| 2020.02.26 | v1.0.0 | 实时行情新增字段   |

## <a href="#概述" class="header-anchor">#</a> 概述

盈立智投开放平台通过websocket与客户端保持长连接，从而提供实时行情推送服务，本文档为websocket长连接接入指引。

## <a href="#_1-接入地址" class="header-anchor">#</a> 1. 接入地址

-   生产环境接入地址 `wss://open-hz.yxzq.com:8443/wss/v1`

-   测试环境接入地址 `wss://open-hz-uat.yxzq.com/wss/v1`

-   接入协议 `websocket`

-   数据交互格式 `json`

## <a href="#_2-接入步骤" class="header-anchor">#</a> 2. 接入步骤

1.  鉴权
2.  心跳维持
3.  订阅行情/取消订阅
4.  接收推送

### <a href="#_2-1-鉴权" class="header-anchor">#</a> 2.1 鉴权

客户端鉴权请求

<div class="language- extra-class">

``` language-text
{
    "op": "auth",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号，
    "accessToken": "4F65x5A2bLyMWVQj3Aqp+B4w+ivaA7n5Oi2SuYtCJ9o=" // 登录成功之后返回的token
}
```

</div>

服务器鉴权应答

<div class="language- extra-class">

``` language-text
{
    "op": "auth",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号
    "code": 0,  //状态码 成功
    "msg": "success"  //状态描述
}
```

</div>

### <a href="#_2-2-心跳维持" class="header-anchor">#</a> 2.2 心跳维持

服务器ping

<div class="language- extra-class">

``` language-text
{
    "op": "ping",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666  //unix 请求序列号
}
```

</div>

客户端pong

<div class="language- extra-class">

``` language-text
{
    "op": "pong",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666  //unix 请求序列号
}
```

</div>

### <a href="#_2-3-订阅行情" class="header-anchor">#</a> 2.3 订阅行情

客户端订阅请求

<div class="language- extra-class">

``` language-text
{
    "op": "sub",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号
    "topiclist": ["$type.$market.$code",...] // 示例:["rt.hk.00700", "tk.hk.00700","ob.hk.00700"]
}
```

</div>

服务端订阅应答

<div class="language- extra-class">

``` language-text
{
    "op": "sub",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号
    "code": 0,  //状态码 成功
    "msg": "success"  //状态描述
}
```

</div>

### <a href="#_2-4-取消订阅" class="header-anchor">#</a> 2.4 取消订阅

客户端取消订阅请求

<div class="language- extra-class">

``` language-text
{
    "op": "unsub",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号
    "topiclist": ["$type.$market.$code",...] // 示例:["rt.hk.00700", "tk.hk.00700","ob.hk.00700"]
}
```

</div>

服务端取消订阅应答

<div class="language- extra-class">

``` language-text
{
    "op": "unsub",
    "ts": 1575531634,  //unix 时间戳
    "reqId": 666666,  //unix 请求序列号
    "code": 0,  //状态码 成功
    "msg": "success"  //状态描述
}
```

</div>

### <a href="#_2-5-行情推送" class="header-anchor">#</a> 2.5 行情推送

订阅成功之后，服务端会主动推送实时行情

<div class="language- extra-class">

``` language-text
{
    "op": "update",
    "topic": "$type.$market.$code", //内容所属topic
    "data": {}  //更新内容，base64编码，根据实时，tick等具体业务定
}
```

</div>

## <a href="#_3-推送数据结构" class="header-anchor">#</a> 3. 推送数据结构

### <a href="#_3-1-实时行情" class="header-anchor">#</a> 3.1 实时行情

实时行情响应字段说明

| 参数名      | 类型   | 说明                                |
|:------------|:-------|-------------------------------------|
| market      | string | 市场标识                            |
| symbol      | string | 证券代码                            |
| latestPrice | double | 最新价                              |
| open        | double | 开盘价                              |
| low         | double | 最低价                              |
| close       | double | 收盘价                              |
| high        | double | 最高价                              |
| latestTime  | int64  | 最近行情时间                        |
| preClose    | double | 昨收价                              |
| turnOver    | double | 总成交额                            |
| volume      | int64  | 总成交量                            |
| bidPrice    | double | 买一价                              |
| bidSize     | int64  | 买一量                              |
| askPrice    | double | 卖一价                              |
| askSize     | int64  | 卖一量                              |
| upLimit     | double | 涨停价                              |
| downLimit   | double | 跌停价                              |
| qtyUnit     | double | 实时价差                            |
| trdStatus   | int32  | 证券状态,具体参见下方的证券状态说明 |

实时响应示例：

<div class="language- extra-class">

``` language-text
{
    "market": "sz",
    "symbol": "000001",
    "latestTime": 20191226103118000,
    "latestPrice": 16.43,
    "open": 16.34,
    "close": 0,
    "high": 16.48,
    "low": 16.34,
    "preClose": 16.3,
    "volume": 11858618,
    "turnOver": 194666461.75,
    "askPrice": 16.43,
    "askSize": 8103,
    "bidPrice": 16.42,
    "bidSize": 48300,
    "trdStatus": 6
}
```

</div>

### <a href="#_3-2-tick行情" class="header-anchor">#</a> 3.2 tick行情

tick响应说明

| 参数名    | 类型   | 说明                                                                               |
|:----------|:-------|------------------------------------------------------------------------------------|
| seq       | int32  | 行情序号                                                                           |
| time      | int64  | 行情时间                                                                           |
| price     | double | 价格                                                                               |
| volume    | double | 成交量                                                                             |
| direction | double | 买卖方向， 0: 默认，1：买，2：卖                                                   |
| trdType   | int64  | 逐笔类型，港股所特有，数值与类型之间的对应关系为：4:P 22:M 100:Y 101:X 102:D 103:U |

tick响应示例:

<div class="language- extra-class">

``` language-text
{
    "market": "sz",
    "symbol": "000002",
    "seq": 1,
    "time": 20191226103118000,
    "price": 31.25,
    "volume": 4600,
    "direction": 2,
    "trdType": 0
}
```

</div>

### <a href="#_3-3-买卖盘" class="header-anchor">#</a> 3.3 买卖盘

买卖盘说明

| 参数名        | 类型   | 说明           |
|:--------------|:-------|----------------|
| bidPrice      | double | 买盘价         |
| bidVolume     | int64  | 买盘量         |
| bidOrderCount | int64  | 买委托订单个数 |
| askPrice      | double | 卖盘价         |
| askVolume     | int64  | 卖盘量         |
| askOrderCount | int64  | 卖委托订单个数 |

响应示例:

<div class="language- extra-class">

``` language-text
[
    {
        "bidPrice": 9.31,
        "bidVolume": 12000,
        "bidOrderCount": 5,
        "askPrice": 9.32,
        "askVolume": 21600,
        "askOrderCount": 3
    }
]
```

</div>

## <a href="#_4-常见错误码定义" class="header-anchor">#</a> 4. 常见错误码定义

| 值     | 说明                   |
|:-------|:-----------------------|
| 0      | 成功                   |
| 800001 | 鉴权失败               |
| 800002 | 参数错误               |
| 800003 | 内部错误               |
| 800004 | 订阅/取消订阅topic超限 |
| 800005 | 非法请求               |
| 800006 | token正在使用中        |
| 800007 | topic格式错误          |
| 800008 | token被占用            |

## <a href="#_5-接口限制" class="header-anchor">#</a> 5. 接口限制

1.  订阅请求限制每秒最多能订阅10个topic
2.  订阅请求限制最大订阅topic数为10
3.  取消订阅限制每秒最多能取消订阅10个topic

## <a href="#_6-市场标识" class="header-anchor">#</a> 6. 市场标识

| 值  | 说明     |
|:----|:---------|
| hk  | 香港市场 |
| us  | 美股市场 |
| sh  | 上海市场 |
| sz  | 深圳市场 |

## <a href="#_7-行情类型" class="header-anchor">#</a> 7. 行情类型

| 值  | 说明               |
|:----|:-------------------|
| rt  | realtime, 实时行情 |
| tk  | tick, 逐笔成交     |
| ob  | orderbook, 买卖盘  |

## <a href="#_8-证券状态说明" class="header-anchor">#</a> 8. 证券状态说明

| 取值 | 说明          |
|:-----|:--------------|
| 0    | 未知          |
| 1    | 停牌          |
| 2    | 港股波动中断  |
| 3    | 未上市        |
| 4    | 暂停上市(A股) |
| 5    | 退市          |
| 6    | 交易中        |

</div>
