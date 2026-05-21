# uSmart 基础行情开放 API

> Source URL: https://api-doc.usmart8.com/zh-cn/quote-base.html
>
> Fetched: 2026-05-21
>
> Truth source: uSmart official web documentation. Do not replace facts in this file with deleted PDF/MinerU output unless a newer official source is provided.

<div class="theme-default-content content__default">

# 基础行情开放API

## 版本说明

| 日期       | 版本   | 说明                 |
|:-----------|:-------|:---------------------|
| 2019-12-27 | v1.0.0 | 创建                 |
| 2019-02-24 | v1.0.1 | 基础信息接口新增字段 |
| 2019-02-27 | v1.0.1 | 添加接口限制描述     |

## 概述

盈立智投开放平台通过HTTP接口提供大部分服务，大多数API功能都是通过简单的HTTP POST请求访问。关于基础行情的接口都通过统一接口调用。

## 接口请求限制

### 请求频率限制：

-   高频请求

| 接口名称     | 一分钟请求次数限制 |
|--------------|--------------------|
| 实时行情接口 | 120                |
| 分时接口     | 120                |
| K线接口      | 120                |
| 逐笔接口     | 120                |
| 市场状态接口 | 120                |
| 买卖盘接口   | 120                |

-   低频请求

| 接口名称         | 一分钟请求次数限制 |
|------------------|--------------------|
| 证券基本信息接口 | 20                 |

## 统一域名

-   正式域名： https://open-hz.yxzq.com:8443
-   测试域名： https://open-hz-uat.yxzq.com

> 如果在测试调试阶段，下面所有接口地址将`https://open-hz.yxzq.com:8443`改为`https://open-hz-uat.yxzq.com`即可。

## 一、统一HTTP头

### 简要描述

基础行情的接口，每次调用都必须携带一些必要的HTTP头，这些HTTP头及其功能如下所示：

| 参数名        | 必选 | 类型   | 说明                                                                            |
|:--------------|:-----|:-------|---------------------------------------------------------------------------------|
| Content-Type  | 是   | string | 必须包含：application/json                                                      |
| Authorization | 是   | string | 登录成功后返回的鉴权token                                                       |
| X-Channel     | 是   | string | 渠道标识                                                                        |
| X-Lang        | 是   | int    | 语言类型：默认为简体，1：简体，2：繁体，3：英文                                 |
| X-Request-Id  | 是   | string | 长度为19位数字，必须确保唯一用于做幂等防重，推荐使用分布式Snowflake雪花算法生成 |
| X-Time        | 是   | string | unix 时间戳                                                                     |
| X-Sign        | 是   | string | 签名                                                                            |

### 签名说明

X-Sign生成规则：

1.  Authorization、 X-Channel、X-Lang、X-Request-Id、X-Time头字段与body内容**按序**拼接成原始内容rowContent.
2.  使用MD5withRSA算法对rowContent进行摘要、加密生成密文cipherContent
3.  再对密文cipherContent使用safeBase64编码生成X-Sign

## 二、市场状态接口

### 简要描述

用来获取市场状态信息。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/marketstate`

### 请求方式

-   POST

### 请求参数

| 参数名 | 必选 | 类型   | 说明                                             |
|:-------|:-----|:-------|--------------------------------------------------|
| market | 是   | string | 市场标识，hk：香港，us：美国，sh：上海，sz：深圳 |

### 返回结果

| 参数名 | 类型     | 说明                                 |
|:-------|:---------|--------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败      |
| msg    | string   | 消息                                 |
| data   | 字典类型 | 数据区，具体的接口参照具体的行情接口 |

### 市场状态结构说明

| 参数名         | 类型   | 说明                                     |
|:---------------|:-------|------------------------------------------|
| market         | string | 市场标识，入参是什么，这里就会返回什么   |
| desc           | string | 当前市场状态的描述                       |
| tradingDayType | int    | 当前交易日类型，参加下方的交易日类型说明 |
| status         | int    | 当前市场状态，参见下方的市场状态说明     |

### 交易日类型说明

| 取值 | 说明       |
|:-----|:-----------|
| 0    | 非交易日   |
| 1    | 全天交易市 |
| 2    | 上半日市   |
| 3    | 下半日市   |

### 市场状态说明

| 取值 | 说明                                                   |
|:-----|:-------------------------------------------------------|
| 0    | 未知                                                   |
| 1    | 启动、开市前                                           |
| 2    | 开盘集合竞价 9:15-9:25                                 |
| 3    | 暂停 9:25-9:30，港股 09:28 - 09:30                     |
| 4    | 连续竞价 9:30-11:30,13:00-15:00，深交所14:57-15:00除外 |
| 5    | 午间休市 11:30-13:00                                   |
| 6    | 收盘集合竞价 深交所14:57-15:00                         |
| 7    | 已收盘 15:00-7b:00                                     |
| 20   | 输入买卖盘 09:00 - 09:15，港股特有状态                 |
| 21   | 对盘前 09:15 - 09:20，港股特有状态                     |
| 22   | 对盘 09:20 - 09:28，港股特有状态                       |
| 23   | 参考定价，港股收盘集合竞价                             |
| 24   | 输入买卖盘，港股收盘集合竞价                           |
| 25   | 不可取消，港股收盘集合竞价                             |
| 26   | 随机收市，港股收盘集合竞价                             |
| 27   | 对盘，港股收盘集合竞价                                 |
| 31   | 盘前，美股所有                                         |
| 32   | 盘后，美股所有                                         |
| 61   | 盘后撮合，A股科创版                                    |
| 62   | 固定价格交易，A股科创版                                |

### 示例

#### 请求

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/marketstate HTTP/1.1
Content-Type: application/json; charset=utf-8

{"market":"sh"}
```

</div>

#### 结果

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
    "market": "sh",
    "desc": "已收盘",
    "tradingDayType": 1,
    "status": 7
  }
}
```

</div>

## 三、基础信息接口

### 简要描述

获取基本信息的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/basicinfo`

### 请求方式

-   POST

### 请求参数

| 参数名 | 必选 | 类型   | 说明                                             |
|:-------|:-----|:-------|--------------------------------------------------|
| market | 是   | string | 市场标识，hk：香港，us：美国，sh：上海，sz：深圳 |

### 返回结果

| 参数名 | 类型     | 说明                                                       |
|:-------|:---------|------------------------------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败                            |
| msg    | string   | 消息                                                       |
| data   | 字典类型 | 数据区，包含一个逐笔条目的数组，具体参照下面的逐笔条目说明 |

### data结构

| 参数名 | 类型   | 说明                                         |
|:-------|:-------|----------------------------------------------|
| market | string | 证券市场，如：hk、us、sh、sz                 |
| list   | array  | 基础信息列表，每个条目说明参见"基础信息条目" |

### 基础信息条目

| 参数名  | 类型   | 说明                       |
|:--------|:-------|----------------------------|
| symbol  | string | 证券代码                   |
| nameChs | string | 证券中文简称               |
| nameCht | string | 证券繁体简称               |
| nameEn  | string | 证券英语简称               |
| type1   | int32  | 证券类型，详见下方证券类型 |
| lotSize | int32  | 最小委托数量               |

### 证券类型

| 参数名 | 类型  | 说明     |
|:-------|:------|----------|
| 0      | int32 | 未知     |
| 1      | int32 | 股票     |
| 2      | int32 | 基金     |
| 3      | int32 | 期货     |
| 4      | int32 | 债券     |
| 5      | int32 | 衍生证券 |
| 6      | int32 | 指数     |
| 7      | int32 | 外汇     |
| 8      | int32 | 其他     |
| 9      | int32 | 板块     |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/basicinfo HTTP/1.1
Content-Type: application/json; charset=utf-8

{"market":"hk"}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
   "market": "hk",
    "list": [
      {
        "symbol": "21922",
        "nameChs": "腾讯东亚零四沽B",
        "nameCht": "騰訊東亞零四沽B",
        "nameEn": "EATENCT@EP2004B",
        "type1": 5,
        "lotSize": 5000
      },
      {
        "symbol": "29260",
        "nameChs": "银证瑞银零八购A",
        "nameCht": "銀證瑞銀零八購A",
        "nameEn": "UB-CGS @EC2008A",
        "type1": 5,
        "lotSize": 5000
      }
    ]
  }
}
```

</div>

## 四、实时行情接口

### 简要描述

获取实时行情行情数据的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/realtime`

### 请求方式

-   POST

### 请求参数

| 参数名  | 必选 | 类型  | 说明                                                                                     |
|:--------|:-----|:------|------------------------------------------------------------------------------------------|
| secuIds | 是   | array | 字符串数组，每个元素为证券的唯一标识，由市场标识+证券代码构成，如腾讯的唯一标识为hk00700 |

### 返回结果

| 参数名 | 类型     | 说明                                                           |
|:-------|:---------|----------------------------------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败                                |
| msg    | string   | 消息                                                           |
| data   | 字典类型 | 数据区，包含一个list字段，list中对象中的字段含义，参照下方说明 |

### list中的对象数据字段说明

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

### 证券状态说明

| 取值 | 说明           |
|:-----|:---------------|
| 0    | 未知           |
| 1    | 停牌           |
| 2    | 港股波动中断   |
| 3    | 未上市         |
| 4    | 暂停上市 (A股) |
| 5    | 退市           |
| 6    | 交易中         |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/realtime HTTP/1.1
Content-Type: application/json; charset=utf-8

{"secuIds":["hk00700"]}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "latestPrice": 376.8,
        "open": 379,
        "low": 376.8,
        "bidPrice": 376.6,
        "symbol": "00700",
        "close": 376.8,
        "high": 379.8,
        "latestTime": 20191224120822000,
        "preClose": 377.8,
        "turnOver": 2403547632,
        "bidSize": 23100,
        "trdStatus": 6,
        "market": "hk",
        "volume": 6360485,
        "askPrice": 376.8,
        "askSize": 12300
      }
    ]
  }
}
```

</div>

## 五、分时接口

### 简要描述

获取分时数据的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/timeline`

### 请求方式

-   POST

### 请求参数

| 参数名 | 必选 | 类型   | 说明                                                               |
|:-------|:-----|:-------|--------------------------------------------------------------------|
| secuId | 是   | string | 证券的唯一标识，由市场标识+证券代码构成，如腾讯的唯一标识为hk00700 |
| type   | 是   | int    | 分时类型 0：一日分时，1：五日分时                                  |

### 返回结果

| 参数名 | 类型     | 说明                                                       |
|:-------|:---------|------------------------------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败                            |
| msg    | string   | 消息                                                       |
| data   | 字典类型 | 数据区，包含一个分时点结构的数组，具体参见下方的分时点接口 |

### 分时点结构说明

| 参数名     | 类型   | 说明         |
|:-----------|:-------|--------------|
| price      | double | 最新价       |
| avg        | double | 均价         |
| latestTime | int64  | 最近行情时间 |
| preClose   | double | 昨收价       |
| amount     | double | 成交额       |
| volume     | int64  | 成交量       |
| netchng    | double | 涨跌额       |
| pctchng    | double | 涨跌幅       |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/timeline HTTP/1.1
Content-Type: application/json; charset=utf-8

{"secuId":"hk02208","type":0}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
     {
        "latestTime": 20191224093000000,
        "preClose": 8.69,
        "price": 8.7,
        "avg": 8.629,
        "volume": 1400,
        "amount": 12080,
        "netchng": 0.01,
        "pctchng": 0.0012
      }
    ]
  }
}
```

</div>

## 六、K线接口

### 简要描述

获取K线数据的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/kline`

### 请求方式

-   POST

### 请求参数

| 参数名 | 必选 | 类型   | 说明                                                               |
|:-------|:-----|:-------|--------------------------------------------------------------------|
| secuId | 是   | string | 证券的唯一标识，由市场标识+证券代码构成，如腾讯的唯一标识为hk00700 |
| type   | 是   | int32  | K线类型，参见下方的K线类型说明                                     |
| start  | 是   | int64  | 当前页的起始时间，第一页可传0                                      |
| right  | 是   | int32  | 复权类型，0：不复权，1：前复权，2：后复权                          |
| count  | 是   | int32  | 每页大小                                                           |

### K线类型说明

| 取值 | 说明                   |
|:-----|:-----------------------|
| 0    | 默认值，不返回任何数据 |
| 1    | 1分钟K线               |
| 2    | 5分钟K线               |
| 3    | 10分钟K线              |
| 4    | 15分钟K线              |
| 5    | 30分钟K线              |
| 6    | 60分钟K线              |
| 7    | 1日K线                 |
| 8    | 1周K线                 |
| 9    | 1月K线                 |
| 10   | 3月K线                 |
| 11   | 6月K线                 |
| 12   | 一年K线                |

### 返回结果

| 参数名 | 类型     | 说明                                 |
|:-------|:---------|--------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败      |
| msg    | string   | 消息                                 |
| data   | 字典类型 | 数据区，具体的接口参照具体的行情接口 |

### K线结构说明

| 参数名     | 类型   | 说明         |
|:-----------|:-------|--------------|
| open       | double | 开盘价       |
| close      | double | 收盘价       |
| latestTime | int64  | 最近行情时间 |
| preClose   | double | 昨收价       |
| amount     | double | 成交额       |
| volume     | int64  | 成交量       |
| high       | double | 最高价       |
| low        | double | 最低价       |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/kline HTTP/1.1
Content-Type: application/json; charset=utf-8

{"secuId":"sh600001","type":7,"start":0,"count":0,"right":0}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
     {
        "latestTime": 20090716000000000,
        "preClose": 6.6,
        "open": 6.6,
        "close": 6.54,
        "high": 6.7,
        "low": 6.5,
        "volume": 41413014,
        "amount": 272594480
      }
    ]
  }
}
```

</div>

## 七、逐笔接口

### 简要描述

-   获取逐笔数据的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/tick`

### 请求方式

-   POST

### 请求参数

| 参数名        | 必选  | 类型   | 说明                                                                            |
|:--------------|:------|:-------|---------------------------------------------------------------------------------|
| secuId        | 是    | string | 证券的唯一标识，由市场标识+证券代码构成，如腾讯的唯一标识为hk00700              |
| tradeTime     | 是    | int64  | 起始的行情时间，首页可传0，其他分页传递结果中的最后或者最开始的一条的latestTime |
| seq           | 是    | int64  | 起始的行情序号，首页可传0，其他分页传递结果中的最后或者最开始的一条的req        |
| count         | int64 | string | 每页数据的大小                                                                  |
| sortDirection | int32 | string | 排序方向，0：时间逆序，1：时间顺序                                              |

### 返回结果

| 参数名 | 类型     | 说明                                                       |
|:-------|:---------|------------------------------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败                            |
| msg    | string   | 消息                                                       |
| data   | 字典类型 | 数据区，包含一个逐笔条目的数组，具体参照下面的逐笔条目说明 |

### 逐笔条目说明

| 参数名    | 类型   | 说明                                                                               |
|:----------|:-------|------------------------------------------------------------------------------------|
| seq       | int32  | 行情序号                                                                           |
| time      | int64  | 行情时间                                                                           |
| price     | double | 价格                                                                               |
| volume    | int64  | 成交量                                                                             |
| direction | double | 买卖方向， 0: 默认，1：买，2：卖                                                   |
| trdType   | int64  | 逐笔类型，港股所特有，数值与类型之间的对应关系为：4:P 22:M 100:Y 101:X 102:D 103:U |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/tick HTTP/1.1
Content-Type: application/json; charset=utf-8

{"secuId":"sh600001","tradeTime":0,"start":0,"count":0,"sortDirection":0}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
   "market": "hk",
    "symbol": "00001",
    "start": "0",
    "list": [
      {
        "seq": 1202,
        "time": 20191224120820000,
        "price": 74.65,
        "volume": 1000,
        "direction": 0,
        "trdType": 103
      }
    ]
  }
}
```

</div>

## 八、买卖盘接口

### 简要描述

-   获取买卖盘数据的接口。

### 请求URL

-   `https://open-hz.yxzq.com:8443/quotes-openservice/api/v1/orderbook`

### 请求方式

-   POST

### 请求参数

| 参数名 | 必选 | 类型   | 说明                                                               |
|:-------|:-----|:-------|--------------------------------------------------------------------|
| secuId | 是   | string | 证券的唯一标识，由市场标识+证券代码构成，如腾讯的唯一标识为hk00700 |

### 返回结果

| 参数名 | 类型     | 说明                                                                                           |
|:-------|:---------|------------------------------------------------------------------------------------------------|
| code   | int      | 错误码，0表示成功，其他表示失败                                                                |
| msg    | string   | 消息                                                                                           |
| data   | 字典类型 | 数据区，包含一个最新行情时间（latestTime），一个买卖盘条目的数组，具体参照下面的买卖盘条目说明 |

### 买卖盘条目说明

| 参数名        | 类型   | 说明           |
|:--------------|:-------|----------------|
| bidPrice      | double | 买盘价         |
| bidVolume     | int64  | 买盘量         |
| bidOrderCount | int64  | 买委托订单个数 |
| askPrice      | double | 卖盘价         |
| askVolume     | int64  | 卖盘量         |
| askOrderCount | int64  | 卖委托订单个数 |

### 示例

<div class="language- extra-class">

``` language-text
POST /quotes-openservice/api/v1/orderbook HTTP/1.1
Content-Type: application/json; charset=utf-8

{"secuId":"hk00001"}
```

</div>

<div class="language- extra-class">

``` language-text
{
  "code": 0,
  "msg": "success",
  "data": {
   "market": "hk",
    "symbol": "00001",
    "latestTime": 20200109153121000,
    "list": [
      {
         "bidPrice": 9.31,
         "bidVolume": 12000,
         "bidOrderCount": 5,
         "askPrice": 9.32,
         "askVolume": 21600,
         "askOrderCount": 3
       }
    ]
  }
}
```

</div>

## 九、错误码说明

| 错误码 | 含义                   |
|:-------|:-----------------------|
| 806000 | 参数错误               |
| 806100 | 未知错误               |
| 806109 | 权限错误               |
| 806110 | 内部服务错误           |
| 806111 | 非法的证券代码或者市场 |

</div>
