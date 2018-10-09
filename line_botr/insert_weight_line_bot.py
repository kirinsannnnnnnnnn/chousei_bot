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

def insert_weight_line_bot(event=None, line_bot_api=None):
  user_id = event.source.user_id
  text = event.message.text
  import re
  pattern=r'([+-]?[0-9]+\.?[0-9]*)'
  weight = re.search(pattern,text).group(0)
  serv.insert_weight(user_id, weight)




