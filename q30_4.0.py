import time
import gzip
import itertools
from collections import Counter
import sys
time1=time.time()
if sys.argv[1].endswith(".gz"):
    fq = gzip.open(sys.argv[1],'r')
else:
    fq = open(sys.argv[1],'r')
lines = fq.readlines()
qual = [item[:-1] for item in lines[3::4]]
quality_count = Counter(itertools.chain.from_iterable(qual))
total_base = sum(quality_count.values())
q20 = sum(value for key, value in quality_count.items() if key >= 53)
q30 = sum(value for key, value in quality_count.items() if key >= 63)
print("q20:", q20/total_base)
print("q30:", q30/total_base)
time2=time.time()
print('Time used: ' + str(time2-time1))
