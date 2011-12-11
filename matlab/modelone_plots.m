k = [1, 3, 5, 10, 25];
x = 0:k(end);

%% Full set
err_nbr = [0.34969, 0.33739, 0.334785, 0.326245, 0.322025];

figure; hold on;
plot(k, err_nbr, 'o-', 'markerfacecolor', 'b');
plot(x, 0.3210925*ones(size(x)), 'r--'); % predict 4
plot(x, 0.30075*ones(size(x)), 'm--'); % predict average

title('Prediction performance on full Amazon dataset')
xlabel('Number of neighbors, k');
ylabel('Normalized RMSE');
legend('Neighborhood model', 'Baseline: Predict 4 for all',...
    'Baseline: Predict Average for each product')
hold off;

%% Pruned set
err_nbr_pruned = [0.135223, 0.1379735, 0.14099425, 0.146693, 0.15489675];

figure; hold on;
plot(k, err_nbr_pruned, 'o-', 'markerfacecolor', 'b');
plot(x, 0.3049275*ones(size(x)), 'r--');
plot(x, 0.251325*ones(size(x)), 'm--');

title('Prediction performance on high-activity users and products');
xlabel('Number of neighbors, k'); % predict 4
ylabel('Normalized RMSE'); % predict average

legend('Neighborhood model', 'Baseline: Predict 4 for all',...
    'Baseline: Predict Average for each product')