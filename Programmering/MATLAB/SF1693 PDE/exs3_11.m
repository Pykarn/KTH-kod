clear all, close all
format long
x = [0.5,0.5,0.5]';
deltax = 100;

while norm(deltax) > 0.5*10^-7
f1 = 10 * x(1) - x(2) - x(1)^2 - x(2)^2;
f2 = x(1) + 10*x(2) - x(3) + x(2)^3 - 2;
f3 = x(1) + 3*x(3) +x(3)^3-1;

A = [10-2*x(1),-1-2*x(2), 0;1,10+3*x(2)^2,-1;1,0,3+3*x(3)^2];

b = [-f1,-f2,-f3]';

deltax = A\b;
x = x + deltax;
end
