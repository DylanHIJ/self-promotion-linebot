import os
import json
import psycopg2
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', None))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', None))

with open('./msgs.json') as msg_file:
    response_msgs = json.load(msg_file)

with open('./quick_reply.json') as qr_file:
    quick_reply = json.load(qr_file)

welcome_msg =\
"""Oops, Invalid option!

If you would like to know more about me, here are some options for you:
1. Education 
2. History & Experience
3. Projects
4. Skills
(ex: type 1 for eductation)

Or you can send a sticker to get a random sticker in response:)"""

# Listen all post requests from /callback
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

# handle text message
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event): 
    if event.message.text in response_msgs:
        msg = TextSendMessage(text=response_msgs[event.message.text])
        line_bot_api.reply_message(event.reply_token, msg)
    else:
        msg = TextSendMessage(text=welcome_msg, quickReply=quick_reply)
        line_bot_api.reply_message(event.reply_token, msg)

# handle sticker message
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event): 
    sticker = StickerSendMessage(package_id='11537', sticker_id=str(52002734 + random.randint(0, 39)))
    line_bot_api.reply_message(event.reply_token, sticker)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
