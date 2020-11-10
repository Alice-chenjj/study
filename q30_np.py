import numpy as np
import time
import gzip
import sys
time1=time.time()
if sys.argv[1].endswith(".gz"):
    fq = gzip.open(sys.argv[1],'r')
else:
    fq = open(sys.argv[1],'r')
lines = fq.readlines()
qual = np.array([item[:-1] for item in lines[3::4]])
qual_20 = qual.copy()
qual_20 = np.delete(qual_20.view(np.int8), np.where(qual_20.view(np.int8) == 0), axis=0)
q20=(qual_20>53).sum()
q30=(qual_20>63).sum()
print("q20:",q20/len(qual_20))
print("q30:", q30/len(qual_20))
time2=time.time()
print('Time used: ' + str(time2-time1))
