from flask import Flask, request, jsonify
import cek
import logging
from flaskr import app
from repository import repository
from multiprocessing import Process
# Create a separate logger for this application
logger = logging.getLogger('my_clova_extension')

clova = cek.Clova(
    application_id="com.clova.extension.trainer",
    default_language="ja",
    debug_mode=True)

@app.route('/testc')
def test_clova_serve():
    """疎通確認用
    """
    import socket, os
    html = "<h3>Hello {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "clova"), hostname=socket.gethostname(), visits=9999)

# https://xxxxxxxxxxxx.com/muscleで待つ
@app.route('/clova', methods=['POST'])
def my_service():
    # Forward the request to the Clova Request Handler
    # Just pass in the binary request body and the request header
    # as a dictionary
    body_dict = clova.route(body=request.data, header=request.headers)

    response = jsonify(body_dict)
    # make sure we have correct Content-Type that CEK expects
    response.headers['Content-Type'] = 'application/json;charset-UTF-8'
    return response


@clova.handle.launch
def launch_request_handler(clova_request):

    # You can answer in different languages within one response
    welcome_japanese = cek.Message(message="おはよう。もう体重は測った？", language="ja")

    response = clova.response([
        welcome_japanese
    ])
    return response

"""Yesという返事はここで処理される。"""
@clova.handle.intent("Clova.YesIntent")
def advise_handler(clova_request):
    msg = 'なんキロ だっ た？'
    message_japanese = cek.Message(message=msg, language="ja")
    response = clova.response([message_japanese])
    return response


"""Noという返事はここで処理される。"""
@clova.handle.intent("Clova.NoIntent")
def advise_handler(clova_request):
    response_builder = cek.ResponseBuilder(default_language="ja")
    return response_builder.simple_speech_text(message="じゃあ測り終わったら, また 呼んで ね", language="ja")

"""TrainingQuestionというカスタムインテントに結びついた発言は全てここで処理される"""
@clova.handle.intent("TrainingQuestion")
def advise_handler(clova_request):
    print('request was submitted.')
    message_japanese = cek.Message(message='何をおっしゃっているのかよくわかりません', language="ja")
    # weightに紐づいてるスロットが存在する -> 体重を入力された
    user_id = clova_request.user_id
    slot = clova_request.slot_value("weight")
    if slot is not None:
        print(slot)
        msg = '{}キロですね。了解です。今日の運動のレコメンドを lineに送 った よ！'.format(slot)
        message_japanese = cek.Message(message=msg, language="ja")
        job = Process(target=log_wight, args=(slot,user_id,))
        job.start()

    response = clova.response([message_japanese])
    return response

def log_wight(slot, user_id):
    repository.insert_weight_into_weight_table(user_id, weight=slot)
    import carousel_adviser
    carousel_adviser.recommend_training(user_id, slot)

def _advise_training(slot):
    if "胸筋" in slot:
        message_japanese = cek.Message(message="ベンチプレスをやりましょう", language="ja")
    elif "上腕二頭筋" in slot:
        message_japanese = cek.Message(message="アームカールをやりましょう", language="ja")
    elif "上腕三頭筋" in slot:
        message_japanese = cek.Message(message="トライセプスキックバックをやりましょう", language="ja")
    elif "腹筋" in slot:
        message_japanese = cek.Message(message="クランチをやりましょう", language="ja")
    return message_japanese

@clova.handle.end
def end_handler(clova_request):
    # Session ended, this handler can be used to clean up
    logger.info("Session ended.")

# In case not all intents have been implemented
# the handler falls back to the default handler
@clova.handle.default
def default_handler(request):
    return clova.response("Sorry I don't understand! Could you please repeat?")
