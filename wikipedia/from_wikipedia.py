import re
import jaconv
import sys
import typing
import xml.etree.ElementTree as ET
from collections.abc import Iterator

ptn_normal = re.compile(r"『?'''([^']+)'''』? ?[(（]([^)）]+)[)）]")
ptn_tagged = re.compile(r"\{\{読み[^|]*\|'''([^']+)'''([^}]+)\}\}")
following_brace = re.compile('[(（][^)）]+[)）]$')
delimiter = re.compile('[、,]')

# argument file should be readable object.
def extract_pages(file: typing.TextIO) -> Iterator[typing.Tuple[str, str]]:
    lines = []
    for line in file:
        if len(lines) == 0 and not line.startswith('  <page>'):
            continue
        lines.append(line.strip())
        if line.startswith('  </page>'):
            text = '\n'.join(lines)
            try:
                parsed = ET.fromstring(text)
                title = parsed.find('title')
                text_element = parsed.find('revision/text')
                if title is not None and text_element is not None:
                    yield (title.text or '', text_element.text or '')
            except ET.ParseError:
                pass
            lines = []

def main(filename):
    print(';; -*- fundamental -*- ; coding: utf-8 -*-')
    for title, text in extract_pages(open(filename, 'r', encoding='utf-8')):
        title = remove_whitespaces(title)
        if not title or not text:
            continue

        for line in text.split('\n'):
            #     break
            if line.startswith('== ') or line.startswith('=== ') or line.startswith('==== '):
                break

            match = ptn_normal.search(line)
            if match and remove_whitespaces(match.group(1)) == title:
                yomis = delimiter.split(match.group(2))
                abstract = line[match.start():]
                descript = get_descript_when_available(abstract)
                for yomi in yomis:
                    if yomi == '': continue
                    yomi = format_yomi(yomi)
                    if yomi is None: continue
                    if yomi == '': continue
                    print(yomi, ' /', title, descript, '/', sep='', flush=False)
                continue

            match = ptn_tagged.search(line)
            if match and remove_whitespaces(match.group(1)) == title:
                yomis = match.group(2).split('|')
                abstract = line[match.start():]
                descript = get_descript_when_available(abstract)
                for yomi in yomis:
                    if yomi == '': continue
                    fyomi = format_yomi(yomi)
                    if fyomi is None: continue
                    if fyomi == '': continue
                    print(fyomi, ' /', title, descript, '/', sep='', flush=False)
                continue



CHARS_KANA = set(''.join(chr(i) for i in range(ord("ぁ"), ord("ゖ")+1)) + 'ー')
valid_chars = CHARS_KANA.union('0123456789')
erase_chars = '-・・･'

def format_yomi(s):
    s = jaconv.kata2hira(s)
    s = unescape_wiki(s)
    s = remove_whitespaces(s)
    s = s.replace("'''", '')
    for c in erase_chars:
        s = s.replace(c, '')
    has_kana = False

    if len(s) <= 1:
        # remove yomi with length 1
        return None

    for c in s:
        if c not in valid_chars:
            return None
        if c in CHARS_KANA:
            has_kana = True

    if not has_kana:
        # remove yomi without kana
        return None
    return s

def remove_whitespaces(s):
    s = s.replace(' ', '')
    s = s.replace('　', '')
    return s

wiki_link = re.compile(r'\[\[(?:[^\|\]]+?\|)?([^\]]+?)\]\]')
wiki_tag = re.compile(r'\{\{[^}]+\}\}')
other_lang = re.compile(r'{{lang[^}]+\|(.+)}}')
comment = re.compile(r'<!--.*?-->', re.DOTALL)
tag_ref = re.compile(r'<ref[^>]*>(.*?)</ref>|<ref [^>]*/>', re.DOTALL)

def get_descript_when_available(s):
    s = unescape_wiki(s)
    s = s.replace('\n', ' ')
    s = s.replace('/', '')
    return ';' + s

def unescape_wiki(s):
    # s = s.replace('<text xml:space="preserve">', '')
    s = tag_ref.sub('', s)
    s = wiki_link.sub('\\1', s)
    s = ptn_tagged.sub('\\1', s)
    s = other_lang.sub('\\1', s)
    s = wiki_tag.sub('', s)
    s = comment.sub('', s)

    s = s.replace("'''", '')
    ban_chars = ['{', '}', '[', ']']
    for c in ban_chars:
        s = s.replace(c, '')
    return s


if __name__ == "__main__":
    fn = 'jawiki-latest-pages-articles.xml'
    if len(sys.argv) >= 2:
        fn = sys.argv[1]
    main(fn)
