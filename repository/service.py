from .repository import *
from datetime import datetime as dt
from datetime import timedelta as delta

def get_age(user_id):
  birth_date = select_from_users(user_id, "birth_date")
  return dt.now().year - dt.strptime(birth_date, "%Y-%m-%d").year

def get_elapsed_days(user_id):
  return (dt.now() - dt.strptime(select_from_users(user_id, "registered_date"), "%Y-%m-%d")).days

def get_current_weight_date(user_id):
    weight_list = select_weight_from_weight(user_id)
    return weight_list.pop()

def get_first_weight(user_id):
    return select_from_users(user_id, "weight")

def get_registered_date(user_id):
  rd = select_from_users(user_id, "registered_date")
  return dt.strptime(rd, "%Y-%m-%d")

def get_goal_weight(user_id):
  w = select_from_users(user_id, "goal_weight")
  return w

def delete_weight_table(user_id):
  delete_from_weight(user_id)

def get_all_weight_list(user_id):
  w_list = select_weight_from_weight(user_id)
  return [el[2] for el in w_list]

def get_all_logged_datetime_list(user_id):
  w_list = select_weight_from_weight(user_id)
  dt_list = [dt.strptime(str(el[3]), "%Y%m%d%H%M%S") for el in w_list]
  return dt_list

def get_sex(user_id):
  return select_from_users(user_id, "sex")

def get_goal_date(user_id):
  goal_date = select_from_users(user_id, "goal_date")

  return dt.strptime(goal_date, "%Y-%m-%d")

def get_user_id_list():
  user_id_list = select_user_id_list()
  ret = []
  for el in user_id_list:
    ret.append(el[0])

  return ret

def insert_weight(user_id, weight):
  insert_weight_into_weight_table(user_id, weight)

def get_email(user_id):
  return select_from_users(user_id, "email")

def get_phone(user_id):
  return select_from_users(user_id, "phone")
def get_sir_name(user_id):
  return select_from_users(user_id, "sir_name")

def get_first_name(user_id):
  return select_from_users(user_id, "first_name")

