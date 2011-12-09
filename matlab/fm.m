clear all; close all;


%% Load train
train_data = dlmread('../data/reduced_matrix.txt');
% shift the customer index by 1 for matlab indexing
train_data(:, 2) = train_data(:, 2) + 1;
% train_matrix = sparse(train_data(:, 1), train_data(:, 2), train_data(:, 3));

train_product_ids = train_data(:, 1);
train_user_ids= train_data(:, 2);
train_ratings = train_data(:, 3);
clear train_data

%% Load test
NUM_LINES_TEST = 750;
test_data = dlmread('../data/test_matrix_750.txt', '\t', [0, 0, NUM_LINES_TEST - 1, 2]);
% shift the customer index by 1 for matlab indexing
test_data(:, 2) = test_data(:, 2) + 1;


%% Run model
num_products = max(train_product_ids);
num_users = max(train_user_ids);
latent_size = 2;

theta = 0.01*randn((num_products + num_users)*latent_size, 1);
options = optimset('GradObj', 'on', 'MaxIter', 50);
fminunc ( @(t) factorization_cost(t, num_products, num_users, ...
    latent_size, train_product_ids, train_user_ids, train_ratings), theta, options);
                              


