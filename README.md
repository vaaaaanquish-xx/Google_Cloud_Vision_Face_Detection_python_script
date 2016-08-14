Google Cloud Visionの顔検出(FACE_DETECTOPN) API　を叩くやつ
====

## Script
 - main.py : 指定したディレクトリのファイル全部をGoogle APIに投げて結果を保存する
     - レスポンスのjsonも保存するようになった
 - face_detector.py : 1枚画像投げてGoogle APIを体験するやつ

## Usage
 - face_detector.py内でAPIキーを指定
 - 画像1枚送りたい時はface_detector.pyで画像へのpathを指定して

    ```python face_detector.py```

 - main.pyで入出力ディレクトリを指定して

    ```python main.py```

 - 後はブログ記事を参考に
    - Google Cloud Visionを登録しよう

    http://vaaaaaanquish.hatenablog.com/entry/2016/08/08/160158
    - PythonでGoogle Cloud Visionを使った顔検出

    http://vaaaaaanquish.hatenablog.com/entry/2016/08/08/160353
