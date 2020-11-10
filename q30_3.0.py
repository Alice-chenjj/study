import sys
import gzip
import itertools
from collections import Counter
import time
time1=time.time()
# fq = sys.argv[1]
fq= 'q30-master\\SRR5367808.1.fastq.gz'
if fq.endswith('gz'):
    with gzip.open(fq, 'rt') as f:
        quality_lines = (i.strip() for i in itertools.islice(f, 3, None, 4))  # start from 3, end of file, step is 4
        quality_count = Counter(itertools.chain.from_iterable(quality_lines))
else:
    with open(fq, 'rt') as f:
        quality_lines = (i.strip() for i in itertools.islice(f, 3, None, 4))  # start from 3, end of file, step is 4
        quality_count = Counter(itertools.chain.from_iterable(quality_lines))
total_base = sum(quality_count.values())
q20 = sum(value for key, value in quality_count.items() if key >= '5')  # q20 base count
q30 = sum(value for key, value in quality_count.items() if key >= '?')  # q30 base count

print(total_base, q20/total_base, q30/total_base, sep='\t')
time2=time.time()
print('Time used: ' + str(time2-time1))