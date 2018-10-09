from urllib import request
from urllib import parse
from bs4 import BeautifulSoup

def _get_request_via_get(url):
    '''入力されたurlからhttpリクエストをして、ページのソースコードを返すモジュール
    '''
    source = request.urlopen(url)
    return source

def scrape_video_ids(source):
    '''検索結果を表示するソースコードから, 動画のidを返す
    '''
    soup = BeautifulSoup(source, "lxml")
    js_script = soup.findAll('img')
    urls = [x.attrs['src'] for x in js_script]
    urls = [x for x in urls if 'https' in x]
    video_ids = [x.split('/')[4] for x in urls]
    return video_ids

def scrape_video_urls(word):
    # 検索クエリの作成とエンコーディング
    query_word = '筋トレ ' + word
    query_word = parse.quote_plus(query_word, encoding="utf8")

    try:
        # 検索結果を表示するページのソースを取得
        url = 'https://www.youtube.com/results?search_query=' + query_word
        source = _get_request_via_get(url)
        if source is None:
            raise Exception
    except:
        return []

    try:
        # 検索結果のvideoのidを取得し、視聴のためのurlを作成する
        video_ids = scrape_video_ids(source=source)
        video_urls = ['https://www.youtube.com/watch?v=' + x for x in video_ids]
        return video_urls
    except:
        return []

if __name__ == "__main__":
    from pprint import pprint
    pprint(scrape_video_urls("腹筋"))
    pprint(scrape_video_urls("腕立て"))