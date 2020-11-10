import sys
import time
import gzip
from typing import List, Union


class Reader:

    def __init__(self, fname):
        self.__file = None
        self.__gz = False
        self.__eof = False
        self.filename = fname
        if self.filename.endswith(".gz"):
            self.__gz = True
            self.__file = gzip.open(self.filename, "r")
        else:
            self.__gz = False
            self.__file = open(self.filename, "r")
        if self.__file == None:
            print("Failed to open file " + self.filename)
            sys.exit(1)
    def nextRead(self):
        if self.__eof == True or self.__file == None:
            return None
        lines = []
        # read 4 (lines, name, sequence, strand, quality)
        for i in range(0, 4):
            line = self.__file.readline().rstrip()
            if len(line) == 0:
                self.__eof = True
                return None
            lines.append(line)
        return lines
def qual_stat(qstr):
    q20 = 0
    q30 = 0
    for q in qstr:
        if q >= '5':
            q20 += 1
            if q >= '?':
                q30 += 1
    return q20, q30

def stat(filename):
    reader = Reader(filename)
    total_count = 0
    q20_count = 0
    q30_count = 0
    while True:
        read = reader.nextRead()
        if read == None:
            break
        total_count += len(read[3])
        q20, q30 = qual_stat(read[3])
        q20_count += q20
        q30_count += q30

    print("total bases:", total_count)
    print("q20 bases:", q20_count)
    print("q30 bases:", q30_count)
    print("q20 percents:", 100 * float(q20_count)/float(total_count))
    print("q30 percents:", 100 * float(q30_count)/float(total_count))

def main():
    if len(sys.argv) < 2:
        print("usage: python q30.py <fastq_file>")
        sys.exit(1)
    stat(sys.argv[1])

if __name__ == "__main__":
    time1 = time.time()
    main()
    time2 = time.time()
    print('Time used: ' + str(time2-time1))

