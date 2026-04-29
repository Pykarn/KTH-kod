%Losning av varmeledningsekvationen med FE
clear all, close all, clc
alpha=1;    %Termisk diffusivitet
T=4;        %Sluttid
M=100;       %Antal delintervall i x
N=100;       %Antal delintervall i t
A=diag(ones(M-2,1),-1)+diag(-2*ones(M-1,1))+diag(ones(M-2,1),1);
dx=pi/M; dt=T/N;




u=zeros(M-1,N+1);   %Initialisering
x=(dx:dx:pi-dx)';
%Temperatur vid t=0
for i=1:length(x)
    if x(i) < pi/2
        u(i,1) = x(i);   % g(x) = x
    else
        u(i,1) = 0;      % g(x) = 0
    end
end

%Framåt Euler
% for i=1:N
%     u(:,i+1)=u(:,i)+dt/dx^2*A*u(:,i);
% end

%Bakåt Euler
for i=1:N
   u(:,i+1)=(eye(M-1)-dt/dx^2*A)\u(:,i);
end

surf(0:dt:T,[0;x;pi], [zeros(1,N+1); u; zeros(1,N+1)])
ylabel('x'),xlabel('t'),

title(['Temperatur u med ',num2str(M),' steg i x och ', num2str(N), ' steg i t'])