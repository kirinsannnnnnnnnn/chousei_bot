from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent,
    SourceUser, SourceGroup, SourceRoom,
    QuickReply, QuickReplyButton,
    MessageAction, CameraAction, LocationAction, PostbackAction, 
    DatetimePickerAction
)

from .MODE import MODE, Session_interface
import time, random
from datetime import datetime as dt
from repository import repository as repo
from repository import service as serv

# TODO: flaskのconf使いこなしてこういう定数をいい感じで扱う
# もしくはinit.pyでglobalに入れちゃうとか https://github.com/colorfultalk/ct_prototype/blob/master/init.py
BOT_NAME = "アルバ"
THRESHOLD_WEIGHT = 5 # これをもうちょっと考える

# ここから動作確認 ######################################
waiting_mode = Session_interface.get_waiting_mode(user_id="test_user_id1234")
print(1, "in onboard: ", waiting_mode)
Session_interface.set_waiting_mode(user_id="test_user_id1234", mode="init in onboarding")
waiting_mode = Session_interface.get_waiting_mode(user_id="test_user_id1234")
print(2, "in onboard: ", waiting_mode)
# ここまで動作確認 ######################################

def dur():
  time.sleep(0) # TODO: ここを1に戻す

def handle_follow_event(event=None, line_bot_api=None):
    user_id = event.source.user_id
    dur()
    _text = "数あるダイエットサービスの中から選んでもらえてくれしいです。"
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
    dur()
    _text = "あなたの最適なパートナーになれるように頑張ります♪これからよろしくお願いします♪"
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
    dur()
    _text = "まずは、あなたのことを知りたいです！性別を教えてください！"
    Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.AFTER_SEX)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
      quick_reply=QuickReply(
              items=[
                QuickReplyButton(action=PostbackAction(label="男性", data=MODE.AFTER_SEX.hash+"&男性", text="男性")),
                QuickReplyButton(action=PostbackAction(label="女性", data=MODE.AFTER_SEX.hash+"&女性", text="女性")),
                QuickReplyButton(action=PostbackAction(label="その他", data=MODE.AFTER_SEX.hash+"&その他", text="その他"))
              ]
          )))

def after_sex(event=None, line_bot_api=None):
    user_id = event.source.user_id

    postback = getattr(event, "postback", None)
    if postback is not None:
      _sex = postback.data.split("&")[1]
      print(_sex)
      repo.insert_into_users_sex(user_id, _sex)

      _text = "ありがとうございます★"
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
      dur()
      _text = "生年月日はもちろん非公開にしますから安心してくださいね。"
      Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.AFTER_BIRTHDATE)
      line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
        quick_reply=QuickReply(
                items=[
                QuickReplyButton(action=DatetimePickerAction(
                  label="日付を選んでね！", 
                  data=MODE.AFTER_BIRTHDATE.hash,
                  mode="date",
                  initial="1990-01-01",
                  min="1950-01-01",
                  max="2017-12-31"
                  ))
                ]
            )))

def after_birthdate(event=None, line_bot_api=None):
    user_id = event.source.user_id

    postback = getattr(event, "postback", None)
    if postback is not None:
      _birth_date = postback.params["date"]
      repo.update_users(user_id, "birth_date", _birth_date)
      
      _text = "ここから少しキーボードを使って入力してください。\n左下のキーボードアイコンから開いてください♪"
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
      dur()
      _text = "まずはユーザー登録をお願いします。"
      line_bot_api.push_message(user_id, TextSendMessage(text=_text))
      dur()
      _text = "最初はメールアドレスを教えてね♪"
      Session_interface.set_waiting_mode(user_id, MODE.AFTER_EMAIL)
      line_bot_api.push_message(user_id, TextSendMessage(text=_text))

def after_email(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _email = event.message.text
    repo.update_users(user_id, "email", _email)

    _text = "ありがとう！次は名字(姓)を入力してね"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_SIR_NAME)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))

def after_sir_name(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _sir_name = event.message.text
    repo.update_users(user_id, "sir_name", _sir_name)

    _text = "下の名前(名)をお願い！"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_FIRST_NAME)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))

def after_first_name(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _first_name = event.message.text
    repo.update_users(user_id, "first_name", _first_name)

    _text = "電話番号を数字で入れてね☆ハイフンはいらないよ"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_PHONE)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))

def after_phone(event=None, line_bot_api=None):
    user_id = event.source.user_id
    # _phone = event.message.text
    # repo.update_users(user_id, "phone", _phone)

    _text = "あなたの身長は何cmですか?\n3桁の数字で入力してください！"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_HEIGHT)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))

def after_height(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _height = event.message.text
    repo.update_users(user_id, "height", _height)

    _text = "体重は何kgですか？\nもちろん、わたしとあなただけの秘密です^^"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_WEIGHT)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))


def _get_weight(user_id):
    return repo.select_from_users(user_id, "weight")
def _get_height(user_id):
    return repo.select_from_users(user_id, "height")

def _get_bmi(h, w):
    return w/h/h*10000

def after_weight(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _weight = event.message.text
    repo.update_users(user_id, "weight", _weight)
    repo.insert_weight_into_weight_table(user_id, _weight)

    _text = "教えてくれて、ありがとうございます！"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
    # TODO: _height, _weightをデータベースから取得する関数を実装する
    dur()
    _weight, _height = _get_weight(user_id), _get_height(user_id)
    _bmi = _get_bmi(_height, _weight)
    _text = "今の情報からすると…BMIは{}ですね".format(_bmi)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
    dur()
    _text = "目標体重は何キロですか？"
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_GOAL_WEIGHT)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))

def after_goal_weight(event=None, line_bot_api=None):
    user_id = event.source.user_id
    _goal_weight = event.message.text
    repo.update_users(user_id, "goal_weight", _goal_weight)

    _text = "いつまでに目標を達成したいですか？"
    Session_interface.set_waiting_mode(user_id=user_id, mode=MODE.AFTER_GOAL_DATE)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
      quick_reply=QuickReply(
              items=[
              QuickReplyButton(action=DatetimePickerAction(
                label="日付を選んでね！", 
                data=MODE.AFTER_GOAL_DATE.hash,
                mode="date",
                initial=dt.now().strftime("%Y-%m-%d"),
                min="2018-10-01",
                max="2018-12-31"
                ))
              ]
          )))

def _get_goal_weight(user_id):
    return repo.select_from_users(user_id, "goal_weight")
    return 50  

def _get_goal_date(user_id):
    ret = repo.select_from_users(user_id, "goal_date")
    return dt.strptime(ret, "%Y-%m-%d")

def after_goal_date(event=None, line_bot_api=None):
    user_id = event.source.user_id
    postback = getattr(event, "postback", None)
    if postback is not None:
      _goal_date = postback.params["date"]
      repo.update_users(user_id, "goal_date", _goal_date)

      _goal_dt = _get_goal_date(user_id)
      _goal_weight = _get_goal_weight(user_id)

      _delta_date = _goal_dt - dt.now()
      _delta_weight = _get_weight(user_id) - _goal_weight

      _text = "{delta_date}日で{delta_weight}キロが目標なんですね！".format(
        delta_date=_delta_date.days, delta_weight=_delta_weight)
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
      dur()
      print(2222, _delta_date.days, _delta_weight, _goal_weight, _goal_date)
      if int(10*_delta_weight/(_delta_date.days+0.000001*30))/10.0 < THRESHOLD_WEIGHT:
        _text = "一緒に頑張っていきましょう！"
        Session_interface.set_waiting_mode(user_id, MODE.AFTER_VALID_GOAL)
        line_bot_api.push_message(user_id, TextSendMessage(text=_text))
        after_valid_goal(event=event, line_bot_api=line_bot_api)
      else:
        _text = "目標がハードすぎます。最高でも30日5キロまでにしてください"
        line_bot_api.push_message(user_id, TextSendMessage(text=_text))
        _text = "改めて、目標体重を入力してね"
        Session_interface.set_waiting_mode(user_id, MODE.AFTER_GOAL_WEIGHT)
        line_bot_api.push_message(user_id, TextSendMessage(text=_text))

def after_valid_goal(event=None, line_bot_api=None):
    user_id = event.source.user_id

    _text = "次に{}で達成したいことを教えてくださいね。".format(BOT_NAME)
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_PURPOSE)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
      quick_reply=QuickReply(
              items=[
                QuickReplyButton(action=PostbackAction(label="体重を落としたい", data=MODE.AFTER_PURPOSE.hash+"&体重を落としたい", text="体重を落としたい")),
                QuickReplyButton(action=PostbackAction(label="身体を引き締めたい", data=MODE.AFTER_PURPOSE.hash+"&身体を引き締めたい", text="身体を引き締めたい")),
                QuickReplyButton(action=PostbackAction(label="健康を維持したい", data=MODE.AFTER_PURPOSE.hash+"&健康を維持したい", text="健康を維持したい"))
              ]
          )))

def _get_purpose(user_id):
    return repo.select_from_users(user_id, "purpose")

def after_purpose(event=None, line_bot_api=None):
    user_id = event.source.user_id
    postback = getattr(event, "postback", None)
    if postback is not None:
      _purpose = postback.data.split("&")[1]
      repo.update_users(user_id, "purpose", _purpose)

      _purpose=_get_purpose(user_id)
      _text = "そうなんですね。{}んですね。".format(_purpose)
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
      dur()
      _text = "良いアドバイスができるようにがんばります！"
      line_bot_api.push_message(user_id, TextSendMessage(text=_text))
      dur()
      _text = "これからあなたに合ったアドバイスができるように、もうちょっとあなたのことを教えてくださいね"
      line_bot_api.push_message(user_id, TextSendMessage(text=_text))
      dur()
      _text = "普段運動はしますか？"
      Session_interface.set_waiting_mode(user_id, MODE.AFTER_PREFERENCE1)
      line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
        quick_reply=QuickReply(
                items=[
                  QuickReplyButton(action=PostbackAction(label="はい", data=MODE.AFTER_PREFERENCE1.hash+"&はい", text="はい")),
                  QuickReplyButton(action=PostbackAction(label="いいえ", data=MODE.AFTER_PREFERENCE1.hash+"&いいえ", text="いいえ"))
                ]
            )))

def after_preference1(event=None, line_bot_api=None):
    user_id = event.source.user_id
    postback = getattr(event, "postback", None)
    if postback is not None:
      _is_sports = postback.data.split("&")[1]
      repo.update_users(user_id, "is_sports", _is_sports)
      if _is_sports == "はい":
        is_sports = True
      else:
        is_sports = False

      _text = "オッケー！"
      line_bot_api.reply_message(event.reply_token, TextSendMessage(text=_text))
      dur()
      if is_sports:
        _text = "いつもどこで運動するの？"
        Session_interface.set_waiting_mode(user_id, MODE.AFTER_PREFERENCE2)
        line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
          quick_reply=QuickReply(
                  items=[
                    QuickReplyButton(action=PostbackAction(label="自宅で", data=MODE.AFTER_PREFERENCE2.hash+"&自宅で", text="自宅で")),
                    QuickReplyButton(action=PostbackAction(label="ジムで", data=MODE.AFTER_PREFERENCE2.hash+"&ジムで", text="ジムで")),
                    QuickReplyButton(action=PostbackAction(label="それ以外で", data=MODE.AFTER_PREFERENCE2.hash+"&それ以外", text="それ以外"))
                  ]
              )))
      else:
        Session_interface.set_waiting_mode(user_id, MODE.AFTER_PREFERENCE2)
        after_preference2(event=event, line_bot_api=line_bot_api)

def after_preference2(event=None, line_bot_api=None):
    user_id = event.source.user_id
    postback = getattr(event, "postback", None)
    if postback is not None:
      _place_sports =  postback.data.split("&")[1]
      repo.update_users(user_id, "place_sports", _place_sports)

    _text = "それじゃあ、どうやって目標を達成しようか？"
    _h = MODE.AFTER_PREFERENCE3.hash
    Session_interface.set_waiting_mode(user_id, MODE.AFTER_PREFERENCE3)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
      quick_reply=QuickReply(
              items=[
                QuickReplyButton(action=PostbackAction(label="食事中心", data=_h+"&食事中心", text="食事中心")),
                QuickReplyButton(action=PostbackAction(label="運動中心", data=_h+"&運動中心", text="運動中心")),
                QuickReplyButton(action=PostbackAction(label="どっちも", data=_h+"&どっちも", text="どっちも"))
              ]
          )))

def _get_food_main(user_id):
    ret = repo.select_from_users(user_id, "food_sports")
    if ret in ["食事中心", "どっちも"]:
      return True
    else:
      False

def after_preference3(event=None, line_bot_api=None):
    user_id = event.source.user_id 
    postback = getattr(event, "postback", None)
    if postback is not None:
      _food_sports =  postback.data.split("&")[1]
      repo.update_users(user_id, "food_sports", _food_sports)

      _is_food_main = _get_food_main(user_id)
      if _is_food_main:
        _text = "オススメの食事を送るね♪\n朝食は何時に送る？"
        Session_interface.set_waiting_mode(user_id, MODE.AFTER_PREFERENCE4)
        line_bot_api.push_message(user_id, TextSendMessage(text=_text, 
          quick_reply=QuickReply(
                  items=[
                  QuickReplyButton(action=DatetimePickerAction(
                    label="時間を選んでね！", 
                    data=MODE.AFTER_PREFERENCE4.hash,
                    mode="time",
                    initial="",
                    min="00:00",
                    max="23:59"
                    ))
                  ]
              )))
      else:
        Session_interface.set_waiting_mode(user_id, MODE.LAST)
        last(event=event, line_bot_api=line_bot_api)

def after_preference4(event=None, line_bot_api=None):
    user_id = event.source.user_id
    postback = getattr(event, "postback", None)
    if postback is not None:
      _recom_time_morning = postback.params["time"]
      repo.update_users(user_id, "recom_time_morning", _recom_time_morning)
      print(repo.select_from_users(user_id, "recom_time_morning"))

      _text = "コンビニで買えるダイエットメニューを送るね！"
      Session_interface.set_waiting_mode(user_id, MODE.LAST)
      line_bot_api.push_message(user_id, TextSendMessage(text=_text))
      last(event=event, line_bot_api=line_bot_api)

def last(event=None, line_bot_api=None):
    user_id = event.source.user_id
    dur()
    _text = "質問にたくさん答えてくれてありがとう！\nそれじゃあこれから一緒に頑張っていこうね！\n(→チュートリアル=デモ始める？)"
    Session_interface.set_waiting_mode(user_id, MODE.NULL)
    line_bot_api.push_message(user_id, TextSendMessage(text=_text))
