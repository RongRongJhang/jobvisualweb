# 職缺訊息視覺化網站
該專案為研究室專案實作考核項目，以 Django 框架為基底開發一個職缺訊息視覺化網站。首先透過網頁爬蟲技術從 104 人力銀行爬取資訊類職缺資料並儲存至 MySQL 資料庫，接著運用 Highcharts 函式庫生成多樣化的統計圖表，直觀呈現職缺分布與趨勢。

![](https://meee.com.tw/OjFwpYc)

## 工作log
### 03/13 -03/18
◆ 安裝並設定Docker環境 </br>
◆ 安裝並設定MySQL環境

---

### 03/20
◆ 資料遷移

---

### 03/21 - 03/24
◆ 網頁模板切版
- base.html
- table.html

---

### 03/27 - 03/30
◆ 網頁模板切版
- wordcloud.html
- piechart.html
- lollipopchart.html

---

### 04/17 - 04/20
◆ 104人力銀行爬蟲改寫成專案API </br>
◆ Table頁面新增"更新Table"按鈕，點擊後觸發爬蟲API
