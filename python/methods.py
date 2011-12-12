from create_matrices import *
from math import sqrt
import heapq

user_edges = {}
product_edges = {}
magnitudes = {}


def neighbourhood_approach(training_matrix, user_dict, product_dict,
                           test_data, k=5):
    global user_edges, magnitudes
    predicted_vals, actual_vals = [], []

    magnitudes = {}
    error, total = 0.0, 0.0
    n_users = training_matrix.nrows
    for it, line in enumerate(test_data):
        product_id, user_id, rating = line.strip().split('\t')[:3]

        if user_id not in user_dict:
            continue
        if product_id not in product_dict:
            continue
            
        user_i = user_dict[user_id]
        product_i = product_dict[product_id]

        product_users = training_matrix.getcol(product_i)
        knn = []
            
        for i in product_users:
            if i == user_i:
                continue

            # value = cosine_similarity(training_matrix, user_i, i, avoidKey=product_i)

            if (user_i, i) in user_edges:
                value = user_edges[(user_i, i)]
            elif (i, user_i) in user_edges:
                value = user_edges[(i, user_i)]
            else:
                value = cosine_similarity(training_matrix, user_i, i)
                user_edges[(user_i, i)] = value

            if value > 0:
                heapq.heappush(knn, (i, value))
                    
        top_k = heapq.nlargest(k, knn, key=lambda x: x[1])
        if len(top_k) > 0:
            prediction = sum([training_matrix[i, product_i] for i,val in top_k]) / len(top_k)
            predicted_vals.append(prediction)
            actual_val = float(rating)
            actual_vals.append(actual_val)
            square_diff = (prediction - actual_val) ** 2
            error += square_diff
            total += 1

    error = sqrt(error / total) / 4.0
    return (error, predicted_vals, actual_vals)



def item_approach(training_matrix, user_dict, product_dict, test_data, k=1):
    global product_edges, magnitudes

    magnitudes = {}
    predicted_vals, actual_vals = [], []
    error, total = 0.0, 0.0
    for it, line in enumerate(test_data):
        product_id, user_id, rating = line.strip().split('\t')[:3]

        prediction = 4.0
        if user_id in user_dict and product_id in product_dict:
            user_i = user_dict[user_id]
            product_i = product_dict[product_id]

            user_row = training_matrix.getrow(user_i)
            product_col = training_matrix.getcol(product_i)

            knn = []
            
            for o_product in user_row:
                if product_i == o_product:
                    continue

                # value = cosine_similarity(training_matrix, o_product, product_i, use_row=False, avoidKey=user_i)

                if (product_i, o_product) in product_edges:
                    value = product_edges[(product_i, o_product)]
                if (o_product, product_i) in product_edges:
                    value = product_edges[(o_product, product_i)]
                else:
                    value = cosine_similarity(training_matrix, o_product, product_i, use_row=False)
                    product_edges[(product_i, o_product)] = value

                if value > 0.0:
                    heapq.heappush(knn, (o_product, value))

            top_k = heapq.nlargest(k, knn, key=lambda x: x[1])
            if len(top_k) > 0:
                prediction = sum(training_matrix[user_i, i] for (i, rating) in top_k) / float(len(top_k))

        predicted_vals.append(prediction)
        actual_val = float(rating)
        actual_vals.append(actual_val)
        square_diff = (prediction - actual_val) ** 2
        error += square_diff
        total += 1

    error = sqrt(error / total) / (4.0)
    return (error, predicted_vals, actual_vals)


def cosine_similarity(training_matrix, item_a, item_b, use_row=True, avoidKey=None):
    if use_row:
        vec_a = training_matrix.getrow(item_a)
        vec_b = training_matrix.getrow(item_b)

    else:
        vec_a = training_matrix.getcol(item_a)
        vec_b = training_matrix.getcol(item_b)

    dot_prod = dot_product(vec_a, vec_b, avoidKey=avoidKey)
    mag_a = get_magnitude(item_a, vec_a, avoidKey=avoidKey)
    mag_b = get_magnitude(item_b, vec_b, avoidKey=avoidKey)

    return dot_prod / sqrt(mag_a * mag_b)

def get_magnitude(item, vec, avoidKey=None):
    global magnitudes

    # return dot_product(vec, vec, avoidKey=avoidKey)

    if item not in magnitudes:
        mag = dot_product(vec, vec, avoidKey=avoidKey)
        magnitudes[item] = mag
    else:
        mag = magnitudes[item]

    return mag


def baseline_error(predicted_val, actual_vals):
    error = 0.0
    for val in actual_vals:
        error += (predicted_val - val)**2
    error /= len(actual_vals)
    return sqrt(error) / 4.0


def dot_product(vec_a, vec_b, avoidKey=None):
    dot_prod = 0.0
    if len(vec_a) > len(vec_b):
        vec_b, vec_a = vec_a, vec_b

    for key, a_val in vec_a.iteritems():
        if key in vec_b and key != avoidKey:
            dot_prod += (a_val * vec_b[key])

    return dot_prod


if __name__ == '__main__':
    train_file = 'data/train_matrix_7500.txt.gz'    
    test_file = 'data/test_matrix_7500.txt.gz'

    # train_file = 'data/pruned_matrix_train.txt.gz'    
    # test_file = 'data/pruned_matrix_test.txt.gz'

    use_gzip = False

    if use_gzip:
        train_data = gzip.open(train_file, 'rb').readlines()
        test_data = gzip.open(test_file, 'rb').readlines()

    else:
        train_data = open(train_file[:-3], 'rb').readlines()
        test_data = open(test_file[:-3], 'rb').readlines()     

    matrix, user_dict, product_dict = create_user_product_matrix(train_data)

    ks = [1, 3, 5, 10, 25]
    # for i in ks:
    #     error, predicted_vals, actual_vals = neighbourhood_approach(matrix, user_dict, product_dict, test_data, k=i)
    #     print("Neighborhood approach, k = %i, error = %f" %(i, error)) 
    for i in ks:
        error, predicted_vals, actual_vals = item_approach(matrix, user_dict, product_dict, test_data, k=i)
        print("Item approach: k = %i, error = %f" %(i, error))
