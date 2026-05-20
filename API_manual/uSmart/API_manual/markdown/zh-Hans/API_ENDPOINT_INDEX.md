# 盈立 OpenAPI 接口索引

生成日期：2026-05-15

说明：本索引由转换后的 Markdown 自动抽取，用于快速定位接口；字段、参数、状态码和示例仍需回到对应 Markdown/PDF 页核对。

## 交易开放API接口文档V1.0-20201029(简)

- 全文 Markdown：[交易开放API接口文档V1.0-20201029(简).md](<交易开放API接口文档V1.0-20201029(简).md>)
- 抽取接口数量：32

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 3 | 1.1 渠道密码登录 | POST | `/user-server/open-api/login` | 102 |
| 5 | 1.2 获取手机验证码 | POST | `/user-server/open-api/send-phone-captcha` | 283 |
| 8 | 1.3 渠道验证码登录 | POST | `/user-server/open-api/loginCaptcha` | 473 |
| 11 | 1.4 设置交易密码 | POST | `/user-server/open-api/set-trade-password` | 665 |
| 13 | 1.5 校验交易密码 | POST | `/user-server/open-api/check-trade-password` | 847 |
| 14 | 1.6 重置登录密码 | POST | `/user-server/open-api/reset-login-password` | 1013 |
| 17 | 1.7 解鎖交易 | POST | `/user-server/open-api/trade-login` | 1224 |
| 19 | 1.8 获取交易解鎖状态 | POST | `/user-server/open-api/get-trade-status` | 1395 |
| 21 | 1.9 修改交易密码 | POST | `/user-server/open-api/update-trade-password` | 1595 |
| 23 | 1.10 重置交易密码 | POST | `/user-server/open-api/reset-trade-password` | 1776 |
| 25 | 1.11 修改登陸密码 | POST | `/user-server/open-api/update-login-password` | 1958 |
| 27 | 2.1 下单 | POST | `/stock-order-server/open-api/entrust-order` | 2128 |
| 30 | 2.2 委托改单/撤单 | POST | `/stock-order-server/open-api/modify-order` | 2443 |
| 32 | 2.3 改单範圍 | POST | `/stock-order-server/open-api/modified-range` | 2683 |
| 34 | 2.4 碎股下单 | POST | `/stock-order-server/open-api/odd-entrust` | 2872 |
| 35 | 2.5 碎股撤单 | POST | `/stock-order-server/open-api/odd-modify` | 2966 |
| 37 | 2.6 最大可买、可卖数量 | POST | `/stock-order-server/open-api/trade-quantity` | 3144 |
| 39 | 2.7 今日订单-分页查询 | POST | `/stock-order-server/open-api/today-entrust` | 3368 |
| 42 | 2.8 全部订单-分页查询 | POST | `/stock-order-server/open-api/his-entrust` | 3723 |
| 46 | 2.9 查询订单明細 | POST | `/stock-order-server/open-api/order-detail` | 4128 |
| 50 | 2.10 查询成交流水-分页查询 | POST | `/stock-order-server/open-api/stock-record` | 4596 |
| 54 | 2.11 查询持倉 | POST | `/stock-order-server/open-api/stock-holding` | 4975 |
| 56 | 2.12 查询资产 | POST | `/stock-order-server/open-api/stock-asset` | 5195 |
| 58 | 2.13 客户股票资产查询批量 | POST | `/stock-order-server/open-api/stock-asset-list` | 5447 |
| 67 | 2.14 查询聚合资产信息 | POST | `/aggregation-server/open-api/user-asset-aggregation/v1` | 5974 |
| 70 | 3.1 获取 IPO 列表-分页查询 | POST | `/stock-order-server/open-api/ipo-list` | 6249 |
| 74 | 3.2 获取新股詳細信息 | POST | `/stock-order-server/open-api/ipo-info` | 6685 |
| 80 | 404 Not Found | POST | `/stock-order-server/open-api/apply-ipo` | 7339 |
| 82 | 404 Not Found | POST | `/stock-order-server/open-api/modify-ipo` | 7542 |
| 84 | 3.5 获取客户 ipo 申購清单-分页查询 | POST | `/stock-order-server/open-api/ipo-record-list` | 7730 |
| 88 | 3.6 获取客户 ipo 申購明細 | POST | `/stock-order-server/open-api/ipo-record` | 8153 |
| 92 | 4.1 查询汇率 | POST | `/stock-capital-server/open-api/currency-exchange-info` | 8576 |

## 基础报价开放API(简)_20201029

- 全文 Markdown：[基础报价开放API(简)_20201029.md](<基础报价开放API(简)_20201029.md>)
- 抽取接口数量：7

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 3 | 一、市場状态接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/marketstate` | 124 |
| 6 | 二、基础信息接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/basicinfo` | 201 |
| 9 | 三、即时报价接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/realtime` | 288 |
| 13 | 四、分时接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/timeline` | 401 |
| 15 | 五、陰陽燭接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/kline` | 478 |
| 18 | 六、逐筆接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/tick` | 579 |
| 20 | 七、买卖盤接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/orderbook` | 666 |

## 报价推送(简)_20201029

- 全文 Markdown：[报价推送(简)_20201029.md](<报价推送(简)_20201029.md>)
- 抽取接口数量：8

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 1 | 2020.02.26 v1.0.0 即时行情新增字段 | - | `wss://open-hz.yxzq.com/wss/v1` | 29 |
| ? | WebSocket 消息 | WS | `接入url:` | 29 |
| ? | WebSocket 消息 | WS | `"op": "auth"` | 63 |
| ? | WebSocket 消息 | WS | `"op": "sub"` | 87 |
| ? | WebSocket 消息 | WS | `"op": "unsub"` | 106 |
| ? | WebSocket 消息 | WS | `"op": "update"` | 126 |
| ? | WebSocket 消息 | WS | `"op": "ping"` | 46 |
| ? | WebSocket 消息 | WS | `"op": "pong"` | 54 |
