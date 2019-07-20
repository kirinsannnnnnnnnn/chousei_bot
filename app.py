from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os
from chouseisan_getter import get_url

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="Spjh9xyndxGlsKiTJNKBqh1iRrLXtXo7xUKXo3rjKfZv6wIFSyUPd7fd9pVUg1o5uHIdyrKZmXCQmpP3AnVQrU0+ZfA5C5MlSd5h18//ldFxpD/9/maBNhgKw2LjQaH/A9fZMHvm+oosgvbIokDQHVGUYhWQfeY8sLGRXgo3xvw="
YOUR_CHANNEL_SECRET="273d68fc84ffcdaf6e45543c245a0fc7"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

@app.route("/make_chousei", methods=["GET"])
def push_send_customer():
    '''送客ロジックが走る
    '''
    n = 2

    event_name = "読書会第{}週目".format(n)
    event_kouho = """7/6(土) 10:00〜
    7/7(日) 10:00〜"""
    event_memo="下記の日程の中からいける日に◯を、行けない日に×を、調整すれば行ける日に△を入力お願いします。"
    chousei_url = get_url(
            event_name=event_name, 
            event_kouho=event_kouho,
            event_memo=event_memo)

    text = """今週の読書会の日程を決めましょう！
下記のURLに予定を入力をお願いしますー！
{}""".format(chousei_url)
sub
    to = "U631f4797dcb994aec61b9e348d0c32bd" # UserIDとか
    line_bot_api.push_message(to, TextSendMessage(text=text))

    return 'OK'

@handler.add(FollowEvent)
def handle_message(event):
    register_userId(event)
    

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
