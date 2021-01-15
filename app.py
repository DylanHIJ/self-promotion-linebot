import os
import psycopg2
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN', None))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET', None))

response_msgs= {
    "1": """
         National Taiwan University, Sep. 2017 ~ Jun. 2021 (Expected) \n
         B.S., Computer Science and Information Engineering
         """,
    "2": """
         - DBS Bank, Taiwan - IT Intern
         - Shopee Taiwan I’m the Best Coder! Challenge 2020 - 3rd Place 
         - Digital Speech Processing Laboratory, National Taiwan University - Undergraduate Researcher 
         - Freshman ACM Contest in NTU CSIE - 6th Place
         - Changhua Alumni Association, National Taiwan University - Director 
         - Academic Dept., 2018 CSIE Night - Frontend Web Developer
         """,
    "3": """
         - New York Times Bilingual News Crawler (Using Python)
         - Implementation of Shading and Transformation (Using WebGL)
         - Machine Learning Competitions on Kaggle (Mainly using PyTorch)
         """,
    "4": """
         - C/C++
         - Python
         - HTML/CSS/Javascript(React.js)
         - Linux/Shell Script
         - Git
         """
}

welcome_msg = """
Oops, Invalid option!

If you would like to know more about me, here are some options for you:
1. Education 
2. History & Experience
3. Projects
4. Skills
(ex: type 1 for eductation)

Or you can send a sticker to get a random sticker in response:)
"""

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
        msg = TextSendMessage(text=welcome_msg)
        line_bot_api.reply_message(event.reply_token, msg)

# handle sticker message
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event): 
    sticker = StickerSendMessage(package_id='11537', sticker_id=str(52002734 + random.randint(0, 39)))
    line_bot_api.reply_message(event.reply_token, sticker)


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

    line_bot_api.push_message(ev)
