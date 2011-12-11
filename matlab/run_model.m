clear all; close all;


%% Load train
train_data = dlmread('../data/pruned_matrix_train.txt');
% shift the customer index by 1 for matlab indexing
train_data(:, 2) = train_data(:, 2) + 1;
train_matrix = sparse(train_data(:, 1), train_data(:, 2), train_data(:, 3));
clear train_data



%% Load test
test_data = dlmread('../data/pruned_matrix_test.txt');
% shift the customer index by 1 for matlab indexing
test_data(:, 2) = test_data(:, 2) + 1;


%% Run model

% baseline comparisons
actual_ratings = test_data(:, 3);
baseline3 = sqrt(mean((3 - actual_ratings).^2));
baseline4 = sqrt(mean((4 - actual_ratings).^2));

rmse = neighborhood(train_matrix, test_data, 1);

fprintf(1, 'Model rmse: %g\nBaseline3: %g\nBaseline4: %g\n',...
    rmse, baseline3, baseline4);
