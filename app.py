import base64
import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from extensions.db import db
from models.user import User
from utils.random_emoji import random_emoji


DB_HOSTNAME = os.getenv('LINE_BOT_DB_HOSTNAME', 'database')
DB_DATABASE = os.getenv('LINE_BOT_DB_DATABASE', 'missue_tracker_linebot')
DB_USERNAME = os.getenv('LINE_BOT_DB_USERNAME', 'miku')
DB_PASSWORD = os.getenv('LINE_BOT_DB_PASSWORD', 'mtpassword')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_DATABASE}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


@app.before_first_request
def init():
    db.create_all()


@app.route('/')
def root():
    return 'Hello Miku!'


@app.route('/callback', methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_follow(event):
    user_id = event.source.user_id

    user = User.find(user_id)
    if not user:
        token = ''
        while True:
            # 產生 token
            for _ in range(10):
                token += random_emoji()

            # 沒有重複就使用
            if not User.find_by_token(User.find_by_token(base64.b64encode(bytes(token, 'utf8')))):
                break
            else:
                token = ''

        user = User(user_id=user_id,
                    token=base64.b64encode(bytes(token, 'utf8')))
        db.session.add(user)
        db.session.commit()

    # 發送回應
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(str(base64.b64decode(user.token), 'utf8')))


if __name__ == "__main__":
    app.run()
