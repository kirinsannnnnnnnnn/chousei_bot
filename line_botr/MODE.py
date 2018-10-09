from enum import Enum, auto
import hashlib
import sqlite3
from datetime import datetime as dt
from datetime import timedelta as delta
from contextlib import closing

DT_FMT ="%Y-%m-%d-%H-%M-%S-%f"

class MODE(Enum):
  NULL = auto()
  NOTHING = auto()
  YOUTUBE_RECOMMEND = auto()
  OK_GOOGLE_ERROR = auto()
  GOING_TO_GO_TO_GYM = auto()

  PUSH_OFF_RATE = auto()
  PUSH_ASK = auto()
  PUSH_HOLIDAY = auto()

  # 登録時の処理用(オンボーディング)
  ONBOARDING = auto()
  AFTER_SEX = auto()
  AFTER_BIRTHDATE = auto()

  AFTER_EMAIL = auto()
  AFTER_SIR_NAME = auto()
  AFTER_FIRST_NAME = auto()
  AFTER_PHONE = auto()

  AFTER_PURPOSE = auto()

  AFTER_HEIGHT = auto()
  AFTER_WEIGHT = auto()
  BEFORE_GOAL_WEIGHT = auto()
  AFTER_GOAL_WEIGHT = auto()
  AFTER_GOAL_DATE = auto()

  AFTER_VALID_GOAL = auto()

  AFTER_PREFERENCE1 = auto()
  AFTER_PREFERENCE2 = auto()
  AFTER_PREFERENCE3 = auto()
  AFTER_PREFERENCE4 = auto()
  LAST = auto()

  START_SEND_CUSTOMER = auto()
  AFTER_START_SEND_CUSTOMER = auto()
  AFTER_CONFIRM_EMAIL = auto()

  INSERT_WEIGHT = auto()

  @property
  def hash(self):
    return self.name + ": " + \
            hashlib.sha256(self.name.encode("utf-8")).hexdigest()

  @classmethod
  def get_mode_by_hash(cls, hash_text):
    for mode in list(cls):
      if mode.hash == hash_text:
        return mode
    return hash_text


class Session_waiting_mode():
  # 参考: https://qiita.com/umisama/items/2014f8f09cee447c313f
  def __init__(self, user_id=None):
    self.expire_time = delta(seconds=3600) # 1hr経ったらsession捨てる
    # https://www.sqlite.org/inmemorydb.html
    # この書き方でon-memoryかつ複数のdbを区別できる
    self.db_name = "{}.db".format(user_id)
    with closing(sqlite3.connect(self.db_name)) as con:
      con.execute("CREATE TABLE IF NOT EXISTS " + \
        "session_table(timestamp TEXT, mode_hash TEXT)")
      con.execute("INSERT INTO session_table(timestamp, mode_hash) " + \
        "VALUES (?, ?)", (dt.now().strftime(DT_FMT), "initialized in Constructor!!!"))
      con.commit()

  def _set_waiting_mode(self, mode):
    now = dt.now().strftime(DT_FMT)
    if isinstance(mode, MODE):
      _text = mode.hash
    else:
      _text = mode
    with closing(sqlite3.connect(self.db_name)) as con:
      con.execute("INSERT INTO session_table(timestamp, mode_hash) " + \
        "VALUES (?, ?)", (now, _text))
      con.commit()

  def _get_waiting_mode(self):
    with closing(sqlite3.connect(self.db_name)) as con:
      sessions =  con.execute("SELECT timestamp, mode_hash FROM session_table")\
                    .fetchall()
    ret = []
    for sess in sessions:
      ret.append((dt.strptime(sess[0], DT_FMT), sess[1]))
    ret = sorted(ret, key=lambda x: x[0]) # 新しいのが一番最後

    ret_dt, ret_hash = ret.pop() # 最新のを返す
    if (dt.now() - ret_dt) > self.expire_time:
      ret_hash = MODE.NOTHING.hash

    ret_mode = MODE.get_mode_by_hash(ret_hash)

    return ret_mode


class Session_interface():
  """参考: https://blanktar.jp/blog/2016/07/python-singleton.html
  """
  _unique_instace_dict = {}

  def __new__(cls):
    raise NotImplementedError("呼ぶな！！！！！！！")

  @classmethod
  def _get_session(cls, **kwargs):
    if not kwargs["user_id"] in cls._unique_instace_dict:
      cls._unique_instace_dict.update({
        kwargs["user_id"]: Session_waiting_mode(kwargs["user_id"])
        })

    return cls._unique_instace_dict[kwargs["user_id"]]

  @classmethod
  def set_waiting_mode(cls, user_id=None, mode=None):
    session = cls._get_session(user_id=user_id)
    session._set_waiting_mode(mode)

  @classmethod
  def get_waiting_mode(cls, user_id=None):
    session = cls._get_session(user_id=user_id)
    return session._get_waiting_mode()

if __name__ == "__main__":
  """使い方"""

  # user_idにつき一つのDBをオンメモリで作る
  # 同じDBだと別のユーザーが同時アクセスした時に壊れそう

  # 十回アクセスがあって、その度にsessionが保存される感じ
  for i in range(10):
    Session_interface.set_waiting_mode(user_id="test_user_id1234", mode=MODE.NOTHING.hash)
  waiting_mode = Session_interface.get_waiting_mode(user_id="test_user_id1234")
  print(111, waiting_mode)
  # で、本来やりたかった、MODEを見て動作に入るのはこんな感じで
  if waiting_mode == MODE.NOTHING:
    print(222, waiting_mode)


  # ハッシュでmodeを取ってくる
  m = MODE.get_mode_by_hash(MODE.AFTER_SEX.hash)
  print(333, m)