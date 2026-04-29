clear;

% ------------------------------------------------
function [u,dt,dx,xvek] = loglogFD(M,N,T)

A = diag(ones(M-2,1),-1) + diag(-2*ones(M-1,1)) + diag(ones(M-2,1),1);
dx = 3.14/M; dt = T/N;

u = zeros(M-1,N+1);
xvek = (dx:dx:3.14-dx)';
u(:,1) = xvek.*(3.14-xvek);   %Temperatur vid t=0

for i=1:N
   u(:,i+1)=(eye(M-1)-dt/dx^2*A)\u(:,i);
end

end
% ------------------------------------------------

function [hvek,felvek] = loglogplot_x(M,N,T)

K = 4;
hvek = zeros(1,4);
uvek = zeros(1,5);

for k = 0:K
    M2 = M*2^k;
    [u, dt, dx, ~] = loglogFD(M2, N, T);
    
    if k > 0
        hvek(k) = dx;
    end

    uvek(k+1) = u(1/dx,0.5/dt);
end

felvek = abs(uvek(1:end-1)-uvek(2:end));

end

function main1x()
Mx = 3.14/0.01;
Nx = 1e2;
T = 1;

[hvek,felvek] = loglogplot_x(Mx,Nx,T);
loglog(hvek,felvek,'o-', hvek,2e-4*hvek.^1, hvek,0.2*hvek.^2, hvek,1e2*hvek.^3)
grid on;
legend('steglängd mot felet loglog för x','lutning 1','lutning 2','lutning 3')
end

% main1x()

% ------------------------------------------------
function [hvek,felvek] = loglogplot_t(M,N,T)
    
K = 4;
hvek = zeros(1,4);
uvek = zeros(1,5);

for k = 0:K
    N2 = N*2^k;
    [u, dt, dx, ~] = loglogFD(M, N2, T);
    
    if k > 0
        hvek(k) = dt;
    end

    uvek(k+1) = u(1/dx,0.5/dt);
end

felvek = abs(uvek(1:end-1)-uvek(2:end));

end

function main1t()
M = 3.14/0.01;
N = 1e2;
T = 1;

[hvek,felvek] = loglogplot_t(M,N,T);
loglog(hvek,felvek,'o-', hvek,2*hvek.^1, hvek,1e3*hvek.^2, hvek,1e6*hvek.^3)
grid on;
legend('steglängd mot felet loglog för t','lutning 1','lutning 2','lutning 3')
end

main1t()

