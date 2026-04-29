clear;

function [u,xvek,tvek] = fourier1(T,N,tN,xN)
dx = pi/xN;
dt = T/tN;
xvek  = 0:dx:pi;
tvek  = 0:dt:T;
u  = zeros(length(xvek),length(tvek));

for k=0:N
    u = u + (8/(pi*(2*k+1)^3)) * sin((2*k+1)*xvek') * exp(-(2*k+1)^2*tvek);
end

end

function [u,xvek,tvek] = fourier2(T,N,tN,xN)
dx = pi/xN;
dt = T/tN;
xvek  = 0:dx:pi;
tvek  = 0:dt:T;
u  = zeros(length(xvek),length(tvek));

for n=1:N
    u = u + (((2*sin(n*pi/2))/(pi*n^2)) - cos(n*pi/2)/n) * sin(n*xvek') * exp(-n^2*tvek);
end

end

N = 50; tN = 100; xN = 100; T = 4;
[u,xvek,tvek] = fourier1(T,N,tN,xN);

% surf(tvek,xvek,u)
% xlabel('t'),ylabel('x'),zlabel('u')

ustart = zeros(size(xvek));

%plot(xvek,x.*(pi-x));

for k=0:N
    ustart = ustart+8/pi/(2*k+1)^3*sin((2*k+1)*xvek);
end

plot(xvek,xvek.*(pi-xvek)-ustart,'.-')

