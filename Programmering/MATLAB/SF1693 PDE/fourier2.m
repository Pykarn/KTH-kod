clear all
close all
N=100;
figure
x=0:0.001:pi;
f=zeros(1,length(x));
s=0;
for n=1:N
    f=f-4*((-1)^n -1)/n^3/pi*sin(n*x);
    s=s+(4*((-1)^n -1)/n^3/pi)^2;
end
plot(x,f)
hold on
plot(x,x.*(pi-x),'r')
s=pi*s/2;
E=sqrt(pi^5/30 -s)
title(['medelkvadratfel  ', num2str(E)])
hold off