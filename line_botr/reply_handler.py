from .MODE import MODE, Session_interface
from .video_scraper import scrape_video_urls
from .words_processor import (
  get_youtube_recommend, judgeWhat
)

# ここから動作確認 ######################################
waiting_mode = Session_interface.get_waiting_mode(user_id="test_user_id1234")
print(3, "in rh: ", waiting_mode)
Session_interface.set_waiting_mode(user_id="test_user_id1234", mode="init in rh")
waiting_mode = Session_interface.get_waiting_mode(user_id="test_user_id1234")
print(4, "in rh: ", waiting_mode)
# ここまで動作確認 ######################################

from .onboarding import *
from .insert_weight_line_bot import *
from .sending_customer import *

class Reply_handler:
  def __init__(self, text, event=None, line_bot_api=None):
    self.text = text
    self.mode = judgeWhat(text)
    self.kwargs = {
    "event": event,
    "line_bot_api": line_bot_api
    }

  def get_message(self):
    user_id = self.kwargs["event"].source.user_id
    waiting_mode = Session_interface.get_waiting_mode(user_id)


    if self.mode == MODE.YOUTUBE_RECOMMEND:
      return get_youtube_recommend(self.text)
    elif self.mode == MODE.GOING_TO_GO_TO_GYM:
      return "OK!"
    elif self.mode == MODE.OK_GOOGLE_ERROR:
      return "ん？"
    elif self.mode == MODE.ONBOARDING:
      return "はじめまして。アルバにご登録ありがとうございます。"
    elif self.mode == MODE.INSERT_WEIGHT:
      insert_weight_line_bot(**self.kwargs)
    elif waiting_mode == MODE.AFTER_SEX:
      after_sex(**self.kwargs)
    elif waiting_mode == MODE.AFTER_BIRTHDATE:
      after_birthdate(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PURPOSE:
      after_purpose(**self.kwargs)
    elif waiting_mode == MODE.AFTER_GOAL_DATE:
      after_goal_date(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PREFERENCE1:
      after_preference1(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PREFERENCE2:
      after_preference2(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PREFERENCE3:
      after_preference3(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PREFERENCE4:
      after_preference4(**self.kwargs)


    elif waiting_mode == MODE.AFTER_EMAIL:
      after_email(**self.kwargs)
    elif waiting_mode == MODE.AFTER_SIR_NAME:
      after_sir_name(**self.kwargs)
    elif waiting_mode == MODE.AFTER_FIRST_NAME:
      after_first_name(**self.kwargs)
    elif waiting_mode == MODE.AFTER_PHONE:
      after_phone(**self.kwargs)
    elif waiting_mode == MODE.AFTER_HEIGHT:
      after_height(**self.kwargs)
    elif waiting_mode == MODE.AFTER_WEIGHT:
      after_weight(**self.kwargs)
    elif waiting_mode == MODE.BEFORE_GOAL_WEIGHT:
      before_goal_weight(**self.kwargs)
    elif waiting_mode == MODE.AFTER_GOAL_WEIGHT:
      after_goal_weight(**self.kwargs)
    elif waiting_mode == MODE.AFTER_VALID_GOAL:
      after_valid_goal(**self.kwargs)
    elif waiting_mode == MODE.LAST:
      last(**self.kwargs)

    elif waiting_mode == MODE.AFTER_START_SEND_CUSTOMER:
      after_start_send_customer(**self.kwargs)
    elif waiting_mode == MODE.AFTER_CONFIRM_EMAIL:
      after_confirm_email(**self.kwargs)

    elif self.mode == MODE.NOTHING:
      return "" # TODO: 提出するときはここを変える

  def __repr__(self):
    return "text: {}\nmode: {}".format(
      self.text,
      self.mode.name)
