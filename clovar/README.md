# Clovar Skillの話

- **Pythonのライブラリは基本的にアノテーションをつけるだけ**

## PG構成
- サーバ待機
	``@app.route('/clova', methods=['POST'])	#普通のflaskアプリケーションと一緒``
- 起動時に実行
	``@clova.handle.launch``

- 特定のカスタムインテントを待つ
	``@clova.handle.intent("specificed indent")``

- スキル終了
	``@clova.handle.end``

## 用語説明
- スロット
	言葉から抽出したい単語群
	eg. slot名: 筋肉, slot_dict: 腹筋、背筋、胸筋

- インテント
	botに対する命令をまとめたもの
