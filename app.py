import os
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 環境変数からキーを読み込む
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# ランダムメッセージ
messages = [
    "おはよう！",
    "今日もがんばって！",
    "おつかれさま！",
    "ひとやすみしよ〜",
    "いい天気だね"
]

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    random_msg = random.choice(messages)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=random_msg)
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway用
    app.run(host="0.0.0.0", port=port)
