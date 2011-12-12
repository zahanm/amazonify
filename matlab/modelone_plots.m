k = [1, 3, 5, 10, 25];
x = 0:k(end);

%% Full set
err_nbr = [0.1972, 0.2099, 0.2185, 0.2284, 0.2339];

figure; hold on;
plot(k, err_nbr, 'o-', 'markerfacecolor', 'b');
plot(x, 0.3210925*ones(size(x)), 'r--'); % predict 4
plot(x, 0.30075*ones(size(x)), 'm--'); % predict average

title('Prediction performance on full Amazon dataset')
xlabel('Number of neighbors, k');
ylabel('Normalized RMSE');
legend('Item-based model', 'Baseline: Predict 4 for all',...
    'Baseline: Predict Average for each product')
hold off;

%% Pruned set
err_nbr_pruned = [0.3636, 0.3172, 0.3083, 0.3024, 0.2967];

figure; hold on;
plot(k, err_nbr_pruned, 'o-', 'markerfacecolor', 'b');
plot(x, 0.3049275*ones(size(x)), 'r--');
plot(x, 0.251325*ones(size(x)), 'm--');

title('Prediction performance on high-activity users and products');
xlabel('Number of neighbors, k'); % predict 4
ylabel('Normalized RMSE'); % predict average

legend('Item-based model', 'Baseline: Predict 4 for all',...
    'Baseline: Predict Average for each product')