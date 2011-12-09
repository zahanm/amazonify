function squared_sum = mean_error( train_m, psqs, n_users, n_items )
%MEAN_ERROR Summary of this function goes here
%   Detailed explanation goes here

ps = psqs(1:n_users,:);
qs = psqs((n_users+1):(n_users+n_items),:);

squared_sum = 0;

for user=1:n_users
    for item=1:n_items
        error = (train_m(user,item) - (ps(user,:) * qs(item,:)'))^2;
        squared_sum = squared_sum + error;
    end
end

end
