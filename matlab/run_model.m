clear all; close all;


%% Load train
train_data = dlmread('../data/pruned_matrix.txt');
% shift the customer index by 1 for matlab indexing
train_data(:, 2) = train_data(:, 2) + 1;
train_matrix = sparse(train_data(:, 1), train_data(:, 2), train_data(:, 3));
clear train_data



%% Load test
NUM_LINES_TEST = 7500;
test_data = dlmread('../data/pruned_matrix_1.txt', '\t', [0, 0, NUM_LINES_TEST - 1, 2]);
% shift the customer index by 1 for matlab indexing
test_data(:, 2) = test_data(:, 2) + 1;


%% Run model
% rmse = neighborhood(train_matrix, test_data, 1);
% 
% baseline comparisons
actual_ratings = test_data(:, 3);
baseline3 = sqrt(mean((3 - actual_ratings).^2));
baseline4 = sqrt(mean((4 - actual_ratings).^2));

rmse = factorization_model(train_matrix, test_data, 10);

fprintf(1, 'Model rmse: %g\nBaseline3: %g\nBaseline4: %g\n',...
    rmse, baseline3, baseline4);
