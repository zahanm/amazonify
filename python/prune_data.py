from create_matrices import *

def prune_matrix(matrix, user_dict, product_dict, min_k=5):
    p_user_dict = {}
    p_product_dict = {}
    
    p_user_i, p_product_i = 0, 0
    p_matrix = ddok_matrix()

    for user, user_i in user_dict.iteritems():
        try:
            user_row = matrix.getrow(user_i)
            if len(user_row) > min_k:
                p_user_dict[user] = p_user_i
                p_user_i += 1
        except:
            pass

    usable_products = {}
    for product, product_i in product_dict.iteritems():
        try:
            product_col = matrix.getcol(product_i)
            if len(product_col) > min_k:
                p_product_dict[product] = p_product_i
                p_product_i += 1
                usable_products[product_i] = product
        except:
            pass

    for user, p_user_i in p_user_dict.iteritems():
        user_row = matrix.getrow(user_dict[user])
        for product_i, rating in user_row.iteritems():
            if product_i in usable_products:
                p_product_i = p_product_dict[usable_products[product_i]]
                p_matrix[p_user_i, p_product_i] = rating

    return (p_matrix, p_user_dict, p_product_dict)

    
if __name__ == '__main__':
    train_file = 'data/reduced_matrix.txt.gz'
    matrix, user_dict, product_dict = create_user_product_matrix(train_file)
    current_size = len(matrix)
    
    p_matrix, p_user_dict, p_product_dict = prune_matrix(matrix, user_dict, product_dict)
    while current_size > len(p_matrix):
        current_size = len(p_matrix)
        print ("Pruning matrix... current size = %i" %current_size)
        p_matrix, p_user_dict, p_product_dict = prune_matrix(p_matrix, p_user_dict, p_product_dict)
