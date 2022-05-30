import re
import jaconv
import sys

tag = re.compile('&lt;(\w+).+?/\\1&gt;')
ptn = re.compile('\'\'\'([^\']+)\'\'\' ?[(（]([^)）]+)[)）]')
following_brace = re.compile('[(（][^)）]+[)）]$')
delimiter = re.compile('[、 ]')

def main(filename):
    title=None
    try:
        with open(filename) as f:
            print(';; -*- fundamental -*- ; coding: utf-8 -*-')
            for l in f:
                l = l.strip()
                l = tag.sub('', l)
                if l.startswith('<title>'):
                    new_title = l[7:-8]
                    new_title = following_brace.sub('', new_title)
                    # if title is not None:
                        # print("yomi not found for:", title)
                    title = remove_whitespaces(new_title)
                    # print("title:",title)
                    continue
                if title is None:
                    continue
                match = ptn.search(l)
                if not match:
                    continue
                if remove_whitespaces(unescape_wiki(match.group(1))) != title: continue
                yomis = delimiter.split(match.group(2))
                for yomi in yomis:
                    fyomi = format_yomi(yomi)
                    if fyomi is None: continue
                    if fyomi == '': continue
                    print(fyomi, ' /', title, get_descript_when_available(l), '/', sep='', flush=False)
                title = None

    except:
        pass

valid_chars = ''.join(chr(i) for i in range(ord("ぁ"), ord("ゖ")+1))
valid_chars += 'ー'
valid_chars += '0123456789'
valid_chars = set(valid_chars)

erase_chars = '-・・･'

def format_yomi(s):
    s = jaconv.kata2hira(s)
    s = remove_whitespaces(s)
    s = s.replace("'''", '')
    for c in erase_chars:
        s = s.replace(c, '')
    for c in s:
        if c not in valid_chars:
            return None
    return s

def remove_whitespaces(s):
    s = s.replace(' ', '')
    s = s.replace('　', '')
    return s

wiki_link = re.compile('\[\[(?:[^\|]+\|)?([^\]]+)\]\]')
other_lang = re.compile('{{lang[^}]+\|(.+)}}')

def get_descript_when_available(s):
    if '/' in s:
        return ''
    return ';' + unescape_wiki(s)

def unescape_wiki(s):
    s = s.replace('<text xml:space="preserve">', '')
    s = s.replace("'''", '')
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')

    s = wiki_link.sub('\\1', s)
    s = other_lang.sub('\\1', s)

    s = tag.sub('', s)
    return s


if __name__ == "__main__":
    fn = 'jawiki-latest-pages-articles.xml'
    if len(sys.argv) >= 2:
        fn = sys.argv[1]
    main(fn)
