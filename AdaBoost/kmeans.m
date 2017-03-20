faces = csvread('kmeans_data.csv');

num_faces = size(faces, 1);
K = 5;
max_iter = 50;
run_time = 15;
obj = zeros(run_time, max_iter);
Cs= cell(run_time, 1);
%% uniformly at random
figure;
hold on;
for run = 1:run_time
rp = randperm(num_faces);
C = faces(rp(1:K), :);
memberships = zeros(num_faces, 1);
for iter = 1:max_iter
    dis = pdist2(C, faces);
    [~, memberships] = min(dis);
    for i = 1:K
        C(i, :) = mean(faces(memberships == i, :), 1);
    end
    
    obj(run, iter) = 0;
    for i = 1:K
        tmp = faces(memberships == i, :);
        obj(run, iter) = obj(run, iter) + sum(sum(pdist2(tmp, tmp).^2)) / size(tmp, 1);
    end
    fprintf('Iter %d... Obj %f...\n', iter, obj(run, iter));
end
Cs{run} = C;
plot([1:max_iter], obj(run, :));
hold on;
end

% finally, plot the mean faces with the minimal objective
[min_obj, min_index] = min(obj(:, end));
mean_faces = Cs{min_index};

to_show = [];
for i = 1:K
    cur = reshape(mean_faces(i, :), [19, 19]);
    to_show = [to_show, cur];
end
figure;
imshow(uint8(to_show));
hold on;

