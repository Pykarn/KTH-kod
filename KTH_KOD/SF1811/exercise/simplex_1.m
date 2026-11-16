
%SIMPLEX Crude simplex code for solving an LP problem given an
%        initial feasible basis B.
%        [x,z,y,r,B,iter] = simplex(A,b,c,B)
%        solves the problem
%                        minimize     c'x
%                        subject to   A x = b
%                                     x >= 0
%
%        On successful termination, x contains the optimal solution, and
%        z contains the final objective function value. y contains
%        an optimal dual solution and r contains the dual slacks. On entry,
%        B is a row vector containing the indices of the basis, which
%        is assumed to be primal feasible. On exit, B contains the indices
%        of the final basis and iter denotes the number of iterations.
%
%        Notation selected to fit with the KTH course SF1811 Optimization.
%
%        Crude version, written by Anders Forsgren for use in SF1811 Optimization
%
function [x,z,y,r,B,iter] = simplex(A,b,c,B)

[m,n] = size(A);

% Use consistent vector formats.
b = b(:);
c = c(:);
B = B(:)';

% Basic dimension checks.
if length(b) ~= m
    error('The length of b must equal the number of rows of A.');
end
if length(c) ~= n
    error('The length of c must equal the number of columns of A.');
end
if length(B) ~= m || length(unique(B)) ~= m ...
        || any(B < 1) || any(B > n) || any(B ~= round(B))
    error('B must contain m distinct valid column indices.');
end

iter = 0;
rNmin = -1;
fuzz = sqrt(eps);

% Initialize full-length output vectors.
x = zeros(n,1);
r = zeros(n,1);

fprintf('\n  Iter              z       Bp        k           tmax \n')

N = 1:n;
N(B) = [];

AB = A(:,B);
if rank(AB) < m
    error('The initial basis matrix is singular.');
end

xB = AB\b;
if any(xB < -fuzz)
    error('The initial basis is not primal feasible.');
end

x(B) = xB;

while rNmin < -fuzz

    AB = A(:,B);
    AN = A(:,N);

    cB = c(B);
    cN = c(N);

    y = (AB')\cB;
    rN = cN-AN'*y;

    z = cB'*xB;

    % Dantzig rule: choose k in N with minimum reduced cost r_k.
    [rNmin,q] = min(rN);

    % Optimal if rN >= 0, up to the numerical tolerance fuzz.
    if rNmin < -fuzz
        k = N(q);

        % dxB corresponds to Delta x_B in the formula sheet.
        dxB = -AB\A(:,k);
        dxBneg = find(dxB < -fuzz);

        if ~isempty(dxBneg)
            [tmax,pneg] = min(xB(dxBneg)./(-dxB(dxBneg)));
            p = dxBneg(pneg);
        else
            fprintf('\n Problem has unbounded solution \n\n')
            break;
        end

        xB = xB+tmax*dxB;
        xB(p) = tmax;

        Bp = B(p);
        B(p) = k;
        N(q) = Bp;

        str1 = sprintf(' %5g   %12.5e',iter,z);
        str2 = sprintf(' %8g   %6g   %12.2e',Bp,k,tmax);
        disp([str1 str2])

        iter = iter+1;

    else
        str1 = sprintf(' %5g   %12.5e',iter,z);
        disp(str1)

        fprintf('  Optimal solution found \n\n')
    end

end

x(:) = 0;
x(B) = xB;

r(:) = 0;
r(N) = rN;
