faces = csvread('kmeans_data.csv');

num_faces = size(faces, 1);
K = 5;
max_iter = 50;
run_time = 15;
obj = zeros(run_time, max_iter);
Cs = cell(run_time, 1);
%% kmeans++
figure;
hold on;
for run = 1:run_time
rp = randperm(num_faces);
C(1, :) = faces(rp(1), :);
for m = 2:K
    dis = pdist2(C, faces).^2;
    [near_dis] = min(dist);
    param = near_dis / sum(near_ids);
    index = sampler(param);
    C(m, :) = faces(index, :);
end
    
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
