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
u(:,1)=x.*(pi-x);    %Temperatur vid t=0

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


%fel

%Referenslösning tas fram med liten steglängd
M_ref = 800;
dx_ref = pi/M_ref;
dt_ref = T/N;
A_ref = diag(ones(M_ref-2,1),-1)+diag(-2*ones(M_ref-1,1))+diag(ones(M_ref-2,1),1);

x_ref = (dx_ref:dx_ref:pi-dx_ref)';
u_ref = zeros(M_ref-1, N+1);

%Startdata g(x)
u_ref(:,1) = x_ref.*(pi-x_ref);

% Beräkna referenslösning med BE
for i = 1:N
    u_ref(:,i+1) = (eye(M_ref-1)-dt_ref/dx_ref^2*A_ref)\u_ref(:,i);
end

%Relevant slutlösning
u_ref_end = u_ref(:,end);

%Testa fem steglängder
M_values = [100 50 25 12 6];  %dvs dx halveras fem gånger
errors = zeros(length(M_values),1);
dx_values = zeros(length(M_values),1);

for j = 1:length(M_values)
    Mj = M_values(j);
    dxj = pi/Mj;
    dx_values(j) = dxj;

    Aj = diag(ones(Mj-2,1),-1)+diag(-2*ones(Mj-1,1))+diag(ones(Mj-2,1),1);

    xj = (dxj:dxj:pi-dxj)';
    uj = zeros(Mj-1, N+1);
    uj(:,1) = xj.*(pi-xj);

    for i = 1:N
        uj(:,i+1) = (eye(Mj-1)-dt_ref/dxj^2*Aj)\uj(:,i);
    end

    %Interpolera referenslösningen till samma punkter
    u_ref_interp = interp1(x_ref, u_ref_end, xj);

    errors(j) = sqrt(dxj * sum((u_ref_interp - uj(:,end)).^2));
end

%Loglog-plot
figure
loglog(dx_values, errors, 'o-', 'LineWidth', 2)
xlabel('Steglängd dx')
ylabel('Fel (L2-norm)')
title('Fel mot steglängd (Bakåt Euler)')
grid on


