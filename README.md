# gym-progress

## google app engine周り
### deploy
`gcloud app deploy`
URL確認
`gcloud app browse`
gcloudの登録情報確認
```
gcloud auth list
gcloud config list
```

## 共通化されたflaskのインスタンスを使う
- アプリケーションの起動コマンド</br>
  ``python manage.py``
- インスタンスを作っている場所</br>
  ``flaskr/__init__.py``
- インスタンスの使い方</br>
  1. ``app = Flask(__name__)``以降に、インスタンスを使いたいファイル名を記述
  2. インスタンスを使いたいファイルの先頭部分で``from flaskr import app``と記述

## youtube video scraper

### feature
引数に指定した単語と筋トレを含んだ動画をyoutubeから探して、動画のurlを返してくれる
検索したvideoが一件もない場合や、うまくパースできない場合は空の配列を返す

### useage

```
word = '上腕三頭筋'
video_urls = scrape_video_urls(word)

```

## バッチ処理
カルーセルを表示するメソッドに関しては、バッチ処理できるようになっている。  
この場合、プログラムのルートディレクトリで、以下のPGと、引数でカテゴリと送信先のuser_idを指定する  

``python carousel_adviser.py  -c CATEGORY (recipie or workout) -uid USER_ID``
