function [cost, grad] = factorization_cost(theta, num_products, num_users, ... 
    latent_size, lambda, train_data)
        
    % May need to scale cost and gradient by (1 / number of training
    % examples)
    
    p_ids = train_data(:, 1);
    u_ids = train_data(:, 2);
    ratings = train_data(:, 3);
    
    % unroll parameters
    p = reshape(theta(1:num_products*latent_size), num_products, latent_size);
    u = reshape(theta(num_products*latent_size + 1: end), num_users, latent_size);
    
    % cost 
    w = p(p_ids, :);
    h = u(u_ids, :);
    rating_diff = ratings - sum(w .* h, 2);
    cost = sum(rating_diff.^2) + lambda * sum(theta.^2);
    
    
        
    % gradient
    grad_p = zeros(size(p));
    grad_u = zeros(size(u));
   
    delta_p = bsxfun(@times, rating_diff, w);
    delta_u = bsxfun(@times, rating_diff, h);
    
    for i = 1:length(ratings);
        grad_p(p_ids(i), :) = grad_p(p_ids(i), :) - 2*delta_p(i, :);
        grad_u(u_ids(i), :) = grad_u(u_ids(i), :) - 2*delta_u(i, :);
    end
    grad = [grad_p(:); grad_u(:)];
    grad = grad + 2*lambda*theta; % regularization adjustment
    
end