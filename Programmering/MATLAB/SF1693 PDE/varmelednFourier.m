clear all
close all
N=20; % antal Fourierbasfunktioner
tN=100; % antal tidssteg
xN=100; % antal x-steg
T=4; %sluttid
dx=pi/xN;
dt=T/tN;
x=0:dx:pi;
t=0:dt:T;
u=zeros(length(x),length(t));
for k=0:N
    u=u+8/pi/(2*k+1)^3*sin((2*k+1)*x')*exp(-(2*k+1)^2*t);
end
surf(x,t,u');
xlabel('x'),ylabel('t'),zlabel('u')

figure

uinit=zeros(size(x));
hold on
plot(x,x.*(pi-x));
for k=0:3
    uinit=uinit+8/pi/(2*k+1)^3*sin((2*k+1)*x);
    plot(x,uinit);
    pause;
end
hold off

figure

uinit=zeros(size(x));
hold on
for k=0:3
    uinit=uinit+8/pi/(2*k+1)^3*sin((2*k+1)*x);
    plot(x,x.*(pi-x)-uinit);
    xlabel('x'),
    title('Differens i temperatur vid tiden t=0');
    pause;
end
hold off
legend('k=0','k=1','k=2','k=3');
