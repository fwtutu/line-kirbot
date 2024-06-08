from flask import Flask, request, abort
import config

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import logging
from logging.handlers import RotatingFileHandler
import os

#====== 引入其他檔案中的函數 ======
from message import *
from new import *
from Function import *
#====== 引入其他檔案中的函數 ======

#====== Python 標準庫 ======
import tempfile
import datetime
import time
#====== Python 標準庫 ======

app = Flask(__name__)

# 設定日誌文件的路徑
log_directory = os.path.join(os.path.dirname(__file__), 'logs')
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

log_file = os.path.join(log_directory, 'app.log')

# 設定日誌處理器
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

# Channel Access Token
line_bot_api = LineBotApi(config.line_bot_api)
# Channel Secret
handler = WebhookHandler(config.handler)

userids = config.userids

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # 獲取 X-Line-Signature 標頭的值
    signature = request.headers['X-Line-Signature']
    # 將請求體轉換為文本
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # 處理 webhook 請求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.error("Invalid signature. Request aborted.")
        abort(400)
    return 'OK'

@app.route("/")
def home():
    try:
        msg = request.args.get('msg')   # 獲取網址的 msg 參數
        if msg is not None:
            # 如果有 msg 參數，觸發 LINE Message API 的 push_message 方法
            for userid in userids:
                try:
                    line_bot_api.push_message(userid, TextSendMessage(text=msg))
                    app.logger.info(f"Sent message to {userid}")
                except Exception as e:
                    app.logger.error(f"Error sending message to {userid}: {e}")
            return msg
        else:
            return 'OK'
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return 'Error'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    if '最新合作廠商' in msg:
        app.logger.info("測試日誌")
        message = imagemap_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '最新活動訊息' in msg:
        message = buttons_message()
        line_bot_api.reply_message(event.reply_token, message)
    elif '註冊會員' in msg:
        message = Confirm_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '旋轉木馬' in msg:
        message = Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    elif '圖片畫廊' in msg:
        message = test()
        line_bot_api.reply_message(event.reply_token, message)
    elif '功能列表' in msg:
        message = function_list()
        line_bot_api.reply_message(event.reply_token, message)
    elif '哈囉' in msg:
        app.logger.info("測試日誌")
        message = ImageSendMessage(
            original_content_url="https://p7.itc.cn/q_70/images03/20211124/77486db85fef4cdb9a50a87615b387e4.gif",
            preview_image_url="https://p7.itc.cn/q_70/images03/20211124/77486db85fef4cdb9a50a87615b387e4.gif"
        )
        line_bot_api.reply_message(event.reply_token, message)
    elif '晚餐吃啥' in msg:
        message = [
            ImageSendMessage(
                original_content_url="https://s1.aigei.com/prevfiles/bbbf5c098a8f4a46b9b1f5a8f26099e4.gif?e=1735488000&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:B8n4hi4HLYqgNlDzUPQ_s2ixXc4=",
                preview_image_url="https://s1.aigei.com/prevfiles/bbbf5c098a8f4a46b9b1f5a8f26099e4.gif?e=1735488000&token=P7S2Xpzfz11vAkASLTkfHN7Fw-oOZBecqeJaxypL:B8n4hi4HLYqgNlDzUPQ_s2ixXc4="
            ),
            TextSendMessage("我放棄 你問問兔肉吧")
        ]
        line_bot_api.reply_message(event.reply_token, message)
    elif 'id' in msg:  
        # 獲取使用者的 LINE ID
        user_id = event.source.user_id
        # 記錄日誌
        app.logger.info("測試日誌")
        app.logger.info(f"User sent 'id' message: {msg}. LINE user ID: {user_id}")
        # 在這裡可以進一步處理，比如回覆消息
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f"Your LINE user ID: {user_id}"))
    else:
        message = TextSendMessage(text=msg)   
        line_bot_api.reply_message(event.reply_token, message)

@handler.add(PostbackEvent)
def handle_postback(event):
    app.logger.info(f"Postback data: {event.postback.data}")
    print(event.postback.data)

@handler.add(MemberJoinedEvent)
def welcome(event):
    uid = event.joined.members[0].user_id
    gid = event.source.group_id
    profile = line_bot_api.get_group_member_profile(gid, uid)
    name = profile.display_name
    message = TextSendMessage(text=f'{name} 歡迎加入')
    line_bot_api.reply_message(event.reply_token, message)
    app.logger.info(f"New member joined: {name} ({uid}) in group {gid}")

if __name__ == "__main__":
    print("Current working directory:", os.getcwd())
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
