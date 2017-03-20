clear all
data = dlmread('SVR_dataset.txt');

x = data(:, 1);
y = data(:, 2);

h = 0.5;
C = 4;
eps = 0.1;

n = size(x, 1);

% Parameters are 2n by 1 vector, whose first n elements are
% p = alpha - alpha ^ star and next n elements are
% q = alpha + alpha ^ star

H = zeros(2 * n, 2 * n);
for i = 1:n
    for j = 1:n
        temp = norm(x(i) - x(j), 2);
        H(i, j) = exp(- temp ^ 2 / 2 / h ^ 2);
    end
end

f = - eps * ones(2 * n, 1);
f(1:50, 1) = y;

A = zeros(4 * n, 2 * n);
for i = 1:n
    A(i, i) = 0.5;
    A(i, i + n) = 0.5;
    A(i + n, i) = -0.5;
    A(i + n, i + n) = 0.5;
    A(i + 2 * n, i) = -0.5;
    A(i + 2 * n, i + n) = -0.5;
    A(i + 3 * n, i) = 0.5;
    A(i + 3 * n, i + n) = -0.5;
end

b = zeros(4 * n, 1);

b(1:2 * n, 1) = C;

params = quadprog(H, -f, A, b);

%% Plot

p = params(1:n, 1);
q = params(n+1:100, 1);

% find support vector
limit = 0.00001;
sv_idx = find(abs(p) > limit);
nsv_idx = find(abs(p) <= limit);

x_sv = x(sv_idx, 1);
x_nsv = x(nsv_idx, 1);
y_sv = y(sv_idx, 1);
y_nsv = y(nsv_idx, 1);

cut = 99;
x_axis = 0:1/cut:1;
y_axis = zeros(size(x_axis));
for i = 1:cut+1
    K = zeros(n, 1);
    for j = 1:n
        K(j, 1) = exp(-norm(x_axis(i) - x(j), 2) ^ 2 / 2 / h ^ 2);
    end
    y_axis(i) = dot(K, p);
end

figure % opens new figure window
plot(x_axis, y_axis);
hold on;
scatter(x_sv, y_sv, '*');
hold on;scatter(x_nsv, y_nsv);
legend('prediction curve', 'support vector');