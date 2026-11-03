%%% hw1data.m %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%
% Problem data for homework assignment 1, SF1811, 2026/2027
%
% function [A,b,c,B] = hw1data(YYMMDD)
%
% Provides matrices A, b, c, and an initial feasible basis B
% for the given date of birth YYMMDD.
%
% Written by Anders Forsgren
%
function [A,b,c,B] = hw1data(YYMMDD)

rng(YYMMDD);

A = [    -1     1
          0     1
          2     3
          2    -1  ];

b = [     2
          3
         14
          6  ];

c = [    -1
         -3  ];

const = 0.05;
A = A+const*randn(size(A));
b = b+const*randn(size(b));
c = c+const*randn(size(c));

m = size(A,1);

A = [A eye(m)];
c = [c; zeros(m,1)];

n = size(A,2);

B = n-m+1:n;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
