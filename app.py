import os
import psycopg2
import random
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('YOUR_CHANNEL_ACCESS_TOKEN', None))

# Channel Secret
handler = WebhookHandler(os.getenv('YOUR_CHANNEL_SECRET', None))

# URL of databases
database_url = os.getenv('DATABASE_URL', None)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event): 
    promotion = "Hi, I am Dylan.\n I am currently a student in NTUCSIE."
    message.TextSendMessage(text=promotion)
    line_bot_api.reply_message(event.reply_token, message)

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     message = TextSendMessage(text=event.message.text)
#     line_bot_api.reply_message(event.reply_token, message)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event): 
    sticker = StickerSendMessage(package_id='11537', sticker_id=str(52002734 + random.randint(0, 39)))
    line_bot_api.reply_message(event.reply_token, sticker)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
