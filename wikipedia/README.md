# Wikipediaの記事タイトルをSKK辞書にするスクリプト

Wikipediaの記事のタイトルと読みをもとにSKK辞書を作成します。

## Usage
1. 公式から全文データをダウンロードする
  ファイル名は`jawiki-latest-pages-articles.xml`です
  (読みがな情報を取得するために第1段落を使用しています)
2. 変換スクリプトを叩く

```sh
# convert
python from_wikipedia.py jawiki-latest-pages-articles.xml > out_with_descripts.txt

# sort and format
skkdic-expr2 out_with_descripts.txt | skkdic-sort > out_with_descripts_sorted.txt
```

## Downloads

Wikipediaのライセンスに基づき、CC BY-SAのもとで頒布されます

最終更新: 2025-06-01
エントリ数: 747289
https://fuwa.dev/Downloads/wikipedia_with_descripts_sorted.utf8.txt
