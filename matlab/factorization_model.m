function rmse = factorization_model(train_matrix, test_data, f)

[n_items, n_users] = size(train_matrix);

ps = rand(n_users, f);
qs = rand(n_items, f);

% test data 
actual_ratings = test_data(:, 3);
num_test = size(test_data, 1);

% training
psqs = vertcat(ps,qs);

weights = fminunc(@(a) mean_error(train_matrix, a, n_users, n_items), psqs);

ps = weights(1:n_users,:);
qs = weights((n_users+1):(n_users+n_items),:);

% testing

rmse = 0.0;

for test = 1:num_test
    if (rem(test, 100) == 0)
        fprintf('Finished %g of %g\n', test, num_test);
    end
    b_id = test_data(test, 1);
    u_id = test_data(test, 2);
    rmse = rmse + (actual_ratings(test) - ps(u_id,:) * qs(b_id,:)')^2;
end

rmse = sqrt(rmse) / num_test;
