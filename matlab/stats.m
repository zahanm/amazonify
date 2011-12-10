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
figure;
user_review_count = full(sum(reviews_logical, 1));
user_edges = 0:max(user_review_count);
user_hist = histc(user_review_count, user_edges);
loglog(user_edges, user_hist / sum(user_review_count))
title('Distribution of reviews per user');
xlabel('Review count');
ylabel('Percentage of users');
hold off;

%% Number of reviews per product
figure;
product_review_count = full(sum(reviews_logical, 2));
product_edges = 0:max(product_review_count);
product_hist = histc(product_review_count, product_edges);
loglog(product_edges, product_hist / sum(product_review_count))
title('Distribution of reviews per product')
xlabel('Review count');
ylabel('Percentage of products');
hold off;

%% Ratings distribution
figure;
all_ratings = nonzeros(reviews);
sum_ratings = sum(all_ratings);
ratings_edges = 1:5;
ratings_hist = histc(all_ratings, ratings_edges);
bar(ratings_edges, ratings_hist / sum_ratings);
title('Distribution of ratings');
xlabel('Number of stars');
ylabel('Percentage of ratings');