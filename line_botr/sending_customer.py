from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, 
    FollowEvent, SourceUser, SourceGroup, SourceRoom,
    QuickReply, QuickReplyButton,
    MessageAction, CameraAction, LocationAction, PostbackAction, 
    DatetimePickerAction
)

from .MODE import MODE, Session_interface
import time, random
from datetime import datetime as dt
from repository import service as serv


def push_send_customer(user_id, line_bot_api):
  _text = "体重目標が厳しいペースになっているね。思い通りのダイエットを実施できているかな？"
  line_bot_api.push_message(user_id, TextSendMessage(text=_text))
  _text = "毎日、運動したり食事コントロールするのは大変だよね。"
  line_bot_api.push_message(user_id, TextSendMessage(text=_text))
  _text = "パーソナルトレーニングジムでは、ボディメイクやダイエットを目的に、食事指導や一緒にトレーニングをサポートしてくれたりするので、もし興味があったら、検討してみてね。"
  line_bot_api.push_message(user_id, TextSendMessage(text=_text))
  _text = "一応、RIZAPの無料カウンセリングがあるんだけど、申し込んでおこうか？"
  line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
    quick_reply=QuickReply(
            items=[
              QuickReplyButton(action=PostbackAction(label="はい", data="はい", text="はい")),
              QuickReplyButton(action=PostbackAction(label="いいえ", data="いいえ", text="いいえ")),
            ]
        )))
  Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.AFTER_START_SEND_CUSTOMER)

def after_start_send_customer(event=None, line_bot_api=None):
  user_id = event.source.user_id
  postback = getattr(event, "postback", None)
  if postback is not None:
    _rep = postback.data
  else:
    _rep = None
  if _rep == "はい":
    sir_name = serv.get_sir_name(user_id)
    first_name = serv.get_first_name(user_id)
    _email = serv.get_email(user_id)
    _phone = serv.get_phone(user_id)
    image_message = ImageSendMessage(
            original_content_url='https://user-images.githubusercontent.com/2950262/46664110-f5267180-cbfa-11e8-849f-83d6f3ae543b.png',
            preview_image_url='https://user-images.githubusercontent.com/2950262/46664110-f5267180-cbfa-11e8-849f-83d6f3ae543b.png'
        )
    line_bot_api.push_message(user_id, image_message)
    _text = "名前、メールアドレス、電話番号はあってる？\n名前: {name}\nアドレス: {email}\n電話番号: {phone}".format(
        name=sir_name+" "+first_name, email=_email, phone=_phone)
    Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.AFTER_CONFIRM_EMAIL)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
      quick_reply=QuickReply(
              items=[
                QuickReplyButton(action=PostbackAction(label="はい", data="はい", text="はい")),
                QuickReplyButton(action=PostbackAction(label="いいえ", data="いいえ", text="いいえ")),
              ]
          )))
  elif _rep == "いいえ":
    _text = "そっか…。"
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
    time.sleep(4)
    _text = "解決できなくてごめんね…"
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))

def after_confirm_email(event=None, line_bot_api=None):
  user_id = event.source.user_id
  postback = getattr(event, "postback", None)
  if postback is not None:
    _rep = postback.data
  else:
    _rep = None
  if _rep == "はい":
    _email = serv.get_email(user_id)
    _phone = serv.get_phone(user_id)
    _text = "オッケー！申し込んでおいたよ！"
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
    image_message = ImageSendMessage(
            original_content_url='https://user-images.githubusercontent.com/2950262/46664137-125b4000-cbfb-11e8-988f-b0dd35410407.png',
            preview_image_url='https://user-images.githubusercontent.com/2950262/46664137-125b4000-cbfb-11e8-988f-b0dd35410407.png'
        )
    line_bot_api.push_message(user_id, image_message)
  elif _rep == "いいえ":
    ごめん

