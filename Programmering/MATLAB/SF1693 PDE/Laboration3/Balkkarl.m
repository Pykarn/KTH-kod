clear;

function [e_final,U] = balk(N,iterationer)
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
delta = 0.5; %tillräckligt litet för konvergens
energivek = zeros(iterationer,1);

%man kör allt i samma for loop
%allt beror på b1, b2, b3 som itereras över
%med gradientmetoden

for i = 1:iterationer

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

    energi = F'*U*dx;
    energivek(i) = energi;

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
        if xinre(n)>1/3 && xinre(n)<2/3
            d_b2L = d_b2L - (DU(n)^2)*dx;
        end
        if xinre(n)>2/3
            d_b2L = d_b2L + (DU(n)^2)*dx;
        end
    end
    

    %gradienmetoden
    b1 = b1 - delta*d_b1L;
    b2 = b2 - delta*d_b2L;

end

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

e_final = F'*U*dx;

end

% xvals = 1:iterationer;
% plot(xvals,energivek)

N_list = [25, 50, 100, 200, 400];

Uvec = cell(length(N_list),1);

for i = 1:length(N_list)
    
[~,U] = balk(N_list(i),1000);
Uvec{i} = U;

end

error_vec = zeros(length(N_list)-1,1);

for i = 1:length(N_list)-1
    U1 = Uvec{i}  ;
    U2 = Uvec{i+1};
    U_err = norm(U1-U2(2:2:end));
    error_vec(i) = U_err;
end

h_vec = 1./N_list(2:length(N_list));

loglog(h_vec, error_vec, '-o',h_vec,h_vec.^1,h_vec,h_vec.^2,h_vec,h_vec.^0.5)


% e_final_vec = zeros(length(N_list),1);
% 
% iterationer = 1000;
% 
% 
% for i = 1:length(N_list)
%     N = N_list(i);
%     [e_final,b1,b2] = balk(N, iterationer);
%     e_final_vec(i) = e_final;
% end
% 
% error_vec = abs(e_final_vec(2:length(N_list))-e_final_vec(1:length(N_list)-1));
% 
% h_vec = 1./N_list(2:length(N_list));
% 
% loglog(h_vec, error_vec,'o-', h_vec, h_vec.^2, h_vec, h_vec)

grid on;
