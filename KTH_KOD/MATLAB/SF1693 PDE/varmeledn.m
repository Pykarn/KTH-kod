%Losning av varmeledningsekvationen med FE
clear all, close all, clc
alpha=0.1;    %Termisk diffusivitet
T=1;        %Sluttid
M=100;       %Antal delintervall i x
N=100;       %Antal delintervall i t
A=diag(ones(M-2,1),-1)+diag(-2*ones(M-1,1))+diag(ones(M-2,1),1);
dx=1/M; dt=T/N;

u=zeros(M-1,N+1);   %Initialisering
x=(dx:dx:1-dx)';
u(:,1)=x.*(1-x);    %Temperatur vid t=0
%Framat Euler
% for i=1:N
%     u(:,i+1)=u(:,i)+alpha*dt/dx^2*A*u(:,i);
% end

%Bakat Euler
for i=1:N
   u(:,i+1)=(eye(M-1)-dt*alpha/dx^2*A)\u(:,i);
end

surf(0:dt:T,[0;x;1], [zeros(1,N+1); u; zeros(1,N+1)])
ylabel('x'),xlabel('t'),

title(['Temperatur u med ',num2str(M),' steg i x och ', num2str(N), ' steg i t'])