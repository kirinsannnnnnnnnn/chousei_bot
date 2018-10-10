from repository import repository as repo 
from datetime import datetime as dt
from datetime import timedelta as delta
from calc import *
import numpy as np
from repository import service as serv 
from line_botr import sending_customer as send_cus
from line_botr import line_bot

def _get_diff_weight_ratio(user_id):
  sex = serv.get_sex(user_id)
  age = serv.get_age(user_id)
  goal_date = serv.get_goal_date(user_id)
  registered_date = serv.get_registered_date(user_id)
  goal_days = (goal_date- registered_date).days
  goal_weight = serv.get_goal_weight(user_id)
  first_weight = serv.get_first_weight(user_id)
  N = serv.get_elapsed_days(user_id)

  _time = serv.get_all_logged_datetime_list(user_id)
  _time = np.array([float((el-registered_date).days) for el in _time]) # datetime → int
  _weight_list = np.array(serv.get_all_weight_list(user_id))

  a = np.cov(_time, _weight_list)[0][1]/np.var(_time)
  b = np.mean(_weight_list) - a*np.mean(_time)

  ideal_E_in = get_E_in_by_M0_N(sex, age, goal_delta=goal_days, Mf=goal_weight, M0=first_weight)
  ideal_w = get_ideal_series_with_E_in(sex, age, first_weight, N, ideal_E_in)

  return ((a*_time+b)[-1] - ideal_w[-1]) / (first_weight - goal_weight)*100 # 百分率

def _is_fail(user_id):
  # 挫折判定
  _diff = _get_diff_weight_ratio(user_id)
  if _diff > 20:
    return True
  else:
    return False

def _send_customer(user_id):
  elapsed_days = serv.get_elapsed_days(user_id)
  if elapsed_days in [15,30]:
    if _is_fail(user_id):
      send_cus.push_send_customer(user_id, line_bot.line_bot_api)
    else:
      comment(user_id)
      
def starting_point():
  user_id_list = serv.get_user_id_list()
  for user_id in user_id_list:
    print(user_id)
    _send_customer(user_id)

if __name__ == "__main__":
  DB_PATH = './sqlite.db'
  repo.create_table(DB_PATH)

  import random
  user_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  if not user_id in serv.get_user_id_list():
    repo.insert_into_users_sex(user_id, "男性", registered_date=dt(2018,10, 9))
    registered_date = serv.get_registered_date(user_id)  

    repo.update_users(user_id, "birth_date", "1988-01-01")
    repo.update_users(user_id, "email", "alba@diet.com")
    repo.update_users(user_id, "phone", "01232345192")
    repo.update_users(user_id, "sir_name", "アルバ")
    repo.update_users(user_id, "first_name", "アル子")
    repo.update_users(user_id, "height", "171")  
    repo.update_users(user_id, "weight", "80")
    repo.update_users(user_id, "goal_weight", "75")
    repo.update_users(user_id, "goal_date", (registered_date+delta(days=60)).strftime("%Y-%m-%d"))

  starting_point()


