
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
num_types = frozenset(('rating', 'votes', 'helpful'))
cat_re = re.compile( r'\[(?P<id>\d+)\]' )
# cutomer is not a typo. I'm entirely serious. Go Amazon!
review_re = re.compile( r'\s*[\d-]+\s+cutomer\s*:\s*(?P<customer>\w+)\s+rating\s*:\s*(?P<rating>\d+)\s+votes\s*:\s*(?P<votes>\d+)\s+helpful\s*:\s*(?P<helpful>\d+)\s*' )

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
      print('', 'All done', sep='\n')

def parse_item(raw_metadata, item, json_output):
  while raw_metadata:
    prefix, _, suffix = raw_metadata.next().partition(':')
    prefix = prefix.strip().lower()
    if prefix in simple_types:
      item[prefix] = suffix.strip()
    elif prefix == 'similar':
      item[prefix] = map(lambda s: s.strip(), suffix.split()[1:])
    elif prefix == 'categories':
      parse_categories(raw_metadata, item, int(suffix))
    elif prefix == 'reviews':
      parse_reviews(raw_metadata, item, suffix)
      break
    else:
      break
  json.dump(item, json_output)
  json_output.write('\n')

def parse_categories(raw_metadata, item, num):
  item['categories'] = []
  for i in xrange(num):
    category_line = raw_metadata.next()
    cat_list = []
    for cat in cat_re.finditer( category_line ):
      cat_list.append(cat.group('id'))
    item['categories'].append(cat_list)

def parse_reviews(raw_metadata, item, meta):
  item['review_info'] = {}
  reviews = []
  item['review_info']['reviews'] = []
  totrating = 0
  m = review_re.match(raw_metadata.next())
  while m:
    review = m.groupdict()
    review['customer'] = m.group('customer')
    for prop in num_types:
      review[prop] = int(m.group(prop))
    totrating += review['rating']
    item['review_info']['reviews'].append(review)
    m = review_re.match(raw_metadata.next())
  # calculating these since meta information seems unreliable
  item['review_info']['total'] = len(item['review_info']['reviews'])
  try:
    item['review_info']['avg'] = float(totrating) / item['review_info']['total']
  except ZeroDivisionError:
    item['review_info']['avg'] = 0

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