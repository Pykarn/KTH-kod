clear all
close all

N=10000;
%figure
x=-1:0.0001:1;
f=0.75*ones(1,length(x));
s=9/8;
for n=1:N
    f=f+((-1)^n -1)/n^2/pi^2*cos(n*pi*x) - sin(n*pi*x)/n/pi;
    s=s+((((-1)^n -1)/n^2/pi^2)^2 + (1/n/pi)^2);
end
plot(x,f)
E=sqrt(4/3-s)
title(['medelkvadratfel  ', num2str(E)])