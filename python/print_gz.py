
from __future__ import print_function
import gzip, sys

def pgz(fname, tot_lines):
  with gzip.open(sys.argv[1]) as f:
    lines = 0
    for line in f:
      print(line.strip())
      lines += 1
      if lines >= tot_lines:
        break

if __name__ == '__main__':
  if len(sys.argv) == 3:
    pgz(sys.argv[1], int(sys.argv[2]))
  else:
    print('usage {0} <gzipped file> <num lines>'.format(__file__))
