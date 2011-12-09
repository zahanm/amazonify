function [cost, grad] = factorization_cost(theta, num_products, num_users, ... 
    latent_size, p_ids, u_ids, ratings)
    
    % Regularization not implemented
    % May need to scale cost and gradient by (1 / number of training
    % examples)
    
    % unroll parameters
    p = reshape(theta(1:num_products*latent_size), num_products, latent_size);
    u = reshape(theta(num_products*latent_size + 1: end), num_users, latent_size);
    
    % cost 
    w = p(p_ids, :);
    h = u(u_ids, :);
    rating_diff = ratings - sum(w .* h, 2);
    cost = sum(rating_diff.^2);
        
    % gradient
    grad_p = zeros(size(p));
    grad_u = zeros(size(u));
    delta_p = bsxfun(@times, rating_diff, h);
    delta_u = bsxfun(@times, rating_diff, w);
    for i = 1:length(ratings);
        grad_p(p_ids(i), :) = grad_p(p_ids(i), :) + delta_p(i, :);
        grad_u(u_ids(i), :) = grad_u(u_ids(i), :) + delta_u(i, :);
    end
    grad = [grad_p(:); grad_u(:)];
    % disp(norm(grad))
end