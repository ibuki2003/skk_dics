import sys

counts = []
maxlen = 0
for line in sys.stdin:
    line = line.strip()
    midashi = line.split(' ')[0]
    length = len(midashi)

    if len(counts) < length + 1:
        counts.extend([0] * (length + 1 - len(counts)))

    counts[length] += 1

for i, count in enumerate(counts):
    print(f'{i} {count}')

