
from __future__ import print_function

import json
import gzip
import sys

def run(raw_metadata_file):
  with gzip.open(raw_metadata_file) as raw_metadata:
    for i in xrange(40):
      print(next(raw_metadata).strip())

if __name__ == '__main__':
  if len(sys.argv) == 2:
    run(sys.argv[1])


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