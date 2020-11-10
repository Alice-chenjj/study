import os
import gzip
import itertools
from collections import Counter
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input', '-i', help='input the fastq file')
parser.add_argument('--sample', '-s', help='set the number for downsample', type=int)
parser.add_argument('--output', '-o', help='output the q20&q30 percentage',default='Q20_Q30.result')
args = parser.parse_args()

if args.sample and args.sample % 4 == 0:
    if args.input.endswith('gz'):
        os.system('zcat ' + args.input + ' |' + ' head ' + '-n ' + str(args.sample) + '> ' + args.input + '.sample')
    else:
        os.system('head ' + '-n ' + str(args.sample) + ' ' + args.input + '> ' + args.input + '.sample')

time1 = time.time()
if args.input.endswith('gz'):
    with gzip.open(args.input, 'rt') as f:
        quality_lines = (i.strip() for i in itertools.islice(f, 3, None, 4))  # start from 3, end of file, step is 4
        quality_count = Counter(itertools.chain.from_iterable(quality_lines))
else:
    with open(args.input, 'rt') as f:
        quality_lines = (i.strip() for i in itertools.islice(f, 3, None, 4))  # start from 3, end of file, step is 4
        quality_count = Counter(itertools.chain.from_iterable(quality_lines))

total_base = sum(quality_count.values())
q20 = sum(value for key, value in quality_count.items() if key >= '5')  # q20 base count
q30 = sum(value for key, value in quality_count.items() if key >= '?')  # q30 base count
os.system('touch ' + args.output)
time2 = time.time()
result = open(args.output, 'w+')
print('total base:', total_base, '\n'      
    'q20 bases:', q20, '\n'
    'q30 bases:', q30, '\n'
    'q20 % :', q20/total_base, '\n'
    'q30 % :', q30/total_base, '\n'
    'Time used: ' + str(time2-time1), file=result)
