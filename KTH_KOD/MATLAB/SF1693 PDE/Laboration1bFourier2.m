clear all
close all
%g(x) = x , [0,pi/2)
%       0 , [pi/2,pi]
N=20;  % antal Fourierbasfunktioner
tN=50; % antal tidssteg
xN=50;  % antal x-steg
T=4;  % sluttid
dx=pi/xN;
dt=T/tN;
x=0:dx:pi;
t=0:dt:T;
u=zeros(length(x),length(t));

for n=1:N
    %Fourierkoefficient
    bn = -(cos(n*pi/2))/n + (2/pi)*sin(n*pi/2)/n^2;
    u = u + bn * sin(n*x') * exp(-n^2*t);
end

surf(x,t,u');
xlabel('x'),ylabel('t'),zlabel('u')

%Fel


