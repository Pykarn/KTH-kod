%FEM
% -(au')' = f   
% u(0) = 0
% a(1)u'(1) = g

% a, f, g godtyckliga

%Lösa diskreta ekvationen:
% A * xi_vek = L
% Aij = A(phi_j, phi_i), xi_vek = (xi_1, ... , xi_N)', 
% L = (L(phi_1), ... , L(phi_N))'

N = 1000;
h = 1/(N+1);
x_vek = 0:h:1;


a = @(x) exp(x);
f = @(x) exp(x);
g = 1;

%Gausskvadratur (Enpunkt) för diagonal element
%index förskjuten med 1
function u_hela = enpunkt(N, h, x_vek, a, f, g)
    D = zeros(N,1);
    for i=1:N
        D(i) = 1/h*(a((x_vek(i+2) + x_vek(i+1))/2) + a((x_vek(i+1) + x_vek(i))/2));
    end
    I_D = 1/h*a((x_vek(N+2)+x_vek(N+1))/2);
    D(end+1) = I_D;
    
    D1 = zeros(N,1);
    for i=1:N
        xm = (x_vek(i+2) + x_vek(i+1))/2;
        D1(i) = -1/h*a(xm);
    end
    
    
    A = diag(D) + diag(D1,1) + diag(D1,-1);
    
    %index förskjuten med 1
    L = zeros(N,1);
    for i=1:N
        L(i) = h/2*(f((x_vek(i+1)+x_vek(i+2))/2) + f((x_vek(i+1)+x_vek(i))/2)); 
    end 
    %integral på randpunkt N+1
    I_L = h/2*(f((x_vek(N)+x_vek(N+1))/2)) + g;
    
    L(end+1)=I_L;
    u_inne = A \ L;
    
    % u(0) = 0
    % a(1)u'(1) = g
    
    u_hela = [0; u_inne];    
end

u_hela_enpunkt = enpunkt(N, h, x_vek, a, f, g);

plot(x_vek, u_hela_enpunkt)
title("Numerisk lösning, enpunkt")
xlabel("x-axel")
ylabel("Temperatur u")


%Gausskvadratur (Tvåpunkt) för diagonal element
%index förskjuten med 1
function u_hela = tvapunkt(N, h, x_vek, a, f, g)
    D = zeros(N,1);
    for i=1:N
        D(i) = 1/(2*h)*(...
        a((x_vek(i) + x_vek(i+1))/2 - h/(2*sqrt(3))) + ...
        a((x_vek(i) + x_vek(i+1))/2 + h/(2*sqrt(3))) + ...
        a((x_vek(i+1) + x_vek(i+2))/2 - h/(2*sqrt(3))) + ...
        a((x_vek(i+1) + x_vek(i+2))/2 + h/(2*sqrt(3))));

    end
    xm = (x_vek(N+2) + x_vek(N+1))/2;
    I_D = (1/(2*h)) * (a(xm-h/(2*sqrt(3))) + a(xm+h/(2*sqrt(3))));


    D(end+1) = I_D;
    
    D1 = zeros(N,1);
    for i=1:N
        xm = (x_vek(i+2) + x_vek(i+1))/2;
        D1(i) = -(1/(2*h)) * (a(xm-h/(2*sqrt(3))) + a(xm+h/(2*sqrt(3))));

    end
    
    
    A = diag(D) + diag(D1,1) + diag(D1,-1);
    
    %index förskjuten med 1
    L = zeros(N,1);
    for i=1:N
        L(i) = h/2*(f((x_vek(i+1)+x_vek(i+2))/2) + f((x_vek(i+1)+x_vek(i))/2)); 
    end 
    %integral på randpunkt N+1
    I_L = h/2*(f((x_vek(N)+x_vek(N+1))/2)) + g;
    
    L(end+1)=I_L;
    
     
    u_inne = A \ L;
    
    % u(0) = 0
    % a(1)u'(1) = g
    
    u_hela = [0; u_inne];       
end

u_hela_tvapunkt = tvapunkt(N, h, x_vek, a, f, g);
figure
plot(x_vek, u_hela_tvapunkt)
title("Numerisk lösning, tvapunkt")
xlabel("x-axel")
ylabel("Temperatur u")


figure
u_exact = @(x) (1+exp(1)) - x - (1+exp(1))*exp(-x);
plot(x_vek, u_exact(x_vek))
title("Exakt lösning")

