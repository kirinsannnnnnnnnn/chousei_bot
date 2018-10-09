from random import choices, sample
from .video_scraper import scrape_video_urls
import sys, os
from .MODE import MODE
import datetime


def get_youtube_recommend(text):
    queries = text.split("\n")[1]
    words_list = get_delimited_word_list(queries)
    word_link_dict = get_youtube_link_dict(words_list)
    send_text = ""
    for word in word_link_dict.keys():
        if word_link_dict[word]:
            send_text += "{}ならこれを見ると良い！\n{}\n".format(
                word, "\n".join(word_link_dict[word]))
        else:
            send_text += "「" + word + "」は動画がないな…。\n"
    send_text.strip()

    return send_text

def get_youtube_link_dict(words_list):
    '''入力されたリストから単語を取り出して、youtubeで検索ランダムに
    合計3つURLを含んだ返答を返す
    '''
    word_link_dict={}
    for word in words_list:
        videos_list = scrape_video_urls(word)
        word_link_dict[word] = \
            sample(videos_list, 3//len(words_list)) \
                if len(videos_list) >= 3//len(words_list) \
            else []
    return word_link_dict

def get_delimited_word_list(text):
    '''入力された単語の羅列を分離してリストにして返す。
    最大で3つの単語をランダムに選んで返す。
    '''
    words_list = text.split(get_delim(text))
    words_list = [w.strip() for w in words_list]
    words_list = choices(words_list, k=3) if len(words_list)>3 else words_list
    words_list.sort()
    return words_list

def get_delim(text):
    # 区切り文字を調べる
    _delim = " "
    if " " in text:
        pass
    if "　" in text:
        _delim = "　"
    elif "\t" in text:
        _delim = "\t"
    elif "," in text:
        _delim = ","
    elif "、" in text:
        _delim = "、"
    return _delim

def judgeWhat(text):
    # 意図解釈部分
    if "ok" in text.lower() and "google" in text.lower():
        if len(text.split("\n"))>1:
            return MODE.YOUTUBE_RECOMMEND
        else:
            return MODE.OK_GOOGLE_ERROR
    elif "行く" in text:
        return MODE.GOING_TO_GO_TO_GYM
    elif "今日の体重は" in text:
        return MODE.INSERT_WEIGHT
    else:
        return MODE.get_mode_by_hash(text)

def get_holiday_message():
    wd = datetime.date.today().weekday()
    asu = "いつか"
    if wd == 7:
        asu = "明後日" # 第一土曜日
    elif wd == 6:
        asu = "明日" # 第一日曜日
    elif wd == 0:
        if datetime.date.today().day < 8:
            asu = "来週の月曜"
        else:
            asu = "今日" # 第二月曜日

    text = "{}はゴールドジム四谷店は定休日😔".format(asu)

    return text

if __name__ == "__main__":
    from pprint import pprint
    print("-----util.py test start------")
    print("-----get_delim------")
    print("\""+get_delim("a, b, c")+"\"")
    print("\""+get_delim("a\tb\tc")+"\"")
    print("\""+get_delim("a b c")+"\"")
    print("\""+get_delim("a　b　c")+"\"")

    print("-----_get_youtube_recommend(\"ok google\\n腹筋\")------")
    print(get_youtube_recommend("ok google\n腹筋"))
    print()
    print("-----_get_youtube_recommend(\"ok google\\n腹筋, 背筋, 胸筋\")------")
    print(get_youtube_recommend("ok google\n腹筋, 背筋, 胸筋"))

    print()
    print("-----_judgeWhat------")
    pprint(judgeWhat("ok google\n腹筋, 背筋, 胸筋"))
    pprint(judgeWhat("今日ジム行くわ！"))


