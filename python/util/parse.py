import gzip
import cPickle


""" Yes, it is 'cutomer' in the dataset and not 'customer'
"""

class Parser:
    def __init__(self):
        self.customer_map = {} 
        self.product_map = {}

    def run(self):
        # self.buildIdMappings()
        self.loadIdMappings()
        self.buildReviewMatrix()
        self.buildSimilarGraph()

    def buildIdMappings(self, filename='../../data/amazon-meta.txt.gz'):
        """Read the file once to map customer ids and product ids to 
        matrix indices. Pickle for next time.
        """
        product_ids = []
        customer_ids = set()

        with gzip.open(filename) as infile:

            for line in infile:
                # track product ID -- should only appear once
                if line.startswith("ASIN:"):
                    asin = line.split()
                    product_ids.append(asin[1])
                # track customer ID 
                if line.find("cutomer:") > -1:
                    review_info = line.split()
                    customer_ids.add(review_info[2])

            # Create map of Amazon customer_id -> Matrix index
            customer_ids = list(customer_ids)
            customer_ids.sort()
            self.customer_map = dict(zip(customer_ids, 
                                range(len(customer_ids))))
    
            # Create map of Amazon product_id -> Matrix index
            self.product_map = dict(zip(product_ids, 
                               range(len(product_ids))))

        # save
        with open('id_maps.pickle', 'w') as map_file:
            cPickle.dump((self.product_map, self.customer_map), map_file)

    def loadIdMappings(self, filename='id_maps.pickle'):
        with open(filename, 'r') as map_file:
            (self.product_map, self.customer_map) = cPickle.load(map_file)
        
    def buildReviewMatrix(self, filename='../../data/amazon-meta.txt.gz'):
        with gzip.open(filename) as infile, \
                open('review_matrix.txt', 'w') as outfile:

            product_idx = -1
            for line in infile:
                line = line.strip()

                # product ID
                if line.startswith("ASIN:"):
                    product_idx += 1

                # Reviews
                elif line.find("cutomer:") > -1:
                    review_info = line.split()

                    customer_idx = str(self.customer_map[review_info[2]])
                    rating = review_info[4]
                    votes = review_info[6]
                    helpful = review_info[8]

                    outfile.write('\t'.join([str(product_idx), customer_idx, 
                                             rating, votes, helpful]) + '\n')

    def buildSimilarGraph(self, filename='../../data/amazon-meta.txt.gz'):
        with gzip.open(filename) as infile, \
                open('similar_products_graph.txt', 'w') as outfile:

            product_idx = -1
            for line in infile:
                line = line.strip()
                
                # product ID
                if line.startswith("ASIN:"):
                    product_idx += 1

                # similar items
                elif line.startswith("similar:"):
                    similar_items = line.split()[2:]
                    for similar in similar_items:
                        if similar in self.product_map:
                            similar_idx = self.product_map[similar]
                            outfile.write('%d\t%d\n' %\
                                              (product_idx, similar_idx))
                
if __name__ == '__main__':
    parser = Parser()
    parser.run()
