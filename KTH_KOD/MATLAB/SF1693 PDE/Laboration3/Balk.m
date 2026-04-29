

function [b1, b2, b3, energivek, U] = balk(N,M,delta)

%N=100
dx = 1/N;
x = linspace(0,1,N+1)';

%man jobbar bara med inre punkter
xinre = x(2:end-1);

%f(x) = 1
F = ones(N-1,1);

D = (1/dx^2)*(diag(-2*ones(N-1,1)) + diag(ones(N-2,1),1) + diag(ones(N-2,1),-1));

%gissning
b1 = 0.3;
b2 = 0.3;
%delta = 0.5, tillräckligt litet för konvergens

%M=100;

energivek = zeros(M,1);

%man kör allt i samma for loop
%allt beror på b1, b2, b3 som itereras över
%med gradientmetoden
for m = 1:M
    b3 = 1 - b1 - b2;

    Bn = zeros(N-1,1);
    for n = 1:N-1
        if xinre(n) < 1/3
            Bn(n) = b1;
        elseif xinre(n) <= 2/3
            Bn(n) = b2;
        else
            Bn(n) = b3;
        end
    end
    B = diag(Bn);

    W = D\F;
    U = (B*D)\W;

    DU = D*U;
    
    %dL för b1 och b2
    d_b1L = 0;
    d_b2L = 0;

    %summera d_b1L och d_b2L enligt derivering
    for n = 1:N-1
        %d_b1L
        if xinre(n)<1/3
            d_b1L = d_b1L - (DU(n)^2)*dx;
        end
        if xinre(n)>2/3
            d_b1L = d_b1L + (DU(n)^2)*dx;
        end
        %d_b2L
        if xinre(n)>=1/3 && xinre(n)<=2/3
            d_b2L = d_b2L - (DU(n)^2)*dx;
        end
        if xinre(n)>2/3
            d_b2L = d_b2L + (DU(n)^2)*dx;
        end
    end
    
    %gradientmetoden
    b1 = b1 - delta*d_b1L;
    b2 = b2 - delta*d_b2L;

    energivek(m) = (F'*U)*dx;
end


b3 = 1 - b1 - b2;
W = D\F;
U = (B*D)\W;

 
end

function plot100100()
[~, ~, ~, energivek, ~] = balk(100, 100, 0.5);
iterationer = 1:100;
plot(iterationer, energivek)
end


function U = solveU(N, b1, b2, b3)

dx = 1/N;
x = linspace(0,1,N+1)';
xinre = x(2:end-1);

F = ones(N-1,1);

D = (1/dx^2)*(diag(-2*ones(N-1,1)) + ...
    diag(ones(N-2,1),1) + ...
    diag(ones(N-2,1),-1));

Bn = zeros(N-1,1);
for n = 1:N-1
    if xinre(n) < 1/3
        Bn(n) = b1;
    elseif xinre(n) <= 2/3
        Bn(n) = b2;
    else
        Bn(n) = b3;
    end
end

B = diag(Bn);

W = D\F;
U = (B*D)\W;

end


function plotEfel()

Ns = [25 50 100 200 400];
M = 1000;
delta = 0.1;

%fixerat b
[b1, b2, b3, ~, ~] = balk(500, M, delta);

Evek = zeros(length(Ns),1);

for i = 1:length(Ns)
    N = Ns(i);

    U = solveU(N, b1, b2, b3);

    dx = 1/N;
    F = ones(N-1,1);

    Evek(i) = (F' * U) * dx;
end


fel = abs(diff(Evek));
dx = 1./Ns;

figure
loglog(dx(2:end), fel, '--o','LineWidth',2)
hold on
grid on

% referenslinjer
C1 = fel(1)/(dx(2)^1);
C2 = fel(1)/(dx(2)^2);

loglog(dx(2:end), C1*dx(2:end).^1, '--')
loglog(dx(2:end), C2*dx(2:end).^2, '--')

xlabel('dx')
ylabel('Energi Fel')
title('Energifel (fixerat b)')
legend('Fel','O(dx)','O(dx^2)','Location','best')

end




function plotUfel()

Ns = [25 50 100 200 400];
M = 1000;
delta = 0.1;

Uvek = cell(length(Ns),1);


for i = 1:length(Ns)
    [~,~,~,~, U] = balk(Ns(i), M, delta);
    Uvek{i} = U;
end

fel = zeros(length(Ns)-1,1);

dx = 1./Ns(1:end-1);

for i = 1:length(Ns)-1
    U1 = Uvek{i}  ;
    U2 = Uvek{i+1};
    U_err = norm(U1-U2(2:2:end)) * sqrt(dx(i));
    fel(i) = U_err;
end



figure
loglog(dx, fel, '--o','LineWidth',2)
hold on
grid on

xlabel('dx')
ylabel('Fel i U')
title('Konvergens av U')

%referenslinjer
C1 = fel(1)/(dx(1)^1);
C2 = fel(1)/(dx(1)^2);

ref1 = C1 * dx.^1;
ref2 = C2 * dx.^2;

loglog(dx, ref1, '--','LineWidth',1.5)
loglog(dx, ref2, '--','LineWidth',1.5)

legend('Fel','lutning 1','lutning 2','Location','best')

end





function plotUfel_fixed()

Ns = [25 50 100 200 400];
M = 1000;
delta = 0.1;

%fixerat b
[b1, b2, b3, ~, ~] = balk(800, M, delta);
% b1 = 1/3;
% b2 = 1/3;
% b3 = 1/3;

Uvek = cell(length(Ns),1);

for i = 1:length(Ns)
    Uvek{i} = solveU(Ns(i), b1, b2, b3);
end

fel = zeros(length(Ns)-1,1);

dx = 1./Ns(2:end);

for i = 1:length(Ns)-1
    U1 = Uvek{i};
    U2 = Uvek{i+1};
    fel(i) = norm(U1 - U2(2:2:end))*sqrt(dx(i)) ;
end



figure
loglog(dx, fel, '--o','LineWidth',2)
hold on
grid on

%referenslinjer
C1 = fel(1)/(dx(1)^1);
C2 = fel(1)/(dx(1)^2);

loglog(dx, C1*dx.^1, '--')
loglog(dx, C2*dx.^2, '--')

legend('Fel','O(dx)','O(dx^2)')
xlabel('dx')
ylabel('Fel')
title('Konvergens av U (fixat b)')

end

function plotUpunktfel()

Ns = [25 50 100 200 400];
M = 1000;
delta = 0.5;

%fixerat b
[b1, b2, b3, ~, ~] = balk(500, M, delta);

Uval = zeros(length(Ns),1);

for i = 1:length(Ns)
    N = Ns(i);
    U = solveU(N, b1, b2, b3);

    %index för mittenpunkt
    idx = floor((N-1)/2);

    Uval(i) = U(idx);
end


fel = abs(diff(Uval));

dx = 1./Ns;

figure
loglog(dx(2:end), fel, '--o','LineWidth',2)
hold on
grid on


C1 = fel(1)/(dx(2)^1);
C2 = fel(1)/(dx(2)^2);

loglog(dx(2:end), C1*dx(2:end).^1, '--')
loglog(dx(2:end), C2*dx(2:end).^2, '--')

legend('Fel','O(dx)','O(dx^2)','Location','best')
xlabel('dx')
ylabel('Fel i U(x_0)')
title('Konvergens i en punkt')

end

% plotEfel()
% 
% plotUfel()

% plotUfel_fixed()

% plotUpunktfel()
%plot100100()
