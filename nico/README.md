# ニコニコ大百科IME SKK変換
[原作](http://tkido.com/blog/1019.html) からダウンロードしたAtok向け辞書をSKKにします。
ここにあるファイルは[読みが通常の読み方とは異なる記事の一覧](https://dic.nicovideo.jp/a/%E8%AA%AD%E3%81%BF%E3%81%8C%E9%80%9A%E5%B8%B8%E3%81%AE%E8%AA%AD%E3%81%BF%E6%96%B9%E3%81%A8%E3%81%AF%E7%95%B0%E3%81%AA%E3%82%8B%E8%A8%98%E4%BA%8B%E3%81%AE%E4%B8%80%E8%A6%A7)から除外タイトル一覧を取得するスクリプトです 変換は`/2skk.py`を用います。

## Usage
```sh
# get ignore titles
python find_ignores.py > ignore_titles.txt

# convert
python 2skk.py nicoime_atok.txt nicoime_skk.eucjp.txt ignore_names.txt

# sort and format
skkdic-expr2 nicoime_skk.eucjp.txt | skkdic-sort > nicoime_skk_sorted.eucjp.txt
```
