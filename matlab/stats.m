%% Load
clear all; close all;
LINES_TO_READ = 7593244;
data = dlmread('../data/review_matrix.txt', '\t', [1, 0, LINES_TO_READ, 2]);
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

mean_user_review_count = mean(user_review_count)
median_user_review_count = median(user_review_count)
std_user_review_count = std(user_review_count)