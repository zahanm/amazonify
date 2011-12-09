clear all; close all;
addpath minFunc/

%% Load data

% work with toy datasets for now
LINES_TO_READ = 100000;
data = dlmread('../data/reduced_matrix.txt', '\t', [0, 0, LINES_TO_READ - 1, 2]);
% shift the customer index by 1 for matlab indexing
data(:, 2) = data(:, 2) + 1;

% remove users with high indices so matrix size stays small
for i = 1:size(data, 1)
    if data(i, 2) > 100000;
        data(i, 1) = 0;
    end
end
remove = find(data(:, 1) == 0);
data(remove, :) = [];


% separate train_test sets
dataset_size = size(data, 1);
num_test = round(dataset_size * 0.1);
shuffled_idx = randperm(dataset_size);
test_data = data(shuffled_idx(1:num_test), :);
train_data = data(shuffled_idx(num_test+1:end), :);

train_product_ids = train_data(:, 1);
train_user_ids= train_data(:, 2);
train_ratings = train_data(:, 3);


%% Intialize model parameters
num_products = max(train_product_ids);
num_users = max(train_user_ids);
latent_size = 2;

% initialize parameters
theta = 0.001*randn((num_products + num_users)*latent_size, 1);

%% if using fmincg
% options = optimset('GradObj', 'on', 'MaxIter', 50);
% [cost, grad] = fmincg( @(t) factorization_cost(t, num_products, num_users, ...
%     latent_size, train_product_ids, train_user_ids, train_ratings), theta, options);

%% if using minFunc
options.Method = 'lbgfs';
options.maxIter = 40;	
options.display = 'on';
options.DerivativeCheck = 'on';
[cost, grad] = minFunc ( @(t) factorization_cost(t, num_products, num_users, ...
    latent_size, train_product_ids, train_user_ids, train_ratings), theta, options);
                              


