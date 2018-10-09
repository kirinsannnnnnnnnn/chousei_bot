from repository import service as serv 
from repository import repository as repo
from calc import *
from datetime import datetime as dt
from datetime import timedelta as delta
import numpy as np

if __name__ == "__main__":
  DB_PATH = './sqlite.db'
  repo.create_table(DB_PATH)

  import random
  user_id = "test_user_id_in_send_customer1234567890"+str(random.randint(0,1000000))
  # repo.delete_from_users(user_id)
  # serv.delete_weight_table(user_id)
  repo.insert_into_users_sex(user_id, "女性", registered_date=dt(2018,7,1))
  registered_date = serv.get_registered_date(user_id)  

  repo.update_users(user_id, "weight", "80")
  repo.update_users(user_id, "birth_date", "1988-01-01")
  repo.update_users(user_id, "goal_weight", "75")
  repo.update_users(user_id, "goal_date", (registered_date+delta(days=60)).strftime("%Y-%m-%d"))
  print("---test user table: ",repo.select_from_users(user_id, "weight"))

  print("----test weight table----")
  # 理想の体重変化を計算する
  sex = serv.get_sex(user_id)
  age = serv.get_age(user_id)
  goal_date = serv.get_goal_date(user_id)
  goal_days = (goal_date- registered_date).days
  goal_weight = serv.get_goal_weight(user_id)
  first_weight = serv.get_first_weight(user_id)
  N = 15 # serv.get_elapsed_days(user_id)

  ideal_E_in = get_E_in_by_M0_N(sex, age, goal_delta=goal_days, Mf=goal_weight, M0=first_weight)
  ideal_w = get_ideal_series_with_E_in(sex, age, first_weight, N, ideal_E_in)

####################################
  # 実際の体重(テストデータ)を入力する
  # 理想の体重 + ノイズ + 挫折率
  N=15
  fail_rate = 0.0
  for i in range(N):
    timestamp = (registered_date + delta(days=i)).strftime("%Y%m%d%H%M%S")
    real_w = ideal_w[i] + np.random.normal(0, 1) + fail_rate*ideal_w[i]
    repo.insert_weight_into_weight_table(user_id, real_w, timestamp=timestamp)


  _time = serv.get_all_logged_datetime_list(user_id)
  _weight_list = serv.get_all_weight_list(user_id)

  from pprint import pprint

  goal_date = serv.get_goal_date(user_id)
  registered_date = serv.get_registered_date(user_id)
#############################################################################################

  _time = serv.get_all_logged_datetime_list(user_id)
  _time = np.array([float((el-registered_date).days) for el in _time]) # datetime → int
  _weight_list = np.array(serv.get_all_weight_list(user_id))

  print(_time)
  print(_weight_list)
  print(ideal_w)

  a = np.cov(_time, _weight_list)[0][1]/np.var(_time)
  b = np.mean(_weight_list) - a*np.mean(_time)

  print(    ((a*_time+b)[-1] - ideal_w[-1]) / (first_weight - goal_weight)*100 )

  print(serv.get_user_id_list())




