%% Load
clear all; close all;

data = dlmread('../data/reduced_matrix.txt');
% load format is product_id, user_id, rating

% shift the customer index by 1 for matlab indexing
data(:, 2) = data(:, 2) + 1;

reviews = sparse(data(:, 1), data(:, 2), data(:, 3));
clear data

[num_products, num_users] = size(reviews);
num_reviews = nnz(reviews);
reviews_logical = reviews > 0;

%% Number of reviews per user
user_review_count = full(sum(reviews_logical, 1));


%% Number of reviews per product
product_review_count = full(sum(reviews_logical, 2));