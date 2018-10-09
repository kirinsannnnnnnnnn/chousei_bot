from flask import Flask

app = Flask(__name__)

from line_botr.MODE import Session_interface as sess
sess.set_waiting_mode(user_id="test_user_id1234", mode="first of all")
waiting_mode = sess.get_waiting_mode(user_id="test_user_id1234")
print(0, waiting_mode)

from clovar import clova
from line_botr import line_bot
