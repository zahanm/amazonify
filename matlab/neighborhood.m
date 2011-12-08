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
for i = 1:num_test
    if (rem(i, 100) == 0)
        fprintf('Finished %g of %g\n', i, num_test);
    end
    
    b_id = test_data(i, 1);
    u_id = test_data(i, 2);
    gold_rating = test_data(i, 3);
    
    % remove the rating we want to predict from the matrix
    train_matrix(b_id, u_id) = 0;
    
    % if the vector for this user is now empty, skip algorithm and just
    % predict 4
    user_vector = train_matrix(:, u_id);
    if isempty(find(user_vector, 1))
        predicted_ratings(i) = 4;
        train_matrix(b_id, u_id) = gold_rating;
        continue
    end
            
    % Calculate cosine similarity
    similarity = user_vector' * train_matrix;
    similarity = similarity ./ norms;
    
    similarity = similarity ./ norm(user_vector);
    similarity(isnan(similarity)) = 0;
    
    % Sort by similarity
    [ignored_sorted_sim, sorted_ids] = sort(similarity, 'descend');
    
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
    
    % restore the rating
    train_matrix(b_id, u_id) = gold_rating;
end

rmse = sqrt(mean((predicted_ratings - actual_ratings).^2));


end % function