clear all; close all;

%% Load train
train_data = dlmread('../data/train_matrix_750.txt');
% shift the customer index by 1 for matlab indexing
train_data(:, 2) = train_data(:, 2) + 1;


%% Load test
NUM_LINES_TEST = 750;
test_data = dlmread('../data/test_matrix_750.txt', '\t', [0, 0, NUM_LINES_TEST - 1, 2]);
% shift the customer index by 1 for matlab indexing
test_data(:, 2) = test_data(:, 2) + 1;


%% Intialize model parameters
num_products = max(train_data(:, 1));
num_users = max(train_data(:, 2));
latent_size = 2;
lambda = 0.01; % regularization constant

% initialize parameters
theta = 0.001*randn((num_products + num_users)*latent_size, 1);

%% if using fmincg
% options = optimset('GradObj', 'on', 'MaxIter', 50);
% [opt_theta, cost] = fmincg ( @(t) factorization_cost(t, num_products, num_users, ...
%   latent_size, lambda, train_data), theta, options);

%% if using minFunc
options.Method = 'lbgfs';
options.maxIter = 500;	
options.display = 'on';
addpath minFunc/
[opt_theta, cost] = minFunc ( @(t) factorization_cost(t, num_products, num_users, ...
    latent_size, lambda, train_data), theta, options);
%% Results
p = reshape(opt_theta(1:num_products*latent_size), num_products, latent_size);
u = reshape(opt_theta(num_products*latent_size + 1: end), num_users, latent_size);

test_product_idx = test_data(:, 1);
test_user_idx = test_data(:, 2);
test_ratings = test_data(:, 3);

predicted_ratings = p(test_product_idx, :) * u(test_user_idx, :)';


