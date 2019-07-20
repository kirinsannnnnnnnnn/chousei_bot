import sqlite3, time
from contextlib import closing
from datetime import datetime as dt
from datetime import timedelta as delta

# 参考: https://qiita.com/mas9612/items/a881e9f14d20ee1c0703

type_dict = {
  "TEXT": "TEXT",
  "INTEGER": "INTEGER",
  "DATE": "TEXT",
  "DATETIME": "TEXT",
  "REAL": "REAL",
  "TIME": "TEXT"
}

col_type_dict = {
  "user_id": "TEXT",
  "sex": "TEXT",
  "registered_date": "DATE",
  "birth_date": "DATE",
  "email": "TEXT",
  "sir_name": "TEXT",
  "first_name": "TEXT",
  "phone": "TEXT",
  "weight": "REAL",
  "height": "REAL",
  "first_weight": "REAL",
  "goal_weight": "REAL",
  "goal_date": "DATE",
  "purpose": "TEXT",
  "food_sports": "TEXT",
  "is_sports": "TEXT",
  "place_sports": "TEXT",
  "recom_time_morning": "TIME",
  "interesting": "TEXT"
}

table_name_dict = {"USER_TABLE_NAME": "users_table",
  "WEIGHT_TABLE_NAME": "weight_table",
}

default_value_dict = {"default_birth_date": "'1900-01-01'",
  "default_purpose": "'undefined purpose'",
  "default_height": "99999999.0",
  "default_weight": "99999999.0",
  "default_first_weight": "10000",
  "default_goal_weight": "0",
  "default_goal_date": "'2100-01-01'",
  "default_interesting": "'undefined interesting'",
  "default_food_sports": "food",
  "default_is_sports": "はいえ",
  "default_place_sports": "どこかで",
  "default_recom_time_morning": "'10:00'",
  "default_text": "'this is not defined'"
}

sql_dict = {}
sql_dict.update(type_dict)
sql_dict.update(table_name_dict)
sql_dict.update(default_value_dict)


DB_PATH = "./repository/sqlite.db"

# create時のみ実行
# main.pyを起動するときにでもやる？
#### create ####
def create_table(path=None):
    path = DB_PATH if path is None else path
    with closing(sqlite3.connect(path)) as con:
        con.execute(
            str("CREATE TABLE IF NOT EXISTS " + \
            "{USER_TABLE_NAME}" + \
            "(user_id {TEXT} PRIMARY KEY, " + \
            "sex {TEXT}, " + \
            "registered_date {DATE}, " + \
            "birth_date {DATE} DEFAULT {default_birth_date}, " + \
            "email {TEXT} DEFAULT {default_text}, " + \
            "sir_name {TEXT} DEFAULT {default_text}, " + \
            "first_name {TEXT} DEFAULT {default_text})").format(**sql_dict))

        con.execute(
              str("CREATE TABLE IF NOT EXISTS " + \
              "{GROUP_TABLE_NAME}" + \
              "(log_id {INTEGER} PRIMARY KEY AUTOINCREMENT," + \
              "user_id {TEXT}, " + \
              "user_weight {REAL}, " + \
              "logged_date {INTEGER})").format(**sql_dict))

        con.commit()

#### insert ####

def _get_timestamp():
    return int(dt.now().strftime("%Y%m%d%H%M%S"))

def insert_weight_into_weight_table(user_id, weight, timestamp=None):
    timestamp = _get_timestamp() if timestamp is None else timestamp
    query =  str("INSERT INTO weight_table (user_id, user_weight, logged_date) " + \
                 "VALUES (?,?,?)")
    print(query)
    with closing(sqlite3.connect(DB_PATH)) as con:
        con.execute(query, (user_id, weight, timestamp))
        con.commit()

def update_users(user_id, value_name, value):
  if col_type_dict[value_name] in ["DATE", "TEXT", "TIME"]:
    query = str("UPDATE {USER_TABLE_NAME} SET {value_name}='{value}' " + \
        "WHERE user_id = '{user_id}'").format(
        **sql_dict, value_name=value_name, value=value, user_id=user_id)
  else:
    query = str("UPDATE {USER_TABLE_NAME} SET {value_name}={value} " + \
        "WHERE user_id = '{user_id}'").format(
        **sql_dict, value_name=value_name, value=value, user_id=user_id)    
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    con.execute(query)
    con.commit()

def insert_into_users_sex(user_id, value, registered_date=None):
  registered_date = dt.now().strftime("%Y-%m-%d") if registered_date is None else registered_date.strftime("%Y-%m-%d")
  query = str("INSERT INTO {USER_TABLE_NAME} (user_id, {value_name}, registered_date) " + \
      "VALUES (?,?,?)").format(**sql_dict, value_name="sex")
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    con.execute(query, (user_id, value, registered_date))
    con.commit()

#### select ####

def select_from_users(user_id, value_name):
  # query = "SELECT {value_name} FROM {USER_TABLE_NAME} WHERE user_id = {user_id}".format(**sql_dict, value_name=value_name, user_id=user_id)
  query = "SELECT {value_name} FROM {USER_TABLE_NAME} WHERE user_id='{user_id}'".format(
                                          **sql_dict, value_name=value_name, user_id=user_id)
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    ret = con.execute(query).fetchall()
    print(ret)
    return ret[0][0]

def select_user_id_list():
  query = "SELECT DISTINCT user_id FROM {USER_TABLE_NAME}".format(
                                          **sql_dict)
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    ret = con.execute(query).fetchall()
    print(ret)
    return ret


def select_weight_from_weight(user_id):
  query = "SELECT * FROM {WEIGHT_TABLE_NAME} WHERE user_id='{user_id}'".format(
                                          **sql_dict, user_id=user_id)
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    weight_list = con.execute(query).fetchall()

  return sorted(weight_list, key=lambda x: x[3]) # 新しいのが一番最後

def select_weight_from_weight(user_id):
  query = "SELECT * FROM {WEIGHT_TABLE_NAME} WHERE user_id='{user_id}'".format(
                                          **sql_dict, user_id=user_id)
  print(query)
  with closing(sqlite3.connect(DB_PATH)) as con:
    weight_list = con.execute(query).fetchall()

  return sorted(weight_list, key=lambda x: x[3]) # 新しいのが一番最後

def delete_from_users(user_id):
  query = "DELETE FROM {USER_TABLE_NAME} WHERE user_id='{user_id}'".format(
                                          **sql_dict, user_id=user_id)

  with closing(sqlite3.connect(DB_PATH)) as con:
    con.execute(query).fetchall()
    con.commit()

def delete_from_weight(user_id):
  query = "DELETE FROM {WEIGHT_TABLE_NAME} WHERE user_id='{user_id}'".format(
                                          **sql_dict, user_id=user_id)

  with closing(sqlite3.connect(DB_PATH)) as con:
    con.execute(query).fetchall()
    con.commit()

if __name__ == "__main__":
  import random
  from pprint import pprint
  DB_PATH = './sqlite.db'

  create_table(DB_PATH)

  user_id = str(random.randint(0,1000000))
  insert_into_users_sex(user_id, "女性", registered_date=(dt.now()-delta(days=90)))
  update_users(user_id, "height", 190)
  update_users(user_id, "birth_date", "1988-01-01")


  for i in range(100):
    insert_weight_into_weight_table(user_id, random.randint(50,100))

  a = select_from_users(user_id, "sex")
  print(111, a)

  b = select_weight_from_weight(user_id)
  pprint(b)

  print(select_from_users(user_id, "sex"))

  update_users(user_id, "weight", "80")
  print(select_from_users(user_id, "weight"))

  update_users(user_id, "goal_date", "2018-12-12")
  print(select_from_users(user_id, "goal_date"))
