function rmse = neighborhood(train_matrix, test_data, k)

% Neighborhood-based algorithm
% params: 
% k -- number of neighbors to use
% train_matrix -- must be sparse. Rows are products, columns are users
% test_data -- nonsparse array where each row is (user, product, rating)


% normalization factors for users in training matrix
norms = full(sqrt(sum(train_matrix.^2)));

% test data 
actual_ratings = test_data(:, 3);
predicted_ratings = zeros(size(actual_ratings));
num_test = size(test_data, 1);

fprintf('Running neighborhood model...\n');

% calculate user similarities
test_users = test_data(:, 2);
similarity = train_matrix(:, test_users)' * train_matrix;
norm_1 = sparse(1 ./ norms);
norm_1 = diag(norm_1);
norm_2 = sparse(1 ./ norms(test_users));
norm_2 = diag(norm_2);
similarity = similarity * norm_1;
similarity = norm_2 * similarity;
similarity(isnan(similarity)) = 0;

% Now have to do this row by row because there's not enough memory on my
% computer

for i = 1:num_test
    if (rem(i, 100) == 0)
        fprintf('Finished %g of %g\n', i, num_test);
    end
    
    % Sort by similarityb_id = test_data(i, 1);
    b_id = test_data(i, 1);
    u_id = test_data(i, 2);
        
    [sorted_sim, sorted_ids] = sort(similarity(i, :), 'descend');
    
    % shortcut to avoid more sparse indexing: if we can't find two users 
    % with nonzero similarity, then this person is not similar to any other
    % users. Just predict 4
    if nnz(sorted_sim) < 2
        predicted_ratings(i) = 4;
        continue;
    end
    
    % Remove this user's id
    sorted_ids(sorted_ids == u_id) = [];
        
    % choose the top k most similar
    neighbor_ids = sorted_ids(1:k);
    
    
    % pick only neighbors with ratings for the business we want
    neighbor_ratings = full(train_matrix(b_id, neighbor_ids));
    neighbor_ratings(neighbor_ratings == 0) = [];

    if isempty(neighbor_ratings)
        % default -- predict mode
        predicted_ratings(i) = 4;
    else
        predicted_ratings(i) = mean(neighbor_ratings);
    end

end

rmse = sqrt(mean((predicted_ratings - actual_ratings).^2));


end % function