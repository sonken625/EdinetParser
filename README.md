# EdinetParser

Edinetにある有価証券報告書をいろいろDBに入れて比較したりするためのツール
とりあえず

- EDINETコードを入れるとEDINETにあるだけのXBRLファイルをダウンロード
- 企業名は[ここ](https://disclosure.edinet-fsa.go.jp/E01EW/download?uji.verb=W1E62071EdinetCodeDownload&uji.bean=ee.bean.W1E62071.EEW1E62071Bean&TID=W1E62071&PID=W1E62071&SESSIONKEY=1503374365874&downloadFileName=&lgKbn=2&dflg=0&iflg=0&dispKbn=1)を参照して、自分でEDINETコードを絞り込んだりして使う。

- EDINETコードだけを書いた１列のエクセルファイルをLoadAndParse.pyと同じ場所に置くと、企業を特定してダウンロードする。
- ダウンロード対象は有価証券報告書のみ。訂正有価証券報告書は覗いている。EDINETにあるだけダウンロードしてる。


- [金融庁のCSV](http://www.fsa.go.jp/search/20170228/1f.xls)からカラムを取得しDB生成
- XBRLのデータからDBにカラム追加


までを作りました。改良する予定。