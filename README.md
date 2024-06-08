# LINE Bot 專案

這是一個簡單的 LINE 機器人，使用 Flask 和 LINE Messaging API 實現。該機器人根據收到的不同訊息回應相應的內容。

## 功能

- 根據特定關鍵字回應不同訊息
- 透過 URL 參數觸發推送訊息
- 處理新成員加入事件並發送歡迎訊息

## 安裝與設定

### 先決條件

- Python 3.x
- Flask
- line-bot-sdk

### 安裝步驟

1. 克隆此專案：

    ```sh
    git clone https://github.com/your-repo/line-bot.git
    cd line-bot
    ```

2. 創建並啟動虛擬環境：

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. 安裝所需套件：

    ```sh
    pip install -r requirements.txt
    ```

### 環境設置

1. 將您的 LINE Channel Access Token 和 Channel Secret 替換到程式碼中相應的位置：

    ```python
    line_bot_api = LineBotApi('YOUR_CHANNEL_ACCESS_TOKEN')
    handler = WebhookHandler('YOUR_CHANNEL_SECRET')
    ```

## 使用方法

### 啟動伺服器

1. 啟動 Flask 伺服器：

    ```sh
    python app.py
    ```

2. 伺服器將在預設的 `http://0.0.0.0:5000` 運行。您可以通過這個網址訪問您的機器人服務。

### 發送訊息

- 在 LINE 機器人中發送以下文字可以觸發相應的回應：
  - `最新合作廠商`：回應圖片地圖訊息。
  - `最新活動訊息`：回應按鈕模板訊息。
  - `註冊會員`：回應確認模板訊息。
  - `旋轉木馬`：回應旋轉木馬模板訊息。
  - `圖片畫廊`：回應圖片畫廊訊息。
  - `功能列表`：回應功能列表訊息。
  - `哈囉`：回應圖片訊息。
  - `晚餐吃啥`：回應圖片和文字訊息。

- 通過瀏覽器訪問 `http://localhost:5000/?msg=您的訊息` 可以觸發推送訊息到指定的用戶。

### 事件處理

- 當有新成員加入時，機器人會發送歡迎訊息給該成員。

#