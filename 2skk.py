import sys

"""
Convert ATOK dictionary to SKK

usage:
python atok2skk.py [input] [output] (ignore_titles(optional))
"""

if len(sys.argv)<3:
    sys.exit(1)

infilep = sys.argv[1]
outfilep = sys.argv[2]

ignores = set()

if len(sys.argv)>=3: # ignore file
    with open(sys.argv[3]) as ignf:
        for l in ignf:
            ignores.add(l.strip())

with open(infilep, 'r', -1, 'utf-16-le') as infile, open(outfilep, 'w', -1, 'euc-jp') as outfile:
    #outfile.write(';; coding: -*- euc-jp -*-\n')
    for l in infile.readlines():
        if l.startswith('#'): continue
        if l.startswith('!'): continue
        if l.find('\t')==-1: continue

        yomi, word, _ = l.strip().split('\t', 3)
        if word in ignores: continue
        if word.find('/') != -1 or word.find(';') != -1:
            word = word.replace('/', '\\057')
            word = word.replace(';', '\\073')
            word = '(concat "{word}")'.format(word=word)
        try:
            outfile.write('{yomi} /{word}/\n'.format(yomi=yomi, word=word))
        except:
            print('invalid character', word)
