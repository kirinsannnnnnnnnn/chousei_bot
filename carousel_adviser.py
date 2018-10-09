from models import item_stub
from models.sample_item import SampleItem, VideoItem
from repository import repository
from jinja2 import Environment, FileSystemLoader, select_autoescape
import time
import argparse

# LineDeveloperのチャネル基本設定のタブのYour user IDを入れる
user_id = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
template_env = Environment(
    loader=FileSystemLoader('template/json'),
    autoescape=select_autoescape(['html', 'xml', 'json'])
)

parser = argparse.ArgumentParser(
            prog='ALBA', # プログラム名
            usage='batch program of ALBA', # プログラムの利用方法
            description='description', # 引数のヘルプの前に表示
            epilog='end', # 引数のヘルプの後で表示
            )

def dur():
  time.sleep(5)


def create_carousel(category):
    if category == 'workout':
        item_dict = item_stub.get_videos()
        items = [VideoItem(k, v) for k,v in item_dict.items()]
    elif category == 'recipie':
        item_dict = item_stub.get_recipies()
        items = [VideoItem(k, v) for k,v in item_dict.items()]
    return items


def recommend_training(user_id, slot=None):
    from line_botr import line_bot as lb

    goal_weight = repository.select_from_users(user_id, 'goal_weight')
    if slot is not None:
        diff_weight = int(slot) - int(goal_weight)
        if(diff_weight < 0):
            lb.push_message(user_id, '達成おめでとう！さようなら!')
            return

    lb.push_message(user_id, '今日のレコメンドはこちらの3つ！')
    dur()

    items = create_carousel('workout')
    template = template_env.get_template('training_with_img.json')
    data = template.render(dict(items=items))
    lb.push_carousel_message(user_id, data)
    dur()

    lb.push_message(user_id, '朝に運動をするとで、一日の代謝量が上がるから試してみてね。')
    dur()
    if slot is not None:
        lb.push_message(user_id, '目標の体重まで後{}Kg, 頑張れ！'.format(diff_weight))

def recommend_recipie(user_id, slot=None):
    from line_botr import line_bot as lb
    lb.push_message(user_id, '今日の食事のレコメンドはこちらの3つ！')
    dur()

    items = create_carousel('recipie')
    template = template_env.get_template('training_with_img.json')
    data = template.render(dict(items=items))
    lb.push_carousel_message(user_id, data)
    dur()

    lb.push_message(user_id, '食事に関するyoutubeの動画を送るから、参考にしてね')

if __name__ == '__main__':
    parser.add_argument("-c", "--category",
                        dest="category",
                        required=True,
                        choices=['workout', 'recipie'],
                        type=str)
    parser.add_argument('-uid', "--userid",
                        dest="uid",
                        required=True,
                        type=str)

    args = parser.parse_args()
    if args.category == 'workout':
        recommend_training(args.uid, None)
    elif args.category == 'recipie':
        recommend_recipie(args.uid, None)
