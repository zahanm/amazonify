clear all; close all;
addpath minFunc/

%% Load data

% work with toy datasets for now
data = dlmread('../data/toy_matrix.txt');
dataset_size = size(data, 1);

% separate train_test sets
num_test = round(dataset_size * 0.1);
test_data = data(1:num_test, :);
train_data = data(num_test+1:end, :);

train_product_ids = train_data(:, 1);
train_user_ids= train_data(:, 2);
train_ratings = train_data(:, 3);


%% Intialize model parameters
num_products = max(train_product_ids);
num_users = max(train_user_ids);
latent_size = 2;

% initialize parameters
theta = 0.001*ones((num_products + num_users)*latent_size, 1);

%% if using fmincg
% options = optimset('GradObj', 'on', 'MaxIter', 50);
% [cost, grad] = fmincg( @(t) factorization_cost(t, num_products, num_users, ...
%     latent_size, train_product_ids, train_user_ids, train_ratings), theta, options);

%% if using minFunc
options.Method = 'lbgfs';
options.maxIter = 1;	
options.display = 'off';
options.DerivativeCheck = 'on';
[opt_theta, cost] = minFunc ( @(t) factorization_cost(t, num_products, num_users, ...
    latent_size, train_product_ids, train_user_ids, train_ratings), theta, options);
                              


