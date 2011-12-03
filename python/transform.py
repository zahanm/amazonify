
from __future__ import print_function

import json
import gzip
import sys
import re

'''
Convert from the stupid Amazon format to json_value
To use with MRJob

Dependencies:
- Python 2.7 (multiple with context managers)

'''

# globals
simple_types = frozenset(('asin', 'title', 'group', 'salesrank'))
cat_re = re.compile( r'\[(?P<id>\d+)\]' )
date_re = re.compile( r'\b(?P<date>\d{4}-\d{1,2}-\d{1,2})\b' )
pair_re = re.compile( r'\b(?P<prefix>[\w]+)\s*:\s*(?P<suffix>[\w]+)\b' )

def run(raw_metadata_file, json_output_file):
  with gzip.open(raw_metadata_file) as raw_metadata, gzip.open(json_output_file, 'wb') as json_output:
    try:
      item_num = 0
      while raw_metadata:
        prefix, _, suffix = raw_metadata.next().partition(':')
        if 'Id' in prefix:
          # item object
          item = {}
          item['id'] = suffix.strip()
          item_num += 1
          parse_item(raw_metadata, item, json_output)
          if item_num % 10000 == 0:
            print('', item_num, sep='\n')
          elif item_num % 100 == 0:
            print('.', end='')
    except StopIteration:
      print('All done')

def parse_item(raw_metadata, item, json_output):
  while raw_metadata:
    prefix, _, suffix = raw_metadata.next().partition(':')
    prefix = prefix.strip().lower()
    if prefix in simple_types:
      item[prefix] = suffix.strip()
    elif prefix == 'similar':
      item[prefix] = map(lambda s: s.strip(), suffix.split()[1:])
    elif prefix == 'categories':
      item[prefix] = []
      parse_categories(raw_metadata, item, int(suffix))
    elif prefix == 'reviews':
      parse_reviews(raw_metadata, item, suffix)
    else:
      break
  json.dump(item, json_output)
  json_output.write('\n')

def parse_categories(raw_metadata, item, num):
  for i in xrange(num):
    category_line = raw_metadata.next()
    cat_list = []
    for cat in cat_re.finditer( category_line ):
      cat_list.append(cat.group('id'))
    item['categories'].append(cat_list)

def parse_reviews(raw_metadata, item, meta):
  item['review_info'] = {}
  reviews = []
  for p in pair_re.finditer(meta):
    if p.group('prefix') == 'total':
      item['review_info']['total'] = int(p.group('suffix'))
    elif p.group('prefix') == 'rating':
      item['review_info']['avg'] = float(p.group('suffix'))
  item['review_info']['reviews'] = []
  for i in xrange(item['review_info']['total']):
    review_line = raw_metadata.next()
    review = {}
    for p in pair_re.finditer(review_line):
      if p.group('prefix') == 'cutomer': # this is not a typo. I'm entirely serious.
        review['customer'] = p.group('suffix').strip()
      else:
        review[p.group('prefix')] = int(p.group('suffix'))
    item['review_info']['reviews'].append(review)

if __name__ == '__main__':
  if len(sys.argv) == 3:
    run(sys.argv[1], sys.argv[2])
  else:
    print('usage: {0} <input file name> <output file name>'.format(__file__))


"""

Id:   1
ASIN: 0827229534
title: Patterns of Preaching: A Sermon Sampler
group: Book
salesrank: 396585
similar: 5  0804215715  156101074X  0687023955  0687074231  082721619X
categories: 2
|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Preaching[12368]
|Books[283155]|Subjects[1000]|Religion & Spirituality[22]|Christianity[12290]|Clergy[12360]|Sermons[12370]
reviews: total: 2  downloaded: 2  avg rating: 5
2000-7-28  cutomer: A2JW67OY8U6HHK  rating: 5  votes:  10  helpful:   9
2003-12-14  cutomer: A2VE83MZF98ITY  rating: 5  votes:   6  helpful:   5

id: 1
asin: 0827229534
title: Patterns of Preaching: A Sermon Sampler
group: Book
salesrank: 396585
similar: [ 0804215715, 156101074X, 0687023955, 0687074231, 082721619X ]
categories:
[ [283155, 1000, 22, 12290, 12360, 12368],
[283155, 1000, 22, 12290, 12360, 12370] ]
review_info:
  total: 2
  avg: 5
  reviews: [
    date: 2000-7-28
    customer: A2JW67OY8U6HHK
    rating: 5
    votes:  10
    helpful:  9
    ,
    date: 2003-12-14
    customer: A2VE83MZF98ITY
    rating: 5
    votes: 6
    helpful: 5
]
"""