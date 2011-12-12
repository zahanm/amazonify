function [cost, grad] = factorization_cost(theta, num_products, num_users, ... 
    latent_size, lambda, train_data)
 
    p_ids = train_data(:, 1);
    u_ids = train_data(:, 2);
    ratings = train_data(:, 3);
    num_examples = length(ratings);
    
    % unroll parameters
    p = reshape(theta(1:num_products*latent_size), num_products, latent_size);
    u = reshape(theta(num_products*latent_size + 1: end), num_users, latent_size);
    
    % cost 
    w = p(p_ids, :);
    h = u(u_ids, :);
    rating_diff = sum(w .* h, 2) - ratings;
    cost = (1 / num_examples) *sum(rating_diff.^2);
    % cost = cost + lambda * sum(theta.^2); % regularization adjustment
    

    % gradient
    grad_p = zeros(size(p));
    grad_u = zeros(size(u));
   
    delta_p = bsxfun(@times, rating_diff, h);
    delta_u = bsxfun(@times, rating_diff, w);
    
    for i = 1:num_examples
        grad_p(p_ids(i), :) = grad_p(p_ids(i), :) + 2*delta_p(i, :);
        grad_u(u_ids(i), :) = grad_u(u_ids(i), :) + 2*delta_u(i, :);
    end
    grad = [grad_p(:); grad_u(:)];
    grad = (1 / num_examples) * grad; % scale
    % grad = grad + 2*lambda*theta; % regularization adjustment
    
end
