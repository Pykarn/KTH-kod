clear;

function [u,dt,dx,xvek] = findiff1(M,N,T)

A = diag(ones(M-2,1),-1) + diag(-2*ones(M-1,1)) + diag(ones(M-2,1),1);
dx = pi/M; dt = T/N;

u = zeros(M-1,N+1);
xvek = (dx:dx:pi-dx)';
u(:,1) = xvek.*(pi-xvek);   %Temperatur vid t=0

%Framat Euler:
% for i=1:N
%     u(:,i+1) = u(:,i) + (dt/dx^2) * A*u(:,i);
% end

% Bakåt Euler:
for i=1:N
   u(:,i+1)=(eye(M-1)-dt/dx^2*A)\u(:,i);
end

end

function [u,dt,dx,xvek] = findiff2(M,N,T)
A = diag(ones(M-2,1),-1) + diag(-2*ones(M-1,1)) + diag(ones(M-2,1),1);
dx = pi/M; dt = T/N;

u = zeros(M-1,N+1);  
xvek = (dx:dx:pi-dx)';
u(:,1) = (xvek < pi/2) .* xvek; %Temperatur vid t=0, styckvis definierad

%Framat Euler:
% for i=1:N
%     u(:,i+1) = u(:,i) + (dt/dx^2) * A*u(:,i);
% end

% Bakåt Euler:
for i=1:N
   u(:,i+1)=(eye(M-1)-dt/dx^2*A)\u(:,i);
end

end

% Diskretisering och sluttid:
M = 1e2; N = 1e2; T = 1;

%  finita differensmetoden:
[u,dt,dx,xvek] = findiff1(M,N,T);

surf(0:dt:T,[0;xvek;pi], [zeros(1,N+1); u; zeros(1,N+1)])
ylabel('x'),xlabel('t'),

title(['Temperatur u med ',num2str(M),' steg i x och ', num2str(N), ' steg i t'])
