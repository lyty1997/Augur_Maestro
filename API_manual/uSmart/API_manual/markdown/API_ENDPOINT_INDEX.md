# 盈立 OpenAPI 接口索引

生成日期：2026-05-15

说明：本索引由转换后的 Markdown 自动抽取，用于快速定位接口；字段、参数、状态码和示例仍需回到对应 Markdown/PDF 页核对。

## 交易開放API接口文檔V1.0-20201029(繁)

- 全文 Markdown：[交易開放API接口文檔V1.0-20201029(繁).md](<交易開放API接口文檔V1.0-20201029(繁).md>)
- 抽取接口数量：32

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 3 | 1.1 管道密碼登錄 | POST | `/user-server/open-api/login` | 102 |
| 5 | 1.2 獲取手機驗證碼 | POST | `/user-server/open-api/send-phone-captcha` | 283 |
| 8 | 1.3 管道驗證碼登錄 | POST | `/user-server/open-api/loginCaptcha` | 473 |
| 11 | 1.4 設置交易密碼 | POST | `/user-server/open-api/set-trade-password` | 665 |
| 13 | 1.5 校驗交易密碼 | POST | `/user-server/open-api/check-trade-password` | 847 |
| 14 | 1.6 重置登錄密碼 | POST | `/user-server/open-api/reset-login-password` | 1013 |
| 17 | 1.7 解鎖交易 | POST | `/user-server/open-api/trade-login` | 1224 |
| 19 | 1.8 獲取交易解鎖狀態 | POST | `/user-server/open-api/get-trade-status` | 1395 |
| 21 | 1.9 修改交易密碼 | POST | `/user-server/open-api/update-trade-password` | 1595 |
| 23 | 1.10 重置交易密碼 | POST | `/user-server/open-api/reset-trade-password` | 1776 |
| 25 | 1.11 修改登陸密碼 | POST | `/user-server/open-api/update-login-password` | 1958 |
| 27 | 2.1 下單 | POST | `/stock-order-server/open-api/entrust-order` | 2128 |
| 30 | 2.2 委託改單/撤單 | POST | `/stock-order-server/open-api/modify-order` | 2443 |
| 32 | 2.3 改單範圍 | POST | `/stock-order-server/open-api/modified-range` | 2683 |
| 34 | 2.4 碎股下單 | POST | `/stock-order-server/open-api/odd-entrust` | 2872 |
| 35 | 2.5 碎股撤單 | POST | `/stock-order-server/open-api/odd-modify` | 2966 |
| 37 | 2.6 最大可買、可賣數量 | POST | `/stock-order-server/open-api/trade-quantity` | 3144 |
| 39 | 2.7 今日訂單-分頁查詢 | POST | `/stock-order-server/open-api/today-entrust` | 3368 |
| 42 | 2.8 全部訂單-分頁查詢 | POST | `/stock-order-server/open-api/his-entrust` | 3723 |
| 46 | 2.9 查詢訂單明細 | POST | `/stock-order-server/open-api/order-detail` | 4128 |
| 50 | 2.10 查詢成交流水-分頁查詢 | POST | `/stock-order-server/open-api/stock-record` | 4596 |
| 54 | 2.11 查詢持倉 | POST | `/stock-order-server/open-api/stock-holding` | 4975 |
| 56 | 2.12 查詢資產 | POST | `/stock-order-server/open-api/stock-asset` | 5195 |
| 58 | 2.13 客戶股票資產查詢批量 | POST | `/stock-order-server/open-api/stock-asset-list` | 5447 |
| 67 | 2.14 查詢聚合資產資訊 | POST | `/aggregation-server/open-api/user-asset-aggregation/v1` | 5974 |
| 70 | 3.1 獲取 IPO 列表-分頁查詢 | POST | `/stock-order-server/open-api/ipo-list` | 6249 |
| 74 | 3.2 獲取新股詳細資訊 | POST | `/stock-order-server/open-api/ipo-info` | 6685 |
| 80 | 404 Not Found | POST | `/stock-order-server/open-api/apply-ipo` | 7339 |
| 82 | 404 Not Found | POST | `/stock-order-server/open-api/modify-ipo` | 7542 |
| 84 | 3.5 獲取客戶 ipo 申購清單-分頁查詢 | POST | `/stock-order-server/open-api/ipo-record-list` | 7730 |
| 88 | 3.6 獲取客戶 ipo 申購明細 | POST | `/stock-order-server/open-api/ipo-record` | 8153 |
| 92 | 4.1 查詢匯率 | POST | `/stock-capital-server/open-api/currency-exchange-info` | 8576 |

## 基礎報價開放API(繁)_20201029

- 全文 Markdown：[基礎報價開放API(繁)_20201029.md](<基礎報價開放API(繁)_20201029.md>)
- 抽取接口数量：7

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 3 | ⼀、市場狀態接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/marketstate` | 124 |
| 6 | ⼆、基礎資訊接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/basicinfo` | 201 |
| 9 | 三、即時報價接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/realtime` | 288 |
| 13 | 四、分時接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/timeline` | 401 |
| 15 | 五、陰陽燭接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/kline` | 478 |
| 18 | 六、逐筆接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/tick` | 579 |
| 20 | 七、買賣盤接口 | POST | `https://open-hz.yxzq.com/quotes-openservice/api/v1/orderbook` | 666 |

## 報價推送(繁)_20201029

- 全文 Markdown：[報價推送(繁)_20201029.md](<報價推送(繁)_20201029.md>)
- 抽取接口数量：8

| 页 | 章节 | 方法 | 接口 / 入口 | Markdown 行 |
|---|---|---|---|---|
| 1 | 2020.02.26 v1.0.0 即時行情新增欄位 | - | `wss://open-hz.yxzq.com/wss/v1` | 29 |
| ? | WebSocket 消息 | WS | `接入url:` | 29 |
| ? | WebSocket 消息 | WS | `"op": "auth"` | 63 |
| ? | WebSocket 消息 | WS | `"op": "sub"` | 87 |
| ? | WebSocket 消息 | WS | `"op": "unsub"` | 106 |
| ? | WebSocket 消息 | WS | `"op": "update"` | 126 |
| ? | WebSocket 消息 | WS | `"op": "ping"` | 46 |
| ? | WebSocket 消息 | WS | `"op": "pong"` | 54 |
