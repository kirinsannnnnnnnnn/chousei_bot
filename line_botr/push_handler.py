from .protein_scraper import get_whey_off_rate
from .MODE import MODE
from .words_processor import get_holiday_message
from .words_processor import (
  get_youtube_recommend, judgeWhat
)

class Push_handler:
  def __init__(self, MODE):
    self.text = ""
    self.mode = judgeWhat(text)
    self.to = ""

  def get_message(self):
    if self.mode == MODE.PUSH_OFF_RATE:    
      # GGのGroupId
      self.to = GG_GID
      return get_whey_off_rate()
    if self.mode == MODE.PUSH_ASK:
      self.to = GG_GID
      return "今日は何時にジム行く？"
    if self.mode == MODE.PUSH_HOLIDAY:
      self.to = GG_GID
      return get_holiday_message()

  def __repr__(self):
    return "text: {}\nmode: {}\nto: {}".format(
      self.text,
      self.mode.name,
      self.to)

if __name__ == "__main__":
  print("-----test start------")
  ph = Push_handler(MODE.PUSH_OFF_RATE)
  print("-----get_reply------")
  print(ph.get_message())
  print("-----print(rh)------")
  print(ph)

  print("-----next start------")
  ph = Push_handler(MODE.PUSH_ASK)
  print("-----get_reply------")
  print(ph.get_message())
  print("-----print(rh)------")
  print(ph)

  print("-----next start------")
  ph = Push_handler(MODE.PUSH_HOLIDAY)
  print("-----get_reply------")
  print(ph.get_message())
  print("-----print(rh)------")
  print(ph)
