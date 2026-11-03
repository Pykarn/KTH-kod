%SIMPLEX12 Crude simplex code for solving an LP problem including phase I.
%          [x,z,y,r,B,iter1,iter2] = simplex12(A,b,c)
%          solves the problem
%                        minimize     c'x
%                        subject to   A x = b
%                                     x >= 0
%
%          On successful termination, x contains the optimal solution,
%          z contains the final objective function value, y contains
%          an optimal dual solution, and r contains the dual slacks.
%          B contains the indices of the final basis, and iter1 and iter2
%          denote the numbers of iterations in phases I and II.
%
%          Crude version, written by Anders Forsgren for use in
%          SF1811 Optimization.
%
function [x,z,y,r,B,iter1,iter2] = simplex12(A,b,c)

[m,n] = size(A);
fuzz = sqrt(eps);

% Use consistent vector formats.
b = b(:);
c = c(:);

% Basic dimension checks.
if length(b) ~= m
    error('The length of b must equal the number of rows of A.');
end
if length(c) ~= n
    error('The length of c must equal the number of columns of A.');
end

% Phase I: add one artificial variable for each constraint. Choose the
% signs of the artificial columns so that the initial basis is feasible.
s = ones(m,1);
s(b < 0) = -1;
A1 = [A diag(s)];
c1 = [zeros(n,1); ones(m,1)];
B = n+1:n+m;

[~,suminf,~,~,B,iter1] = simplex(A1,b,c1,B);

if suminf > fuzz
    x = [];
    z = [];
    y = [];
    r = [];
    B = [];
    iter2 = [];
    fprintf('Error, no feasible solution exists \n\n')
else
    if any(B > n)
        fprintf('Warning, artificial variables are still basic \n')
        fprintf('Cannot be dealt with properly in this implementation \n\n')

        % Retain the artificial variables that are still basic and use a
        % large penalty for them in phase II.
        Bart = B(B > n);
        B = [B(B <= n), n+1:n+length(Bart)];
        A2 = A1(:,[1:n, Bart]);
        c2 = [c; 1e6*ones(length(Bart),1)];

        [x,z,y,r,B,iter2] = simplex(A2,b,c2,B);
        x = x(1:n);
        r = r(1:n);
    else
        [x,z,y,r,B,iter2] = simplex(A,b,c,B);
    end
end
