k = [10, 20];
x = 5:25;

% Pruned set
err_nbr_pruned = [0.2231, 0.2280];

figure; hold on;
plot(k, err_nbr_pruned, 'o-', 'markerfacecolor', 'b');
plot(x, 0.3049275*ones(size(x)), 'r--');
plot(x, 0.251325*ones(size(x)), 'm--');

title('Prediction performance on high-activity users and products');
xlabel('Number of latent dimensions, f'); % predict 4
ylabel('Normalized RMSE'); % predict average

legend('Matrix factorization model', 'Baseline: Predict 4 for all',...
    'Baseline: Predict Average for each product')