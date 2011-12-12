from __future__ import print_function
import sys

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    if 'libedit' in readline.__doc__:
        readline.parse_and_bind('bind ^I rl_complete')
    else:
        readline.parse_and_bind("tab: complete")

import json
import sys
import gzip
import random
from scipy.sparse import *


class ddok_matrix:
    def __init__(self):
        self.rows = {}
        self.cols = {}
        self.nrows = 0
        self.ncols = 0
        self.size = 0
        self.shape = (self.nrows, self.ncols)

    def getrow(self, row):
        if row in self.rows:
            return self.rows[row]
        else:
            raise KeyError("Row not in matrix: %i" %row)

    def getcol(self, col):
        if col in self.cols:
            return self.cols[col]
        else:
            raise KeyError("Column not in matrix: %i" %col)
        
    def __setitem__(self, key, val):
        row, col = key
        if row not in self.rows:
            self.rows[row] = {col: val}
            self.nrows += 1
            self.size  += 1
        else:
            if col not in self.rows[row]:
                self.size += 1
            self.rows[row][col] = val

        if col not in self.cols:
            self.cols[col] = {row: val}
            self.ncols += 1
        else:
            self.cols[col][row] = val

    def __getitem__(self, key):
        row, col = key
        if row not in self.rows or col not in self.rows[row]:
            return 0.0
        else:
            return self.rows[row][col]
                   

    def __len__(self):
        return self.size

def output_file(filename, matrix, user_dict, product_dict):
    rev_user_dict = {}
    for user, user_i in user_dict.iteritems():
        rev_user_dict[user_i] = user
    lines = []
    for prod, prod_i in product_dict.iteritems():
        users = matrix.getcol(prod_i)
        for user, rating in users.iteritems():
            lines.append('%s\t%s\t%s' %(str(rev_user_dict[user]), str(prod), str(rating)))
    f = open(filename, 'wb')
    f.writelines('\n'.join(lines))
    f.close()


def create_test_set(test_file, data_file, pct):
    f = gzip.open(data_file, 'rb')
    lines = f.readlines()
    f.close()

    test_set = []
    for line in lines:
        num = random.random()
        if num <= pct:
            test_set.append(line)

    f = open(test_file, 'wb')
    f.write(''.join(test_set))
    f.close()

def create_user_product_matrix(train_data):
    product_dict, user_dict = {}, {}    
    products, users = [], []
    product_i, user_i = 0, 0

    records = []

    for i, line in enumerate(train_data):
        items = line.strip().split('\t')
        product_id, user_id, rating = items[:3]
        record = {'product_id' : product_id, 'user_id' : user_id, 'stars' : rating}
        records.append(record)
        if i%100000 == 0:
            print(i)

    for record in records:      
        try:
            user_id = record['user_id']
            product_id = record['product_id']
        
            if user_id not in user_dict:
                user_dict[user_id] = user_i
                user_i += 1
                users.append(user_id)
            
            if product_id not in product_dict:
                product_dict[product_id] = product_i
                product_i += 1
                products.append(product_id)

        except:
            print(record)

    #S = dok_matrix((user_i, product_i))
    S = ddok_matrix()
    for record in records:
        try:
            user_id = record['user_id']
            product_id = record['product_id']
            user_i = user_dict[user_id]
            product_i = product_dict[product_id]
            rating = int(record['stars'])
            S[(user_i, product_i)] = rating

        except:
            pass

    return (S, user_dict, product_dict)

    
if __name__ == '__main__':
    train_file = 'data/pruned_matrix.txt'
    train_data = open(train_file, 'rb').readlines()

    matrix, user_dict, product_dict = create_user_product_matrix(train_data)
